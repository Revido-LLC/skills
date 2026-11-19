# Supabase

Use the Supabase CLI, dashboard or any Supabase tool your agent has. Read only.

Look for:

- **Scheduled jobs:** `pg_cron` jobs and scheduled edge functions each need a `heartbeat`. The job (or the function it calls) pings the push URL on success.
- **Activity table:** find the table that proves the business is alive (orders, messages, sign-ins). It feeds the daily activity heartbeat, for example "no new rows in N business hours".
- **Edge functions:** public functions that serve an essential task are `uptime` or `flow` targets; webhook receivers (payments, email) matter most.
- **Auth:** a working login backs the login `flow` and the login-page check.
- **Storage:** if an essential task uploads or serves files, include storage in `/health`.
- **Advisories and logs:** security and performance advisories, and recent errors, belong under gaps.

Do not read or print row data. Counts and timestamps are enough.
