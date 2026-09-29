# Claude's hosted-by instructions, 2026-09-29 (verbatim)

```text
rom Claude (manager). Keep this session short and cheap: do only what is listed, and give short answers. Save this prompt in hosting-migration/ as before.

1. Run sites-status. If anything is not running, run sites-on and show sites-status again.
2. In hosting/Caddyfile, add to ALL THREE site blocks (8081, 8082, 8083), before the other handlers:
   handle /hosted-by {
       header Cache-Control "no-store"
       respond "Served by {system.hostname} (home PC via Cloudflare Tunnel)" 200
   }
   First check that no real file/folder named "hosted-by" exists in the 3 sites.
3. In hosting/bin/sites-on, print this reminder at the start: "REMINDER: run sites-off on the OTHER computer first. Never host from both at the same time (their strulovitz build versions differ, which would break pages)."
4. caddy validate, reload, then curl http://127.0.0.1:808{1,2,3}/hosted-by and show the output.
5. Commit + push (no secrets). Reply in max 10 lines.
```
