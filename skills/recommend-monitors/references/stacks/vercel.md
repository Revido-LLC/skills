# Vercel

Read the repo plus `vercel.json` and the project settings if you have access.

Look for:

- **Domains:** production domains are `uptime` targets; preview URLs are not monitored.
- **Cron jobs:** entries in `vercel.json` under `crons` each need a `heartbeat`. The cron route pings the push URL on success.
- **API routes and functions:** build `/health` as a route that checks the database and any provider on an essential task; cold starts make a 15 to 30 second timeout sensible.
- **Edge and middleware:** a redirect or auth middleware that fails closed can take the whole site down; the login page `content` check catches it.
- **Error tracking:** check for an error tracker in the framework config and whether personal data is scrubbed.
