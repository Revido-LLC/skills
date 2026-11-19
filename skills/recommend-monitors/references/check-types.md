# Building each check well

Read the section for the check you are recommending.

## Contents

- uptime and content
- health
- heartbeat
- flow (robot check)
- error_rate
- ssl and domain

## uptime and content

- Monitor the login page and the API base, not only the home page.
- A content check looks for text that proves the page rendered (the login button label) or alerts when an error string appears. It catches pages that return 200 but are blank or broken.

## health

- One route, `/health`, protected by a secret header, so the public cannot probe it.
- It checks each dependency (database, queue, payment or email provider that sits on an essential task) and returns pass or fail per dependency.
- It reveals no versions, hostnames, stack traces or table names.
- Keep it fast and cheap. It must not write data.

## heartbeat

- One check per scheduled job or worker. The job pings the push URL when it finishes successfully, never at the start.
- Set the window to the schedule plus a margin. A job that runs every night at 02:00 gets about a 26-hour window.
- Add a daily activity check where the business has a clear signal, for example "no orders saved in 2 hours during business hours". The signal comes from the scan.

## flow (robot check)

- Reuse the project's end-to-end tests where they exist. One flow per essential task: log in, place an order, run payroll.
- Run on a schedule from outside the client's hosting, every 5 to 10 minutes, with a dedicated test account agreed with the client at onboarding.
- Retry once before alerting. A check that pages falsely twice in a month is fixed or downgraded within a week.
- Never trigger real payments, emails to real users or fulfilment. Mark test records clearly and clean them up. If the client cannot accept test records in production, stop the flow before the final submit.

## error_rate

- Error tracking alert rules post to the portal webhook. Personal data must be scrubbed before events leave the app.
- Default priority P1. Tune the threshold after the first week of real traffic.

## ssl and domain

- Alert at 30, 14 and 3 days before expiry. Priorities: P3 at 30, P2 at 14, P1 at 3.
- Domain expiry matters most for domains registered by someone other than Revido; note who owns the registrar login.
