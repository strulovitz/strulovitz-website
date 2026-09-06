#!/usr/bin/env python3
"""
deploy_windows.py -- the same deploy ritual as ops/deploy.sh, working on
Windows, where lftp does not exist. The password is read from the SFTP_PASS
environment variable and is never written to any file.

    python ops/deploy_windows.py check     look at the server, change nothing
    python ops/deploy_windows.py upload    folder first, root pages, pointer LAST
"""

import json
import os
import stat as statmod
import sys
import time

import paramiko

REPOSITORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORTS = os.path.join(REPOSITORY, "exports")


def load_env():
    values = {}
    with open(os.path.join(REPOSITORY, ".env"), encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
    return values


def connect(env):
    password = os.environ.get("SFTP_PASS")
    if not password:
        raise SystemExit("SFTP_PASS is not set in the environment.")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(env["FTP_HOST"], port=22, username=env["FTP_USER"],
                   password=password, look_for_keys=False, allow_agent=False)
    return client


def remote_isdir(sftp, path):
    try:
        return statmod.S_ISDIR(sftp.stat(path).st_mode)
    except FileNotFoundError:
        return False


def check(env):
    client = connect(env)
    sftp = client.open_sftp()
    root = env["FTP_REMOTE_WEB_ROOT"]
    print("home listing:")
    for entry in sorted(sftp.listdir(".")):
        marker = "/" if remote_isdir(sftp, entry) else ""
        print("  " + entry + marker)
    if not remote_isdir(sftp, root):
        raise SystemExit(f"'{root}' is not a folder on the server.")
    pointer = sftp.open(f"{root}/pointer.json").read().decode().strip()
    print(f"live pointer says: {json.loads(pointer)['live']}")
    print("versions on the server:")
    for entry in sorted(sftp.listdir(root)):
        if remote_isdir(sftp, f"{root}/{entry}") and entry.startswith("v"):
            print("  " + entry)
    sftp.close()
    client.close()


def upload_dir(sftp, local_root, remote_root):
    total = 0
    count = 0
    for base, _dirs, files in os.walk(local_root):
        relative = os.path.relpath(base, local_root).replace(os.sep, "/")
        remote_dir = remote_root if relative == "." else f"{remote_root}/{relative}"
        if not remote_isdir(sftp, remote_dir):
            sftp.mkdir(remote_dir)
        for name in sorted(files):
            local_file = os.path.join(base, name)
            sftp.put(local_file, f"{remote_dir}/{name}")
            total += os.path.getsize(local_file)
            count += 1
            if count % 25 == 0:
                print(f"  {count} files, {total / (1 << 20):.0f} MB so far", flush=True)
    return count, total


def find_previous_version(current):
    """The newest version folder in exports/ other than the one being shipped."""
    names = [n for n in os.listdir(EXPORTS)
             if n.startswith("v") and os.path.isdir(os.path.join(EXPORTS, n))
             and n != current]
    return max(names) if names else None


def files_differing(previous, current):
    """Relative paths of files that changed or are new, by real content hash.

    This is the whole trick DECISION 23 asks for: compare the new build with
    the previous one file by file, so the upload carries only the difference.
    """
    import hashlib
    def manifest(folder):
        result = {}
        for base, _dirs, files in os.walk(folder):
            for name in files:
                path = os.path.join(base, name)
                rel = os.path.relpath(path, folder).replace(os.sep, "/")
                with open(path, "rb") as handle:
                    result[rel] = hashlib.sha256(handle.read()).hexdigest()
        return result
    old = manifest(os.path.join(EXPORTS, previous))
    new = manifest(os.path.join(EXPORTS, current))
    return sorted(rel for rel, digest in new.items() if old.get(rel) != digest)


def server_side_copy(client, root, previous, version):
    """Copy the previous folder into the new name ON THE SERVER, so the
    hundreds of unchanged files never cross the wire. Returns True on success.
    Any failure means the caller falls back to a full upload - correctness
    first, bytes second."""
    try:
        _stdin, stdout, _stderr = client.exec_command(
            f"cp -r '{root}/{previous}' '{root}/{version}'", timeout=60)
        if stdout.channel.recv_exit_status() != 0:
            return False
        stat = sftp_stat_quiet(client, f"{root}/{version}/tesseract.html")
        return stat is not None
    except Exception:
        return False


def sftp_stat_quiet(client, path):
    try:
        sftp = client.open_sftp()
        return sftp.stat(path)
    except Exception:
        return None


def upload_changed(changed, version, sftp, root):
    total = 0
    for rel in changed:
        local = os.path.join(EXPORTS, version, rel.replace("/", os.sep))
        remote_dir = f"{root}/{version}" if "/" not in rel else \
            f"{root}/{version}/{rel.rsplit('/', 1)[0]}"
        if not remote_isdir(sftp, remote_dir):
            sftp.mkdir(remote_dir)
        sftp.put(local, f"{root}/{version}/{rel}")
        total += os.path.getsize(local)
        print(f"  {rel}", flush=True)
    return len(changed), total


def upload(env):
    with open(os.path.join(EXPORTS, "pointer.json"), encoding="utf-8") as handle:
        version = json.load(handle)["live"]
    client = connect(env)
    sftp = client.open_sftp()
    root = env["FTP_REMOTE_WEB_ROOT"]

    print(f"STEP 1 of 3  preparing the folder {version} ...", flush=True)
    started = time.time()
    previous = find_previous_version(version)
    if previous is None:
        print("  no previous version folder found locally - full upload", flush=True)
        count, total = upload_dir(sftp, os.path.join(EXPORTS, version), f"{root}/{version}")
        print(f"  done: {count} files, {total / (1 << 20):.0f} MB in {time.time() - started:.0f}s", flush=True)
    else:
        changed = files_differing(previous, version)
        print(f"  local diff vs {previous}: {len(changed)} file(s) differ or are new", flush=True)
        if server_side_copy(client, root, previous, version):
            print("  server-side copy done - the unchanged files never cross the wire", flush=True)
            count, total = upload_changed(changed, version, sftp, root)
            print(f"  then {count} changed file(s), {total / (1 << 20):.2f} MB in {time.time() - started:.0f}s", flush=True)
        else:
            print("  server-side copy not possible - uploading the full folder (correctness first)", flush=True)
            count, total = upload_dir(sftp, os.path.join(EXPORTS, version), f"{root}/{version}")
            print(f"  done: {count} files, {total / (1 << 20):.0f} MB in {time.time() - started:.0f}s", flush=True)

    print("STEP 2 of 3  uploading the root pages ...", flush=True)
    # DECISION 23: upload every root page and the lightbox - they are small and
    # they all changed with this milestone - but NEVER the images folder. The
    # pictures are already on the server and re-sending 311 MB of them for a
    # text change is exactly the mistake Nir stopped on 2026-09-06.
    root_files = sorted(
        name for name in os.listdir(EXPORTS)
        if os.path.isfile(os.path.join(EXPORTS, name))
        and name != "pointer.json"
        and (name.endswith(".html") or name.endswith(".js"))
    )
    for name in root_files:
        sftp.put(os.path.join(EXPORTS, name), f"{root}/{name}")
        print(f"  {name}", flush=True)

    print("STEP 3 of 3  uploading pointer.json - this is the moment it goes live ...", flush=True)
    sftp.put(os.path.join(EXPORTS, "pointer.json"), f"{root}/pointer.json")
    print(f"PUBLISHED. {version} is live at https://www.strulovitz.org/")
    sftp.close()
    client.close()


def main():
    env = load_env()
    action = sys.argv[1] if len(sys.argv) > 1 else "check"
    if action == "check":
        check(env)
    elif action == "upload":
        upload(env)
    else:
        raise SystemExit("usage: python ops/deploy_windows.py check|upload")


if __name__ == "__main__":
    main()
