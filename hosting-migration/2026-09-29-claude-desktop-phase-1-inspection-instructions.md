You are working on Nir's Desktop PC (Linux Mint 22). Phase 1 = READ-ONLY inspection. Do NOT install, change, create, move, delete, clone or pull anything.

HARD RULES (for all phases): never touch Windows/NTFS partitions; don't break existing installs; no apt upgrade/full-upgrade; no new top-level project folders; GitHub is the single source of truth; never run ops/deploy.sh or ops/deploy_windows.py.

Check and report:
1. OS version, hostname, username, $HOME, is ~/.local/bin in PATH?
2. `which git curl python3 cloudflared caddy nginx apache2` (plus versions of the ones that exist)
3. Are ports 8081, 8082, 8083, 2019 free? (`ss -ltnp`). If any is taken, say by what.
4. `find ~ -maxdepth 4 -name .git -type d 2>/dev/null`. For each clone of strulovitz-website, Anime, peaktogether-website: path, `git remote -v`, `git status -sb` (short). Report duplicates, don't delete them.
5. If Anime isn't cloned: its size on GitHub (`curl -s https://api.github.com/repos/strulovitz/Anime | grep '"size"'`, in KB).
6. Sleep settings, read-only: `gsettings list-recursively org.cinnamon.settings-daemon.plugins.power | grep -i sleep` and `grep -v '^#' /etc/systemd/logind.conf | grep .`

Reply with a SHORT report (max 20 lines), no long explanations.
