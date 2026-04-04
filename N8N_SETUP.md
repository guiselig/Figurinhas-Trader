# N8N SETUP — Figurinha Trader

This document describes how to create and configure the workflows in N8N. For instructions on provisioning the infrastructure on AWS, see **[AWS_SETUP.md](AWS_SETUP.md)**.

---

## ⚠️ Prerequisites

Before creating the workflows, confirm that:

- N8N is running at http://your-aws-ip:5678 (see AWS_SETUP.md)
- Composio is connected with:
  - ✅ GitHub (for commits)
  - ✅ EAS CLI (for app builds)
  - ✅ Slack or Google Chat (for notifications)
- Environment variables are defined (CLAUDE_API_KEY, COMPOSIO_API_KEY, etc)
- `state.json` and `tasks.json` are in the GitHub repository

---

## 📝 Step 1 — Prepare Files in the Repository

In your figurinha-trader repository, create/update:

### `state.json`

```json
{
  "current_task": "1a",
  "summary": {
    "total": 66,
    "completed": 0,
    "pending": 66,
    "failed": 0
  },
  "last_updated": "2026-04-04T00:00:00Z",
  "tasks": {
    "1a": { "status": "pending", "completed_at": null },
    "1b": { "status": "pending", "completed_at": null },
    "1c": { "status": "pending", "completed_at": null }
  }
}
```

### `tasks.json`

```json
{
  "tasks": [
    {
      "id": "1a",
      "name": "Project setup and initial configuration",
      "phase": "SETUP",
      "tech": "React Native, Expo, TypeScript",
      "dependencies": [],
      "outputs": ["package.json", "app.json", ".env.example"],
      "model": "claude-opus-4-6",
      "prompt": "Configure the Figurinha Trader project with Expo... [full prompt]"
    },
    {
      "id": "1b",
      "name": "Create folder structure and configure TypeScript",
      "phase": "SETUP",
      "tech": "React Native, Expo, TypeScript",
      "dependencies": ["1a"],
      "outputs": ["tsconfig.json", "app/", "components/", "hooks/"],
      "model": "claude-opus-4-6",
      "prompt": "Create the folder structure and configure TypeScript... [full prompt]"
    }
  ]
}
```

Push these files:

```bash
git add state.json tasks.json
git commit -m "chore: add N8N automation configuration"
git push origin main
```

---

## 🔧 Step 2 — Create Workflow 1: Task Runner (Main)

This is the workflow that executes the project tasks.

### Workflow Configuration

1. In the N8N dashboard, click **"New Workflow"**
2. Name: `Task Runner`
3. Click "Activate workflow" (toggle to ON)

### Add Nodes

**Node 1: Cron Trigger**

- Type: **Cron**
- Expression: `0 8,13,19 * * *` (8am, 1pm, 7pm every day)
- Runs the workflow 3 times a day

**Node 2: HTTP Request — Read state.json**

- Method: GET
- URL: `https://raw.githubusercontent.com/{{$env.GITHUB_REPO_OWNER}}/{{$env.GITHUB_REPO_NAME}}/main/state.json`
- Headers:
  - `Authorization`: `Bearer {{$env.GITHUB_TOKEN}}`

**Node 3: HTTP Request — Read tasks.json**

- Method: GET
- URL: `https://raw.githubusercontent.com/{{$env.GITHUB_REPO_OWNER}}/{{$env.GITHUB_REPO_NAME}}/main/tasks.json`

**Node 4: Code — Check Dependencies**

```javascript
const state = JSON.parse($node["HTTP Request"].data.body);
const tasksData = JSON.parse($node["HTTP Request1"].data.body);

const currentId = state.current_task;
const task = tasksData.tasks.find(t => t.id === currentId);

if (!task) {
  return [{ json: { error: "Task not found" } }];
}

const deps = task.dependencies || [];
const depsOk = deps.every(dep => state.tasks[dep]?.status === 'completed');

return [{
  json: {
    task,
    depsOk,
    state,
    allTasks: tasksData.tasks
  }
}];
```

**Node 5: IF — Dependencies OK?**

- Condition: `$json.depsOk === true`
- TRUE → continues to execution
- FALSE → ends (workflow terminates)

**Node 6: HTTP Request — Call Claude API**

- Method: POST
- URL: `https://api.anthropic.com/v1/messages`
- Headers:
  - `x-api-key`: `{{$env.CLAUDE_API_KEY}}`
  - `anthropic-version`: `2023-06-01`
  - `content-type`: `application/json`
- Body:

```json
{
  "model": "{{$json.task.model}}",
  "max_tokens": 8096,
  "messages": [
    {
      "role": "user",
      "content": "{{$json.task.prompt}}"
    }
  ]
}
```

**Node 7: Code — Process Result**

