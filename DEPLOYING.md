# Deploying the library

How the agents map onto Mistral's actual tooling. Verified against
docs.mistral.ai and the mistralai/mistral-vibe repository as of
2026-10; TOML key names evolve — confirm against your Vibe version
(the docs pages: Agents, Skills, Install and setup).

**Note:** Running any agent (including the orchestrator) requires a valid
`MISTRAL_API_KEY` environment variable. The installation and update procedures
do not require this key as they only perform git operations.

## How Mistral Vibe works

Vibe Code is the CLI and VS Code agent (the extension connects via
ACP). It has three extension mechanisms, and this library uses all
three:

1. **Agent profiles** — TOML files in `~/.vibe/agents/` (user) or
   `.vibe/agents/` (project), switched with `vibe --agent <name>` or
   Shift+Tab. The schema, verified from the mistral-vibe source
   (`vibe/core/agents/models.py`): the profile's name is its filename;
   the popped keys are `display_name`, `description`, `safety`
   (`safe`/`neutral`/`destructive`/`yolo`/`smart`), `agent_type`
   (`agent` or `subagent`), and `instructions` — the system prompt,
   inline in the TOML as a multiline string, no separate file needed.
   Everything else lands in the config `overrides`: `active_model`,
   `enabled_tools`, `disabled_tools`, and per-tool rules such as
   `tools.write_file.permission` with allowlists.
2. **Subagents** — profiles with `agent_type = "subagent"`:
   delegation-only, spawned by the model through the task tool, not
   user-selectable. Per the docs, subagents cannot ask the user
   questions — which is this library's protocol already: specialists
   return `needs-input` through the orchestrator.
3. **Skills** — directories with a `SKILL.md` (the Agent Skills
   specification, portable to other agents), in `./.vibe/skills/`
   (project) or `~/.vibe/skills/` (user). `user-invocable: true`
   makes a skill a slash command — in the CLI and in the VS Code
   extension's slash picker. `allowed-tools` scopes what it may
   call. On Vibe Work (web and mobile), skills are invoked with `@`.

There is no Copilot-style `/agents` command list; the equivalents are
Shift+Tab for profiles and the slash picker for skills.

## The mapping

| Library concept | Mistral mechanism |
|-----------------|-------------------|
| orchestrator.md | an agent profile — the one you run |
| the 49 specialists | subagent TOMLs, spawned by the orchestrator |
| agent bodies | prompt files: standards.md + body, composed |
| task classes | the routing table from manifest.yaml, carried into the orchestrator's prompt |
| dialects | files on disk, read at dispatch: reference the library by path in the brief |
| tier routing | `active_model` per profile, from the manifest's tier table |
| workflows | skills: `/ma-orient`, `/ma-tour`, `/ma-coverage`, `/ma-gdpr-audit`, `/ma-upgrade`, `/ma-update`, `/ma-autocorrect`, `/ma-framework-context`, `/ma-ai-guardrails`, `/ma-governance-policy`, `/ma-dev-workflow`, `/ma-test-data`, `/ma-combinatorial`, `/ma-modernize`, `/ma-anti-agentic`, `/ma-chaos-testing`, `/ma-infra-security`, `/ma-test-methodologies`, `/ma-legacy-testing`, `/ma-design-principles` |
| the target repo | a thin AGENTS.md pointing at the orchestrator |

## The one-command install

`install.py` at the repo root automates the recipe below: it reads
`manifest.yaml`, composes each profile (shared standards + the agent
body + a deployment addendum), resolves the tier's model from
`models.resolved` (the strongest entry — the lists run
cheapest-first), pins the tool surface per role, and writes the
batch to `~/.vibe/agents/`:

```sh
./install.py                       # install or refresh all profiles
./install.py --dest DIR            # try a batch somewhere else first
./install.py --target /path/repo   # also write the thin AGENTS.md
./install.py --dry-run             # print the plan, write nothing
./install.py --check               # check if updates are available
./install.py --update              # pull latest and reinstall
```

On Windows, every shell installs the same batch: `install.bat`
from cmd, `.\install.ps1` from PowerShell, or `py install.py` —
same composition, same defaults, and the same generated header, so
the installers recognize and prune each other's stale output.
install.bat is a one-liner wrapper,
`powershell -ExecutionPolicy Bypass -File .\install.ps1` with the
arguments forwarded, so cmd needs no script-policy detour and no
Python: every entry point composes the same profiles. Equivalence
between them is a release test
(`smoke/parity.sh` runs it):
both must compose byte-identical profiles. Both read every source
through LF normalization — a `core.autocrlf` checkout and a
Windows library path (whose backslashes are escapes in TOML)
compose to the same files as on Linux.

