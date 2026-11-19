---
name: recommend-monitors
description: Use when an app is being finished, handed over or put under a support plan, or when asked what to monitor, which alerts should page someone, or what priority a monitor deserves. Also when adding health checks, heartbeats, uptime checks or error alerts to an app.
---

# Recommend monitors

## Overview

Turn an app into a monitoring plan a human can approve: which checks, what priority, who gets paged, and what the developers must build first.

**Core principle:** recommend only. Never create, change, pause or delete a monitor without explicit approval in the conversation.

Policy source of truth: the doc "Revido SLA, Support & On-Call Policy" (claude.ai/artifact/6t1DuNe3SawqQyzztryrZy) and the plans page sla.revido.co. If either is reachable, read it and follow it where it differs from this skill.

## When to use

- A client app is going live, or a client has signed a support plan.
- Someone asks what to monitor, what should wake people up, or what priority an alert gets.
- A dev is adding a health endpoint, heartbeat or error alert and needs to know where it fits.

Not for: building dashboards or log pipelines, responding to a live incident, writing the runbook.

## Steps

1. **Scan the app.** If your agent can dispatch a subagent, give it [scout-prompt.md](scout-prompt.md) filled in; otherwise run the same scan yourself. Stack-specific hints live in `references/stacks/` (railway, supabase, bubble, dokploy, vercel). Read only the ones that match.
2. **Collect what the scan can't tell you:** client, project name, project code, support plan (standard, priority, premium, 24x7), the 2-3 essential tasks agreed at onboarding, production URLs. Look in the Revido portal and the repo before asking. Ask once, together.
3. **Pick checks** from the table below.
4. **Assign priorities** with the rules below.
5. **Write the plan** in the output format, then stop and wait for approval.

If the plan is unknown, do not guess. Recommend the full set and tag every monitor with the lowest plan that includes it (`min_plan`), so the reader can cut down to what was bought.

## Checks

| Check | Catches | Lowest plan |
|---|---|---|
| `uptime` | site or API unreachable | standard |
| `health` | a dependency failing behind a page that still loads | standard |
| `content` | blank or error pages that return 200 | standard |
| `ssl`, `domain` | certificate or domain expiry | standard |
| `error_rate` | exception spike users hit before any check does | standard |
| `heartbeat` | scheduled job or worker silently stopped; no business activity today | priority |
| `flow` | an essential task broken end to end (robot check) | premium |

Never present a check as part of a plan that doesn't include it. If it would clearly help, list it as an upsell naming the plan that has it. How to build each check well: [references/check-types.md](references/check-types.md). StatusCake naming, tags and settings: [references/statuscake.md](references/statuscake.md).

## Priorities

Priority is impact times workaround.

- **P0:** the platform is down, an essential task is blocked, or there is any security or data problem.
- **P1:** a major feature is broken and there is no workaround.
- **P2:** a feature is broken but a workaround exists, or the app is degraded.
- **P3:** cosmetic or informational.

Rules:

- Every essential task has at least one P0 monitor: a `flow` on premium and 24x7, the closest `uptime`, `health` or `content` check on lower plans.
- More than about 4 P0 monitors per project means something is mis-ranked. Justify each one or lower it.
- `error_rate` defaults to P1.
- `ssl` and `domain` are P2 at 14 days left and P1 at 3 days.
- A `heartbeat` for a job users depend on the same day is P1. A nightly or weekly job is P2.
- Marketing-site content checks are P3.

Paging by plan (contact group `p0` pages a human, `standard` goes to the portal queue only):

| | standard | priority | premium | 24x7 |
|---|---|---|---|---|
| Out-of-hours paging | never | never | P0 until 22:00 evenings and weekends | P0 and P1, any hour |
| Urgent response | 4 business hours | 1 business hour | 1 business hour; 2 hours out of hours | 15 minutes |

## Output

Write the plan in this order. [assets/plan-template.md](assets/plan-template.md) has the skeleton.

1. **Summary:** client, project, plan, what the plan covers, in one or two lines.
2. **Monitors table:** name, type, target, what it catches, priority, contact group, interval, lowest plan.
3. **Dev tasks** needed before the monitors can work, each naming the monitors it unblocks.
4. **Manual setup steps** for an admin: contact groups, phone numbers, Slack channel.
5. **Gaps and upsells**, and open questions.
6. **Readiness checklist** for this project.

Then end with one fenced `json` block named `monitor-plan` that follows [assets/monitor-plan.schema.json](assets/monitor-plan.schema.json). Humans approve the table; the portal reads the block. Both must say the same thing. Monitor names follow `CLIENT – Project – Check`.

```json
{
  "schema_version": "1",
  "project": { "client": "ACME", "name": "Ordering", "code": "ACME-ORD", "hosting": ["railway", "supabase"], "plan": "premium" },
  "monitors": [
    { "name": "ACME – Ordering – Login page", "type": "uptime", "target": "https://orders.acme.example/login", "catches": "App down or login unreachable", "priority": "P0", "min_plan": "standard", "contact_group": "p0", "interval_seconds": 60, "evidence": "railway domain orders.acme.example" },
    { "name": "ACME – Ordering – Place order", "type": "flow", "target": "tests/e2e/order.spec.ts", "catches": "Customers cannot place an order", "priority": "P0", "min_plan": "premium", "contact_group": "p0", "interval_seconds": 600, "evidence": "essential task: place an order" }
  ],
  "dev_tasks": [
    { "title": "Add /health that checks the database and Stripe", "why": "No health endpoint exists", "blocks": ["ACME – Ordering – Health"] }
  ],
  "manual_steps": ["Create contact groups p0 and standard in StatusCake"],
  "gaps": [{ "item": "No error tracking installed", "upsell_plan": "standard" }],
  "readiness": [{ "item": "Runbook linked in the portal", "done": false }]
}
```

## Applying (only after approval)

- Prefer the Revido portal's monitoring toggle once it exists: the portal is the source of truth and monitors are never edited by hand.
- Before then, produce a script or exact API calls that create the approved monitors, with the API token read from an environment variable. Never put a token in chat or in a file. Make it idempotent: look monitors up by name or tag and update them rather than duplicate.
- After applying, list each monitor with its ID and ask for a test alert through the whole path.

## Common mistakes

| Mistake | Fix |
|---|---|
| Marking everything P0 | Cap at about 4; rank by impact and workaround |
| Recommending robot checks on a standard plan as included | Tag `min_plan: premium` and list as an upsell |
| Monitoring only the home page | Map each essential task to a check |
| A health endpoint that reveals internals | Secret header, dependency pass/fail only |
| Heartbeat pinged at job start | Ping on success, at the end |
| Table and JSON disagree | Generate the table from the JSON |
| Creating monitors "to save time" | Wait for approval |
