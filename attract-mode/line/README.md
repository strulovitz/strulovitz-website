# The line (Part 01, section 1.10)

One entry point, so that a cheap model never has to guess which script to run.

    cd attract-mode/line
    uv run am doctor

`am doctor` checks this PC and prints a plain-language report: the versions
against `config/pins`, the ports, whether Moodle answers, whether Git is clean
and up to date, whether Syncthing sees the other PC, how old the newest
hand-over is, and the free space. Every failure is one sentence saying what to
do.

The other words (`build`, `publish`, `today`) are named by later Parts and say
so plainly until they exist.

Both PCs build this environment from the same `uv.lock` in Git, so both run the
same Python (Part 01, section 1.8).
