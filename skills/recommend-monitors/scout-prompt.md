# Scout prompt

Fill in the three placeholders and hand this to a read-only subagent. If your agent cannot dispatch subagents, follow the same instructions yourself.

---

You are scanning one application so someone can decide what to monitor. You only read; change nothing, run nothing that writes, and never print secrets or tokens (report that a secret exists, never its value).

Repo path: {REPO_PATH}
Hosting seen or expected: {HOSTING}   (railway, supabase, bubble, dokploy, vercel, other)
Essential tasks, if known: {ESSENTIAL_TASKS}

Find and report, with a file path or URL as evidence for each:

1. **Entry points:** production domains, the login page and login API route, the API base, any marketing site.
2. **Health endpoint:** does `/health` (or similar) exist? What does it check? Does the hosting config reference a health check path?
3. **Scheduled work:** cron jobs, queues, workers, background processes, recurring workflows, edge functions on a schedule. For each: name, schedule, what breaks for users if it stops, and whether it already pings anything.
4. **Third-party dependencies:** payment, email, auth, storage, webhooks in or out. Note which ones sit on an essential task.
5. **Business activity signal:** the table or event that proves the app is alive during business hours (orders, sign-ins, messages), and a plausible "none in N hours" threshold.
6. **Existing tests:** end-to-end tests (Playwright, Cypress, similar) that already walk an essential task and could become robot checks.
7. **Error tracking:** which tool, whether personal data is scrubbed, whether alert rules exist.
8. **Rollback and runbook:** a documented rollback, a runbook or handbook link, who has access.

Where hosting hints exist, read the matching file in `references/stacks/` first and use the hosting tools or CLI if one is available.

Reply with a short list per numbered item, "none found" where nothing exists, and a final line listing anything you could not check and why. Stay under 60 lines.
