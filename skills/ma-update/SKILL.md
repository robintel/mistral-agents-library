---
name: ma-update
description: Check for and apply updates to the Mistral Agents Library
user-invocable: true
allowed-tools:
  - bash
  - read_file
---

# Mistral Agents Library Update

You are invoked as `/ma-update`. Your task is to check for updates to
the Mistral Agents Library and apply them if available.

## Steps

1. **Find the library repository:**
   - Look for AGENTS.md in the current directory. If it contains a
     reference to the Mistral Agents Library, extract the path.
   - Alternatively, check common locations:
     - `~/.vibe/agents/AGENTS.md` (user-level installation)
     - `./AGENTS.md` (project-level installation)
   - If AGENTS.md references a path like `/path/to/mistral-agents-library`,
     use that as the library root.

2. **Check current state:**
   - Run: `cd <library_path> && ./install.py --check`
   - Report whether updates are available and what version they would
     update from/to.

3. **If updates are available:**
   - Ask the user: "Update available. Apply now? (yes/no)"
   - If yes: `cd <library_path> && ./install.py --update`
   - Report the result: success, failure, or already up to date.

4. **If no updates:**
   - Report: "Mistral Agents Library is already up to date (vX)."

5. **Error handling:**
   - If the library path cannot be found, ask the user to provide it.
   - If install.py fails, report the error and suggest manual update.

## User interaction

- Always confirm before applying updates (unless the user explicitly
  requested automatic updates).
- Show the version change: "Updating from vX to vY".
- Show a brief changelog if available (from CHANGELOG.md).
- Report success: "Updated to vY. Reload VS Code or restart CLI to use."

## Notes

- This skill requires the library to be installed via git (not a
  downloaded zip) so that `git pull` works.
- The skill uses the same installer that was used for the original
  installation, ensuring consistency.
- On Windows, use backslashes in paths and `py install.py` if Python
  is not the default.
