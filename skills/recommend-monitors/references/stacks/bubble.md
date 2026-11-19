# Bubble

A Bubble app has no code repo to scan, so ask for editor access or a walkthrough, and treat anything you cannot see as an open question.

Look for:

- **No custom `/health`:** monitor the live page and add a `content` check for text that proves the page rendered. If the Workflow API or Data API is enabled, a lightweight API workflow that touches the database can serve as the `health` target; add that as a dev task.
- **Scheduled workflows:** recurring events and scheduled API workflows each need a `heartbeat`. Add a final step to the workflow that calls the push URL.
- **Plugins and API connector calls:** third-party calls on an essential task (payments, email, SMS) are the usual cause of silent failure; list them and prefer a `flow` on premium and above.
- **Capacity:** note any workload or capacity limits near the plan ceiling under gaps.
- **Error tracking:** Bubble's server logs are not alerting. Ask whether anything watches them.
