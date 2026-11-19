# Monitoring plan: {CLIENT} – {PROJECT}

**Plan:** {standard | priority | premium | 24x7 | unknown}   **Project code:** {CODE}   **Hosting:** {HOSTING}

## 1. Summary

{One or two lines: what this plan covers and what it does not.}

## 2. Monitors

| Name | Type | Target | What it catches | Priority | Contact group | Interval | Lowest plan |
|---|---|---|---|---|---|---|---|
| {CLIENT} – {PROJECT} – {Check} | uptime | {URL} | {impact in plain words} | P0 | p0 | 60 s | standard |

## 3. Dev tasks before the monitors can work

- [ ] {Task} (unblocks: {monitor names})

## 4. Manual setup steps

- [ ] {Step for an admin}

## 5. Gaps, upsells and open questions

- {Gap}: {upsell plan, or "open question"}

## 6. Readiness checklist

- [ ] Health endpoint live and monitored, with a content check on the main page
- [ ] A robot check running for each essential task (premium and 24x7)
- [ ] Heartbeat pings in every scheduled job (priority and above)
- [ ] Error tracking installed, personal data scrubbed
- [ ] Tested rollback and a linked runbook
- [ ] Contact groups, phone numbers and Slack channel set up

## Machine-readable plan

```json
{ "schema_version": "1" }
```
