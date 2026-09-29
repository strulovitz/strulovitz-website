# Hosting the three websites locally

These files live in the Strulovitz GitHub repository, so the same instructions
can be used on the Debian laptop and the Linux Mint desktop. Apache is separate
and stays untouched. The local websites listen only on `127.0.0.1`, not on the
public network. No services are enabled automatically at boot.

- `sites-status` shows which services are running and checks ports 8081-8083.
- `sites-on` checks GitHub for updates to the three existing repos, rebuilds the
  Strulovitz export only when its website source changes, and starts the local
  web server, tunnel, and keep-awake service. It refuses to start anything if
  the tunnel token is missing. It does not upload to DreamHost.
- `sites-off` stops these three services, leaving Apache alone.

The local pages are `http://127.0.0.1:8081/` (Strulovitz), `:8082/`
(Learnime), and `:8083/` (Peak Together). Open each in Firefox after starting
the local server. The Strulovitz output comes from `exports/`; the current
version and the old `v2026-09-11-c` links both work through the local `current`
symlink. `ghost/` and `hive/` are served from the same repository separately.
Build output stays in the repository's gitignored `exports/` folder.

For now, only `site-caddy.service` can be started to preview locally; the
tunnel has not been set up. Once the Cloudflare dashboard gives Nir a tunnel
token, store it **outside** GitHub as `~/.config/site-hosting/tunnel-token` with
mode 600. Never paste or commit the token. The tunnel must point the three
domains to this computer's ports 8081, 8082, and 8083 respectively.

On this laptop Caddy is already running. After a restart, preview the sites
without a tunnel with `systemctl --user start site-caddy.service`, then run
`sites-status`. Stop the preview with `systemctl --user stop site-caddy.service`.
These commands only control our Caddy user service; they never touch Apache.
Cloudflared 2026.9.3 is installed and supports `--token-file`, but the tunnel
service must not start until Nir has a token from the dashboard.

To switch computers later: stop hosting on the old computer with `sites-off`;
on the other Linux computer, pull the Strulovitz, Anime, and Peak Together
repos, install Caddy and cloudflared there, link the repo's user services and
scripts there, and use that computer's own private tunnel token. Do not run
both tunnels for the same websites simultaneously. Use `sites-on` then
`sites-status` on the new computer. No DreamHost deploy script is used.

## Clickable icons

Run `hosting/bin/install-launchers` once to add **Websites ON** and **Websites OFF**
to the applications menu and your desktop. Each opens a terminal and waits for
Enter so you can read the result. On GNOME, the Desktop Icons NG (DING)
extension must be enabled to see the desktop copies; on Mint Cinnamon, desktop
icons work natively. Re-run the installer after moving the repository to update
its absolute paths.
