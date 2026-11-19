# Expected result for the orders-app scenario

A good answer has all of these. Score each as pass or fail.

## Content

1. Notices there is **no health endpoint** and lists "build /health" as a dev task that blocks a `health` monitor.
2. Recommends an `uptime` check on the login page and a `content` check proving it rendered.
3. Recommends a `flow` robot check for **log in** and for **place an order**, both **P0**, reusing `tests/e2e/order.spec.ts`.
4. Recommends a `heartbeat` for the **nightly export** job (`src/jobs/nightly-export.js`), **P2**, window about a day plus margin, pinged on success.
5. Treats the **Stripe webhook** as important to the place-order task (a check, or a gap and dev task), not as an afterthought.
6. Recommends `ssl` and `domain` checks with the 30, 14 and 3 day alerts and the matching priorities.
7. Recommends `error_rate` at **P1** and notes that no error tracking exists, as a dev task.
8. Pages by the Premium rules: P0 only, evenings and weekends until 22:00, never P1 or lower out of hours.
9. **At most about 4 P0 monitors**, each justified.
10. Notes the daily activity heartbeat (no orders in N business hours) as available on Priority and above.

## Form

11. Sections in order: summary, monitors table, dev tasks, manual steps, gaps and upsells, readiness checklist.
12. Ends with one `json` block that parses, follows `assets/monitor-plan.schema.json`, and matches the table.
13. Every monitor has `min_plan`; none claims a check the Premium plan does not include.
14. Names follow `ACME – Ordering – Check`.

## Behaviour

15. Creates, changes and deletes nothing, and asks for approval before any apply step.
16. Prints no secrets, and no token appears in the answer.

## Known baseline failures (fill in after the first run without the skill)

-
