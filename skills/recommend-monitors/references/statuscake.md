# StatusCake settings

Revido runs hosted StatusCake (Superior plan). The Revido portal is the source of truth for monitors; once the portal's monitoring toggle exists, nobody edits monitors by hand in StatusCake.

**Verify before applying anything:** StatusCake's API changes. Check its current API docs for the exact field names for tags, find string, confirmation, regions, custom headers, push tests, SSL alert days, domain monitoring and contact groups. Do not rely on memory or on this file for field names.

## Conventions

- **Name:** `CLIENT – Project – Check`, for example `ACME – Ordering – Login page`.
- **Tags:** the project code, a priority tag (`p0` to `p3`) and the plan name.
- **Uptime tests:** HTTP, 1-minute checks, several regions, confirmation from at least 2 locations before alerting, timeout 15 to 30 seconds.
- **Health:** the `/health` route with the secret header, sent as a custom header.
- **Content:** a find-string test on the expected text, or an alert when an error string appears.
- **Heartbeat:** a push check per job, window set as in check-types.md.
- **SSL:** alerts at 30, 14 and 3 days.
- **Status page:** only if the client wants one.

## Contact groups

Two groups, created once by hand:

- **p0:** the portal webhook. On premium and 24x7, also a phone call and SMS to management and the week's backup, as the fallback when the portal is down.
- **standard:** the portal webhook only.

Until the portal is live, use Slack and email, plus the phone call to the on-call dev on premium and 24x7.

## Applying through the API

- Read the token from an environment variable such as `STATUSCAKE_API_TOKEN`. Never write it to a file or print it.
- Look up existing tests by name or tag and update them; never create duplicates.
- Afterwards list each monitor with its ID and send a test alert through the full path.
