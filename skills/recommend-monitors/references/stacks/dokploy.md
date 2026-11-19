# Dokploy

Read the Dokploy project through its dashboard or API if you have access, plus the repo's Dockerfile or compose file.

Look for:

- **Applications and domains:** each public domain on an application is an `uptime` target.
- **Compose services and workers:** every worker or queue consumer in the compose file needs a `heartbeat`.
- **Scheduled jobs:** check the application's schedules and any cron container. Each gets a `heartbeat`.
- **Health check:** see whether the Dockerfile or compose file defines a health check and which route it calls; point the `health` monitor at the same route, or add "build `/health`" as a dev task.
- **Databases and volumes:** cover them through the app's `/health`. Backups that matter get their own `heartbeat` on the backup job.
- **Host health:** a single VPS is a shared failure point. Mention it under gaps when several clients' apps sit on one host, and keep the monitoring itself on a different provider from the apps it watches.
