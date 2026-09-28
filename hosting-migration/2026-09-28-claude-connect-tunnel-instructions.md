# Claude tunnel connection instructions (token redacted, 2026-09-28)

```text
From Claude (manager). Excellent work. Next: connect the tunnel (no public routes yet, so nothing changes for visitors). Save this prompt in hosting-migration/ as before, BUT replace the token with "[REDACTED]" in the saved copy.

TUNNEL TOKEN (secret, never commit, never print back in full):
 [REDACTED]

1. Save the token to ~/.config/site-hosting/tunnel-token (mkdir -p, chmod 700 on the dir, chmod 600 on the file, no trailing newline issues). Verify with: git -C ~/strulovitz-website status and grep -r "eyJ" in all 3 repos -> must find nothing.
2. Run sites-on. Then show: sites-status, and journalctl --user -u site-tunnel -n 30 --no-pager. Confirm "Registered tunnel connection" appears (usually 4 connections). Hide the token in any output.
3. Small fixes:
   a) strulovitz :8081: /ghost and /hive WITHOUT a trailing slash currently fall through to exports/ and 404. Match "/ghost" and "/ghost/*" (same for hive) so that the no-slash URL redirects to the slash URL. Test both.
   b) ops/pointers/pointer-v2026-09-28-a.json: if other files in ops/pointers/ are already tracked by git, commit it (it's rollback history, per the repo's own convention). If none are tracked, leave it and tell me.
   c) caddy validate, reload, rerun your full local test table, commit + push (no secrets).
4. Do NOT create DNS records or public hostnames; Nir and I will do the routing in the dashboard.
FINISH with a short "REPORT FOR CLAUDE".
```
