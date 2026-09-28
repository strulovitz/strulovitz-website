# REPORT FOR CLAUDE (read-only hosting investigation, 2026-09-28)

**Task 1:** Updated `hosting-migration/domains-status.md`: all three domains were added to Cloudflare Free on 2026-09-28 and have assigned nameservers `lia.ns.cloudflare.com`, `stanley.ns.cloudflare.com`. DreamHost nameserver-change and registrar-transfer status for Learnime and Peak Together were not provided, so those fields say `NOT VERIFIED`, not an invented status. Your prompt is saved verbatim in `hosting-migration/2026-09-28-claude-apache-investigation-instructions.md`. Both changes were pushed in commit `204af39`. No DNS settings were changed.

**Task 2: Apache and prior tunnel traces.** `apache2.service` is enabled and running, listening on `*:80` as `www-data`. `apache2ctl -S` shows one `*:80` virtual host (`deb-server.strulovitz.home`) with document root `/var/www/html`; `http://127.0.0.1/` returns HTTP 200 and the unmodified "Apache2 Debian Default Page: It works". The only enabled vhost is symlink `sites-enabled/000-default.conf -> ../sites-available/000-default.conf` (dated 2025-11-05). Its full content:

```apacheconf
<VirtualHost *:80>
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	#ServerName www.example.com

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf
</VirtualHost>
```

`/var/www/` contains only `html/`, containing the Debian default `index.html`. `dpkg.log*` records Apache installed **2025-11-05 14:21:42** and upgraded 2026-01-29, 2026-05-03, 2026-08-17. Systemd reverse dependencies show only the standard multi-user/graphical targets, no other service depending on Apache. No local site is configured in it; a leftover/unused installation is plausible but its original purpose cannot be established from these checks. **Do not stop it.** Unprivileged `systemctl status` and `apache2ctl -S` worked; sudo was unnecessary for these observations. `dpkg -l` found no cloudflared/caddy/nginx packages; `/etc/apt/sources.list.d/` contains only `github-cli.list`, `google-chrome.sources`, and `nodesource.sources`. No `cloudflared*` path was found on the accessible Linux root filesystem (`find / -xdev`); no cloudflared unit/config was found earlier. No dpkg-log cloudflared entry was found.

**Task 3: Strulovitz deployed layout.** `python3 ops/build-export.py` from `/home/nir/strulovitz-website/` would create `exports/vYYYY-MM-DD-letter/` containing `tesseract.html`, `src/`, `vendor/`, `data/`, `stories/`, `ideas/`, and generated `build-health.html`. At the `exports/` root it copies root HTML pages, `lightbox.js`, and `images/` from `site/`, substitutes the chosen version for `VERSION_FALLBACK` in HTML links, and writes `pointer.json` pointing to the new dated folder. It also writes `ops/pointers/pointer-vYYYY-MM-DD-letter.json` for rollback. The live DreamHost root currently points to `v2026-09-11-c/`; a new build today would use today's date, **not** recreate that old folder name. `exports/*` is gitignored except `.gitkeep` and `live-manifest.json`; `exports/` currently contains only `.gitkeep`. `ops/pointers/` is **not** gitignored: a new build would create an untracked pointer-history file. The build overwrites root files and pointer in local `exports/`, and copies substantial assets, but does not access the network, upload, delete existing versions, or change services. **It was not run.**

`ops/deploy.sh` would use SFTP to upload the version folder first, root files next, `pointer.json` last. `ops/deploy_windows.py` does the analogous upload with Paramiko (or root-pages-only upload); those scripts are the ones with network/remote side effects, and neither was run. `ghost/` and `hive/` live alongside `site/` at the repository root and their public `/ghost/index.html` and `/hive/index.html` each returned HTTP 200, but **build-export.py and both deploy scripts do not copy those directories**. To match the full live layout locally, `exports/` alone is insufficient; those two folders must be made available at the same served web root in a separate, future approved step. Do not assume the build includes them. These two live responses showed `Server: cloudflare`; that alone does not prove the registrar nameservers changed.

**Task 4: .htaccess.** Only `peaktogether-website/.htaccess` was found; none in `learnime-site/` or anywhere in `strulovitz-website/`. Full file:

```apacheconf
DirectoryIndex index.html

# Make directory URLs work without trailing slash
RewriteEngine On

# Redirect /folder to /folder/ (add trailing slash for clean URLs)
RewriteCond %{REQUEST_FILENAME} -d
RewriteRule ^(.+[^/])$ $1/ [R=301,L]

# Serve index.html when requesting a directory
RewriteCond %{REQUEST_FILENAME} -d
RewriteRule ^(.+)/$ $1/index.html [L]

# Caching for images (30 days)
<FilesMatch "\.(png|jpg|jpeg|gif|svg|webp)$">
    Header set Cache-Control "max-age=2592000, public"
</FilesMatch>

# Force .py files to download (Dreamhost would try to execute them as CGI)
<FilesMatch "\.py$">
    SetHandler default-handler
    Header set Content-Disposition "attachment"
</FilesMatch>

# Caching for CSS/JS (7 days)
<FilesMatch "\.(css|js)$">
    Header set Cache-Control "max-age=604800, public"
</FilesMatch>
```

`DirectoryIndex` and the rewrite rules make `/folder` redirect to `/folder/` and make `/folder/` serve `index.html`; equivalent behavior is important because the site links to clean directory URLs. `Header` rules provide optional image/CSS/JS cache lifetimes. The `.py` rule prevents DreamHost CGI execution and forces downloads; on a static server Python must never execute, and access to source/scripts should be restricted. `.htaccess` is Apache-specific and is **not** interpreted by other static servers; any required behavior needs explicit equivalents.

**Task 5: live redirects (HEAD, no redirects followed).**

```text
http://strulovitz.org/      301 Location: https://strulovitz.org/
http://www.strulovitz.org/  301 Location: https://strulovitz.org/
https://strulovitz.org/     200 (no Location)
https://www.strulovitz.org/ 200 (no Location)
http://learnime.com/        301 Location: https://learnime.com/
http://www.learnime.com/    301 Location: https://learnime.com/
https://learnime.com/       200 (no Location)
https://www.learnime.com/   200 (no Location)
http://peaktogether.me/       301 Location: https://peaktogether.me/
http://www.peaktogether.me/   301 Location: https://peaktogether.me/
https://peaktogether.me/      200 (no Location)
https://www.peaktogether.me/  200 (no Location)
```

**Recommendation (not implemented):** Use **Caddy** later as the static web server, run by user `nir` on three separate high-numbered loopback endpoints (`127.0.0.1`, e.g. ports 8081-8083). It is not installed; installation/configuration would require a separate approval. This avoids Apache's port 80 and its `www-data` inability to traverse `/home/nir` (mode 700), works the same way on Debian 13 and Linux Mint 22, and can serve each site's own files with explicit directory-index and content-type rules. Configure access restrictions so `.git`, private files, and Peak Together's Python source are not exposed; replicate any needed `.htaccess` behavior explicitly. HTTPS and public-domain redirects are currently outside this loopback-server proposal. Nothing was installed, built, deployed, stopped, or reconfigured.
