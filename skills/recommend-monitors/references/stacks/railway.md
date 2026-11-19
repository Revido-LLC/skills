# Railway

Use the Railway CLI or any Railway tool your agent has. Read only.

Look for:

- **Services and domains:** list the services and their public domains. Each production domain gets an `uptime` check; the domain list is the evidence for targets.
- **Cron and worker services:** a service with a cron schedule, or one that is a queue worker, needs a `heartbeat`. The schedule sets the heartbeat window.
- **Health check path:** see whether the service config (the dashboard, or `railway.json`) sets a health check path. If it does, point the `health` monitor at the same route; if not, add "build `/health`" as a dev task.
- **Databases:** a Railway-hosted database should be covered by the app's `/health`, not monitored directly from outside.
- **Recent failures and restarts:** crash loops and recent failed deploys show what usually breaks. Mention them under gaps.
