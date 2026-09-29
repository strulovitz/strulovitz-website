From Claude (manager). Keep it short and cheap. Save this prompt in hosting-migration/ as before.

GOAL: Nir wants 2 clickable icons, "Websites ON" and "Websites OFF", both in the applications menu AND on the desktop background. No terminal typing needed.

1. Detect the desktop environment (echo $XDG_CURRENT_DESKTOP) and the real desktop folder (xdg-user-dir DESKTOP; it may be localized, so don't assume ~/Desktop).
2. Create a reusable installer in the repo: hosting/bin/install-launchers (so the Desktop PC can run the same thing later). It must:
   - Write 2 .desktop files into ~/.local/share/applications/ (sites-on.desktop, sites-off.desktop) and copy them into the desktop folder.
   - Use ABSOLUTE paths in Exec (expand $HOME at install time; a launcher does not read ~/.local/bin from PATH reliably).
   - Run in a visible terminal window, and at the end show "Press Enter to close" so Nir can read the result (e.g. Exec=<terminal> -e bash -c '...; read -p "Press Enter to close"'). Pick the terminal that actually exists on this system, or use Terminal=true if that works here. TEST that the window really opens.
   - Icons: standard theme icons (e.g. media-playback-start / media-playback-stop), with Names "Websites ON" and "Websites OFF".
   - chmod +x both files. On GNOME, also mark the desktop copies trusted: gio set <file> metadata::trusted true.
   - Be safe to run twice (overwrite its own files only).
3. If the DE is GNOME: GNOME doesn't show desktop icons by default. Check whether the "Desktop Icons NG (DING)" extension is installed/enabled. If it's missing, you may apt install ONLY gnome-shell-extension-desktop-icons-ng and enable it for user nir (gnome-extensions enable ding@rastersoft.com). Nir may need to log out and back in; tell him plainly. Change nothing else. For other DEs (KDE/XFCE/Cinnamon), desktop icons work natively.
4. Run install-launchers. Test by launching both .desktop files (gio launch <file> or gtk-launch). IMPORTANT: finish in the ON state (sites-status must show all 3 active), because the websites are live from this laptop.
5. Update hosting/README.md: one short section about the icons.
6. APPEND this section to the end of hosting-migration/HANDOFF-for-desktop.md (don't change the rest):

## Extra request from Nir (added from the laptop session)
Nir wants 2 clickable icons, "Websites ON" and "Websites OFF", in the applications menu AND on the desktop background, so he never needs the terminal. This is already done on the laptop via hosting/bin/install-launchers (in the repo). On the Desktop (Linux Mint 22, Cinnamon, which shows desktop icons natively): after the setup works, have the worker run hosting/bin/install-launchers, fix anything Mint-specific (terminal = gnome-terminal or x-terminal-emulator; it may need "Allow launching" / trusted), and test both icons. Keep hosting ON the correct PC at the end of the test.

7. Commit + push (no secrets). Reply in max 10 lines, including exactly what Nir must do (e.g. log out/in, or right-click the icon -> "Allow Launching").  