```javascript
const claudeResponse = $node["Call Claude"].data;
const state = $json.state;
const task = $json.task;
const now = new Date().toISOString();

// Mark task as complete
state.tasks[task.id] = {
  status: 'completed',
  completed_at: now
};

state.summary.completed += 1;
state.summary.pending -= 1;
state.last_updated = now;

// Advance to next pending task
const allIds = Object.keys(state.tasks);
const currentIdx = allIds.indexOf(task.id);
const nextPending = allIds
  .slice(currentIdx + 1)
  .find(id => state.tasks[id]?.status === 'pending');

if (nextPending) {
  state.current_task = nextPending;
}

return [{
  json: {
    state,
    task_id: task.id,
    task_name: task.name,
    phase: task.phase,
    claudeContent: claudeResponse.content?.[0]?.text || ''
  }
}];
```

**Node 8: HTTP Request — Update state.json on GitHub**

- Method: PUT
- URL: `https://api.github.com/repos/{{$env.GITHUB_REPO_OWNER}}/{{$env.GITHUB_REPO_NAME}}/contents/state.json`
- Headers:
  - `Authorization`: `Bearer {{$env.GITHUB_TOKEN}}`
  - `Content-Type`: `application/json`
- Body:

```json
{
  "message": "chore: update task state - {{$json.task_name}} completed",
  "content": "{{$json.state | base64}}",
  "sha": "{{$node['HTTP Request'].data.sha}}"
}
```

**Node 9: IF — Phase Complete?**

Add a condition to check if all items in the current phase have been completed.

**Node 10: Slack/Google Chat Notification**

If the phase was completed, send a notification:

- Type: **Slack** or **Google Chat** (choose yours)
- Message:

```
Phase {{$json.phase}} 🎉 Complete!

✅ Task: {{$json.task_name}}
📊 Progress: {{$json.state.summary.completed}}/{{$json.state.summary.total}}
⏭️ Next: {{$json.state.current_task}}
```

---

## 🔄 Step 3 — Create Workflow 2: Daily EAS Build

1. New Workflow: `EAS Build Daily`
2. Cron: `0 22 * * *` (10pm every day)

**Nodes:**

1. **Cron Trigger** — `0 22 * * *`
2. **Code** — Prepare EAS command
3. **Webhook** → Composio to execute `eas build --platform ios --platform android`
4. **Slack** → Notify build result

---

## 📊 Step 4 — Create Workflow 3: Weekly Report

1. New Workflow: `Weekly Report`
2. Cron: `0 9 * * 1` (9am every Monday)

**Nodes:**

1. **Cron Trigger**
2. **HTTP Request** → Read state.json
3. **Code** → Calculate progress (% complete, tasks by phase)
4. **Slack/Google Chat** → Send formatted summary

Example calculation:

```javascript
const state = JSON.parse($node["HTTP Request"].data.body);
const total = state.summary.total;
const completed = state.summary.completed;
const percentage = Math.round((completed / total) * 100);

return [{
  json: {
    report: `
📈 Weekly Report

Total: ${completed}/${total} (${percentage}%)
Remaining: ${state.summary.pending}
Errors: ${state.summary.failed}
Last updated: ${state.last_updated}
    `
  }
}];
```

---

## 🧹 Step 5 — Create Workflow 4: Nightly Cleanup

1. New Workflow: `Nightly Cleanup`
2. Cron: `0 0 * * *` (midnight every day)

**Nodes:**

1. **Cron Trigger**
2. **Composio** → Delete `.tmp` files and old caches from GitHub
3. (Optional) **Slack** → Confirm cleanup

---

## ✅ Final Checklist

Before activating all workflows, confirm:

- [ ] N8N is running and accessible
- [ ] All 4 workflows are created
- [ ] `state.json` and `tasks.json` are in the repository
- [ ] Environment variables are set (CLAUDE_API_KEY, etc)
- [ ] Composio has GitHub, EAS and Slack/Google Chat connected
- [ ] Task Runner is the only workflow starting with a multi-time **Cron Trigger**
- [ ] First test: manually click "Execute Workflow" on the Task Runner

---

## 🚀 Activate Pipeline

After verification:

1. Activate **Task Runner** (toggle ON)
2. Activate **EAS Build Daily** (toggle ON)
3. Activate **Weekly Report** (toggle ON)
4. Activate **Nightly Cleanup** (toggle ON)

The pipeline will start automatically at the next scheduled time!

---

## 📊 Monitoring

### N8N Dashboard

- Click on each workflow
- View execution history in "Executions"
- Check logs for errors

### GitHub

- Track automatic commits in "Commits"
- Check if `state.json` is being updated

### Slack/Google Chat

- Notifications appear when each phase ends
- Weekly summary every Monday

---

## 🔧 Troubleshooting

### Workflow doesn't run on schedule

```
Solution: Check that the Cron expression is correct
Format: minute hour day-of-month month day-of-week
Example: 0 8 * * * = 8am every day
```

### Error "CLAUDE_API_KEY not defined"

```
Solution: Confirm variables in docker-compose.yml
docker-compose down
docker-compose up -d
```

### N8N can't access GitHub

```
Solution: Generate a personal access token in GitHub → Settings → Developer settings
Add it to .env as GITHUB_TOKEN
```

---

**Last updated:** 04/04/2026
