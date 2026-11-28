"""Small self-checks for the line, run with: uv run python tests/selftest.py

They exist because a real bug shipped: an empty but successful command (a
clean "git status") was read as a failure, and am doctor then said "no git
repository found". A test is cheaper than that mistake.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from attract_line import doctor, pins  # noqa: E402

fails = []


def check(name, ok, said=""):
    print(("  ok   " if ok else "  FAIL ") + name + ("" if ok else "  " + said))
    if not ok:
        fails.append(name)


print("THE RUN HELPER")
check("a successful silent command returns empty text, not None",
      doctor.run(["true"]) == "", repr(doctor.run(["true"])))
check("a failing command returns None",
      doctor.run(["false"]) is None)
check("a command that does not exist returns None",
      doctor.run(["this-command-does-not-exist-anywhere"]) is None)
check("git status on a clean folder returns empty text, not None",
      doctor.run(["git", "-C", str(doctor.repo_root()), "status", "--porcelain", "--", "nope"]) == "")

print("THE PINS PARSER")
p = pins.read()
check("every name has a value", all(isinstance(v, str) and v for v in p.values()), repr(p))
check("PHP is split by PC", "PHP (desktop)" in p and "PHP (laptop)" in p, repr(list(p)))
check("Syncthing is 2.1.7", p.get("Syncthing") == "2.1.7", repr(p.get("Syncthing")))
check("no pin says 'latest'", all("latest" not in v.lower() for v in p.values()))

print("THE MATCH RULE")
check("exact pin matches itself", doctor.matches("2.1.7", "2.1.7"))
check("a series pin accepts a patch", doctor.matches("11.8", "11.8.2"))
check("a pin rejects another version", not doctor.matches("2.1.7", "1.30.0"))
check("a pin rejects a look-alike", not doctor.matches("8.3", "8.30"))

print()
if fails:
    print(str(len(fails)) + " check(s) failed.")
    sys.exit(1)
print("All self-checks passed.")
