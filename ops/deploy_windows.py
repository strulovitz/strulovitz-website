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


def files_differing_remote(sftp, root, previous, current):
    """The exact set of files to upload, computed without moving the big
    bytes: the server's live folder is listed (names and sizes only), the new
    local build is hashed, and every file that is missing, bigger/smaller, or
    a text file whose size happens to match but whose content differs is
    marked for upload. Binary files with identical sizes are treated as
    identical - for pictures that is certain for all practical purposes.
    This is DECISION 23 in code: only the difference crosses the wire."""
    import hashlib
    import stat as statmod
    text_suffixes = (".html", ".json", ".js", ".css", ".txt", ".svg", ".md", ".xml")
    remote_sizes = {}
    def walk(path, prefix):
        for entry in sftp.listdir_attr(path):
            remote_path = f"{path}/{entry.filename}"
            rel = f"{prefix}{entry.filename}" if prefix == "" else f"{prefix}/{entry.filename}"
            if statmod.S_ISDIR(entry.st_mode):
                walk(remote_path, rel)
            else:
                remote_sizes[rel] = entry.st_size
    walk(f"{root}/{previous}", "")

    delta = []
    for base, _dirs, files in os.walk(os.path.join(EXPORTS, current)):
        for name in files:
            local_path = os.path.join(base, name)
            rel = os.path.relpath(local_path, os.path.join(EXPORTS, current)).replace(os.sep, "/")
            local_size = os.path.getsize(local_path)
            if rel not in remote_sizes:
                delta.append(rel)
            elif remote_sizes[rel] != local_size:
                delta.append(rel)
            elif rel.lower().endswith(text_suffixes):
                remote_hash = hashlib.sha256(sftp.open(f"{root}/{previous}/{rel}").read()).hexdigest()
                with open(local_path, "rb") as handle:
                    local_hash = hashlib.sha256(handle.read()).hexdigest()
                if remote_hash != local_hash:
                    delta.append(rel)
    return sorted(delta)


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
    # DECISION 23: the delta is computed against the folder the SERVER is
    # actually serving right now (its live pointer), not against whichever
    # local build happens to be newest. A build can exist locally and never
    # have been uploaded - that is exactly what happened with v2026-09-04-h.
    # And because the old local exports folders get cleaned up over time, the
    # comparison reads the server's own listing instead of trusting a local
    # copy: missing, resized, and hash-differing text files go up; everything
    # else stays where it is.
    remote_live = json.loads(
        sftp.open(f"{root}/pointer.json").read().decode().strip())["live"]
    if remote_live == version:
        print(f"  the server is already live on {version} - uploading it in full to be safe", flush=True)
        count, total = upload_dir(sftp, os.path.join(EXPORTS, version), f"{root}/{version}")
        print(f"  done: {count} files, {total / (1 << 20):.0f} MB in {time.time() - started:.0f}s", flush=True)
        return
    changed = files_differing_remote(sftp, root, remote_live, version)
    print(f"  server is live on {remote_live}; exact delta to upload: {len(changed)} file(s)", flush=True)
    if server_side_copy(client, root, remote_live, version):
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


def upload_root(env):
    """Upload ONLY the small root pages and the lightbox.

    This is the deploy for milestones that change the pages but not the
    magazine application itself (menu changes, new pages, new text). No
    version folder, no pointer upload: the tesseract app keeps running from
    whichever folder the server's pointer already names, so nothing that is
    already on the server crosses the wire. DECISION 23 in its plainest form.
    """
    client = connect(env)
    sftp = client.open_sftp()
    root = env["FTP_REMOTE_WEB_ROOT"]
    live = json.loads(sftp.open(f"{root}/pointer.json").read().decode().strip())["live"]
    print(f"the server's magazine application stays on {live} - untouched", flush=True)
    root_files = sorted(
        name for name in os.listdir(EXPORTS)
        if os.path.isfile(os.path.join(EXPORTS, name))
        and name != "pointer.json"
        and (name.endswith(".html") or name.endswith(".js")))
    total = 0
    for name in root_files:
        local = os.path.join(EXPORTS, name)
        sftp.put(local, f"{root}/{name}")
        total += os.path.getsize(local)
        print(f"  {name}  ({os.path.getsize(local) / 1024:.0f} KB)", flush=True)
    print(f"PUBLISHED {len(root_files)} root files, {total / (1 << 10):.0f} KB total. "
          f"Version folders and pointer: NOT touched.", flush=True)
    sftp.close()
    client.close()


def main():
    env = load_env()
    action = sys.argv[1] if len(sys.argv) > 1 else "check"
    if action == "check":
        check(env)
    elif action == "upload":
        upload(env)
    elif action == "upload_root":
        upload_root(env)
    else:
        raise SystemExit("usage: python ops/deploy_windows.py check|upload|upload_root")


if __name__ == "__main__":
    main()
