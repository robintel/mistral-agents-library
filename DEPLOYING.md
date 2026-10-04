# Deploying the library

How the agents map onto Mistral's actual tooling. Verified against
docs.mistral.ai and the mistralai/mistral-vibe repository as of
2026-10; TOML key names evolve — confirm against your Vibe version
(the docs pages: Agents, Skills, Install and setup).

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
| workflows | skills: `/orient`, `/tour`, `/coverage`, `/gdpr-audit`, `/upgrade` |
| the target repo | a thin AGENTS.md pointing at the orchestrator |

## First-run recipe (verified schema)

Each profile is one self-contained TOML: the agent body composed
into `instructions` inline, plus the keys that make it a role.

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
- The ten-minute verification, before scripting the batch:
  1. One orchestrator profile, hand-written — `vibe --agent
     orchestrator`, confirm the composed prompt loads and Shift+Tab
     lists it.
  2. One subagent profile — confirm the orchestrator spawns it and
     the prompt applies.
  3. Misspell one key on purpose: a complaint means loud errors
     (safe world); silence means keys can be ignored (verify
     everything, twice).
  4. Generate the remaining profiles from `manifest.yaml`.
- The orchestrator's escalation path: subagent profiles cannot raise
  their own model — escalation happens by the orchestrator's own
  per-task decision encoded at composition time (a second profile per
  escalated tier is the workaround if needed).
- This deployment gives the tiers teeth: a t1 subagent literally
  runs on a t1 model.