Tool surfaces encode the role's rules: read-only by default (the
Explore trio), command access for the reproducers (debugger,
coverage-manager, flaky-test-analyst), the write set for the
executors. Reruns are idempotent; a rerun prunes profiles from
earlier installs that are no longer in the manifest, and profiles
you wrote by hand are left alone. Every generated file is validated
by parsing it back and comparing the instructions round-trip — the
silent-batch failure mode below cannot ship.

## Version tracking and updates

The installer tracks the library version in two places:

1. **Source of truth**: `manifest.yaml` contains a `version` field
   (currently `1`).
2. **Installed marker**: After installation, a `.mal_version` file
   is written to the profile directory (e.g., `~/.vibe/agents/.mal_version`)
   containing the installed version.

The `--check` and `--update` flags leverage this tracking:

- `--check`: Compares the installed version with the latest version
  from the remote repository. Reports if an update is available and
  shows the changelog entries since the installed version.
- `--update`: Performs a `git pull` in the library repository, then
  reinstalls all profiles with the latest version. This is equivalent
  to running `git pull && ./install.py` in one step.

Both flags use `git ls-remote` to fetch the latest version from `origin`
without requiring a local clone to be up to date first. If git is not
available or the repository is not a git clone, version checking falls
back to comparing with the local manifest version.

For Vibe users, the `/ma-update` skill provides the same functionality
through a discoverable slash command. It locates the library repository,
checks for updates, and applies them with user confirmation.

## First-run recipe (verified schema)

Each profile is one self-contained TOML: the agent body composed
into `instructions` inline, plus the keys that make it a role. This
is what `install.py` writes — read it to know exactly what lands on
disk.

1. **The orchestrator profile** (`~/.vibe/agents/orchestrator.toml`):

   ```toml
   description = "The agent library single source of truth"
   safety = "neutral"
   active_model = "mistral-small-latest"    # t1 per the manifest

   instructions = """
   <shared/standards.md>
   ---
   <orchestrator.md>
   ---
   ## Deployment addendum
   Specialists are subagent profiles, spawned by name. This
   deployment ships: <list>. manifest.yaml is the routing registry;
   the library lives at <path>; dialects attach by reading those
   files. A specialist not deployed: handle it yourself per your
   failure-handling rules, and say so.
   """
   ```

2. **Specialist subagents**, one per role the orchestrator
   dispatches, model and tools pinned by the manifest:

   ```toml
   # ~/.vibe/agents/app-cartographer.toml
   display_name = "App Cartographer"
   description = "Maps the application: skim or full. Read-only."
   safety = "safe"
   agent_type = "subagent"
   enabled_tools = ["grep", "read_file", "skill"]

   instructions = """
   <shared/standards.md>
   ---
   <sdlc/testing/app-cartographer.md>
   """
   ```

   Tool permissions encode the role's rules: reviewers and
   cartographers read-only via `enabled_tools` (the built-in Explore
   subagent uses the same trio); the implementer and code-developer
   write-capable — the library's "you audit, you never fix" made
   mechanical.
3. **Skills for the workflows** (`/orient`, `/tour`, `/coverage`):
   SKILL.md directories, `user-invocable: true` — the slash picker in
   the CLI and the VS Code extension carries them.
4. **The target repo**: a thin AGENTS.md — "run the orchestrator
   profile; the agent library lives at <path>." Per Mistral's own
   guidance, AGENTS.md stays small; the specialists and skills carry
   the detail, loaded only when dispatched.

## Clean-room smoke test

`smoke/` ships a container-based smoke test that exercises the
deployed batch without touching the host: the image is the
environment spec (Vibe CLI + Python, nothing library-specific baked
in), the library mounts read-only, and the whole HOME dies with the
container.

```sh
docker build -t mistral-agents-smoke smoke/
docker run --rm -e MISTRAL_API_KEY \
  -v "$(pwd)":/library:ro mistral-agents-smoke /library/smoke/smoke.sh
```

Knobs: `TARGET_URL` clones a fixture repo instead of the default
target (the library itself — known ground truth, so the assertion is
checkable), `MAX_TURNS` (12) and `TIMEOUT_SECS` (300) bound the run.
The same image is the CI job: a GitHub Actions workflow is a thin
scheduler around the same `docker run`. With podman instead of
Docker, replace `docker` with `podman` in both commands and add
`:Z` to the volume (SELinux labeling; harmless elsewhere) — the
image and script are runtime-agnostic.

The run uses the CLI's verified programmatic mode (docs.mistral.ai,
Vibe Code > CLI > Work with the CLI): `vibe --agent orchestrator
--prompt "..." --max-turns N --output text --trust`, with
`MISTRAL_API_KEY` as an environment reference and `--trust` granting
folder trust per invocation. Asserts shape, not prose: the answer is
answer-length, describes the target, the target repo is unmodified,
and the tool cache stays empty — no permission prompt was answered,
so no tool may have been born (the birth gate, headless).

