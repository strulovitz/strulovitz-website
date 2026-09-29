Phase 5 (Desktop, mint-desktop, Linux Mint 22 Cinnamon). Same HARD RULES. You may save this prompt to GitHub as usual.

1. Run hosting/bin/install-launchers from ~/strulovitz-website. It must create "Websites ON" and "Websites OFF" in the applications menu AND on the desktop background (~/Desktop, or `xdg-user-dir DESKTOP`).
2. Fix anything Mint-specific: the terminal (gnome-terminal or x-terminal-emulator, whichever exists), chmod +x on the desktop files, and mark them trusted (`gio set <file> metadata::trusted true`) so Cinnamon doesn't show "Untrusted launcher". If you change install-launchers, it MUST keep working on the laptop (Debian 13). Commit and push only those changes.
3. Test by launching each exactly the way a click does (`gtk-launch <desktop-file-name>`): first OFF, then check that sites-status shows everything stopped; then ON, then check that https://strulovitz.org/hosted-by?t=$(date +%s) says "Served by mint-desktop".
4. END STATE: the sites must be ON.

Reply with a SHORT report (max 8 lines).
