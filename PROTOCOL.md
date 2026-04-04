# PROTOCOL — Figurinha Trader

This file defines Claude's behavior when called by N8N to execute a task. N8N is responsible for all orchestration — reading state, checking dependencies, updating results, and committing. Claude only receives the task instruction and returns the result.

---

## What Claude receives

N8N sends a JSON payload with the following fields:

```json
{
  "id": "4a",
  "name": "Collection screen: sticker list",
  "phase": "COLLECTION",
  "tech": "React Native + Expo Router + Supabase",
  "outputs": ["src/app/(tabs)/collection/index.tsx"],
  "skills": ["frontend-design", "web-artifacts-builder", "claude-d3js-skill", "canvas-design"],
  "prompt": "..."
}
```

---

## What Claude does

### 1. Load skills

Load all skills listed in `skills`, in the order they appear, before any action. No exceptions. If a skill fails to load, return immediately with `status: error` and a description of the problem.

### 2. Execute

Execute the task as described in `prompt`, using `tech` as the stack reference and `outputs` as the list of artifacts to be generated. Each file in `outputs` must be created at the exact path specified.

### 3. Return result

When finished, return a JSON with the following structure:

```json
{
  "task_id": "4a",
  "status": "completed",
  "artifacts": [
    { "path": "src/app/(tabs)/collection/index.tsx", "created": true }
  ],
  "error": null
}
```

In case of partial or total failure:

```json
{
  "task_id": "4a",
  "status": "failed",
  "artifacts": [],
  "error": "Objective description of what failed and why."
}
```

---

## Rules

- Do not read or modify `state.json` or `tasks.json`. This is the exclusive responsibility of N8N.
- Do not make decisions about execution order or dependencies. This has already been resolved by N8N before this call arrives.
- The return must always be valid JSON. N8N depends on this structure to update the project state.
- Commits are made by N8N via Composio after receiving the return. Claude does not commit.