The image build and the first end-to-end run are verified (podman
4.9): 52 profiles installed, an on-target 135-word answer in 13
seconds, tool cache empty. Two hardening notes from that first
contact: export `PATH` before the Vibe installer — it exits
non-zero when its own command is not found on PATH — and a tree
written by mode-restricted tools (files at 600) must be
`chmod -R a+rX` before mounting, since the container runs as an
unprivileged user; a fresh git clone is already 644/755. Approval
semantics for a `neutral`-safety agent in programmatic mode stayed
unblocked on the observed run — the timeout remains the guard that
turns a blocked approval into a loud failure rather than a hung CI
job.

## Windows coverage, in three honest layers

A Linux host cannot run Windows containers, so the Windows installer
is tested where it can run: `smoke/parity.sh` executes install.ps1's
composition under the cross-platform pwsh and diffs it byte-for-byte
against install.py's batch — no API key, no model calls, pure
composition. The image pins PowerShell (7.6.6) and carries libicu76
for Debian trixie: .NET aborts without ICU, a failure the build
catches at `pwsh --version`.

A Windows machine with WSL adds a second layer, no container
needed: run parity.sh against the Windows checkout mounted at
/mnt/c, pwsh from a user-local tarball. Before .gitattributes
pinned working trees to LF, this run caught a real leak the
container's LF clone could never see:
install.ps1's here-strings carried the checkout's \r into
every composed profile (Python normalizes install.py's source;
PowerShell keeps the CR), so the two installers diverged on any
Windows checkout. Composed text is LF-normalized at emission now
(ConvertTo-TomlMultiline and the AGENTS.md template) — the
normalization stays load-bearing for pre-pin checkouts — and
parity passes from both a CRLF mount and an LF clone; the native
Windows PowerShell 5.1 batch (via install.bat) matches both
except the embedded library path, C:... backslash-escaped as
designed.

The third layer is the real Windows runner — Windows-native
Python composing backslash paths, ANSI decoding, ExecutionPolicy
— the windows-latest CI job to come.

## Caveats

- The mechanism shape (profiles, subagents, skills, the directories)
  is solid — it appeared consistently across the docs and the
  mistral-vibe repository. The exact TOML keys are softer: they were
  taken from documentation excerpts, some reconstructed, and Vibe
  ships fast — schema evolves.
- Why this matters more for the fifty-profile batch than for one
  hand-written profile: a wrong key in one profile fails loudly and
  immediately. A wrong key in a generated batch may fail *silently* —
  a subagent whose prompt reference was misspelled would run with no
  system prompt and no error message. Verify, then generate.
- The ten-minute verification, before trusting the batch:
  1. One orchestrator profile, hand-written — `vibe --agent
     orchestrator`, confirm the composed prompt loads and Shift+Tab
     lists it.
  2. One subagent profile — confirm the orchestrator spawns it and
     the prompt applies.
  3. Misspell one key on purpose: a complaint means loud errors
     (safe world); silence means keys can be ignored (verify
     everything, twice).
  4. Run `./install.py --dest /tmp/vibe-check`, confirm a profile
     loads, then install for real.
- The orchestrator's escalation path: subagent profiles cannot raise
  their own model — escalation happens by the orchestrator's own
  per-task decision encoded at composition time (a second profile per
  escalated tier is the workaround if needed).
- This deployment gives the tiers teeth: a t1 subagent literally
  runs on a t1 model.

## Integrations: connectors and MCP

The library never re-implements integrations; it rides the two
native mechanisms and treats them as session capabilities:

- **MCP servers** — user-configured in config.toml (`[[mcp_servers]]`:
  transport, url, headers, `api_key_env`); their tools arrive like
  built-ins, filtered with `enabled_tools`/`disabled_tools` patterns
  (`mcp_*`). Browsed with `/mcp`.
- **Connectors** — Mistral-managed integrations (managed MCP proxies):
  first-party and third-party (Jira, GitHub, Gmail, DeepWiki, ...),
  centrally registered on the platform, shared across Vibe Code and
  Vibe Work, OAuth handled by the platform. Browsed with
  `/connectors`; the directory is admin-curated — never suggest
  connecting unvetted servers.
- **API deployments**: platform connectors attach to conversations
  and agents with `tools=[{type: connector, connector_id}]` and
  include/exclude filtering — the same capability model, so the
  library's briefs carry capability names unchanged.

The discipline lives in `shared/standards.md` (rule 7) and
`shared/dialects/patterns/integrations.md`: discover, never assume;
the brief names the capabilities; authentication lives in the
integration, never in briefs, reports, or code.
