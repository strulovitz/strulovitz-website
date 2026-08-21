RUNBOOK: THE SECRET SCANNER
===========================

WHAT THIS PROTECTS AGAINST

A password or an API key accidentally saved into the project's git history.
This matters more than it sounds. Once a secret is committed, it stays in the
history forever, even if the line is deleted afterwards, and anyone who can
see the repository can use it to spend Nir's money.

So the defence is simple: never let it in. See bible/part-07.md section 7.4.


WHEN TO USE THIS RUNBOOK

1. You are setting the project up on a fresh machine and need the guard back.
2. Somebody reports that the guard did not fire when it should have.
3. You want to check some files by hand before sending them anywhere.


BEFORE YOU START

Nothing special. The scanner is a small script with no dependencies at all,
so it works on any Linux machine with bash and grep.


STEPS: INSTALLING THE GUARD

The guard works by asking git to run the scanner every time somebody commits.

1. Go to the project folder:
       cd /home/nir/strulovitz-website

2. Create the hook file:
       cat > .git/hooks/pre-commit <<'END'
       #!/usr/bin/env bash
       exec "$(git rev-parse --show-toplevel)/ops/check-secrets.sh"
       END

3. Make it runnable:
       chmod +x .git/hooks/pre-commit


HOW YOU KNOW IT WORKED

1. Make a harmless commit. Before the commit goes through, you should see a
   line beginning "Secret scanner: checking" and then "SECRET SCANNER: CLEAN".

2. Test that it actually bites. The command below BUILDS a fake key as it
   runs, rather than spelling one out, so that this page does not itself
   contain something the scanner has to complain about:

       printf 'OPENROUTER_API_KEY=%s\n' "sk-or-v1-$(printf 'x%.0s' {1..30})" > leaktest.txt
       git add leaktest.txt
       git commit -m "this should be refused"

   The commit must be REFUSED, naming the file and the line number. Then clean
   up:
       git reset leaktest.txt && rm leaktest.txt

   (This is a real lesson worth keeping: when this very runbook was first
   written with a fake key spelled out in full, the scanner refused to let it
   be committed. Writing about secrets is enough to trip a good guard.)

   A guard that has never been tested is not a guard. Test it once.


STEPS: CHECKING FILES BY HAND

To check what git is about to commit:
    ops/check-secrets.sh

To check particular files:
    ops/check-secrets.sh some/file.txt another/file.json


WHAT IT WILL AND WILL NOT SAY

It prints the file name, the line number, and what kind of secret it thinks it
found. It never prints the secret itself, because that would just move the
leak into the terminal history and the log files.


IF IT FAILS

Symptom: it complains about a line that is obviously harmless, for example a
long example value inside documentation.
    This is a false alarm, and false alarms are the price of a guard that
    catches real leaks. Two options. The clean one is to shorten or obviously
    fake the example value. The quick one is the emergency bypass below.

Symptom: it says "this is not a git repository".
    You are in the wrong folder. Go to /home/nir/strulovitz-website first.

Symptom: the commit went through without any scanner message at all.
    The hook is missing or not executable. Redo the installation steps above,
    and do not forget the chmod line.


THE EMERGENCY BYPASS

    git commit --no-verify -m "your message"

Use it only when you are certain the finding is a false alarm. If you find
yourself using it often, the honest fix is to add the exception into the
scanner rather than to get into the habit of ignoring the guard.


ROLLBACK

To remove the guard entirely:
    rm /home/nir/strulovitz-website/.git/hooks/pre-commit

Note that git hooks are not part of the repository, so they do not travel when
the project is copied to another machine. That is why this runbook exists: on
a new machine, the guard has to be installed again by hand, once.
