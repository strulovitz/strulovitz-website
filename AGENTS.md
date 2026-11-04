# NIR'S RULE FOR EVERY AGENT (4 Nov 2026) — A WEBSITE MUST BE COMPLETE ON GITHUB

Nir serves ALL his websites from TWO computers, one at a time: the laptop and
the desktop (the desktop half of the time or more). Each computer serves what
it pulled from GitHub. So everything a website serves (pages, data, images)
must be committed AND pushed. Never hide website files in `.gitignore`. Never
say "pushed" or "done" until you have checked that GitHub really has it
(`git status --porcelain --ignored <site folder>` empty, `git log
origin/<branch>..` empty, and after a data change a fresh `git clone` works).
Push only what Nir asks for, by name; never secrets or tokens. Full rule:
github.com/strulovitz/claude-memory feedback_website_complete_on_github.md and
second-opinion BIBLE Part 9 section 9.S (LAW 16).

# NIR'S ONE RULE FOR EVERY AGENT — UPLOAD ONLY WHAT CHANGED

When pushing to GitHub, or uploading to the live server, or deploying:

Look at what ACTUALLY changed, and send ONLY that.

Never re-send files that are already there and unchanged. Not images, not
folders, not "to be safe". Unchanged files cost money (the agent burns
tokens watching them) and they risk breaking a working site.

Before any push or upload, say what you are about to send and how many
files it is. If the number looks bigger than the change you made, stop and
check before sending.

Everything else stays as always: emojis in every reply, the important
thing first, plain words.
