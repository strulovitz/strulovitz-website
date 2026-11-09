# STATUS 2026-11-09 (13:55): TTS studios on desktop-linux, exact progress

Companion to HANDOFF-2026-11-09-DESKTOP-LINUX-TTS-STUDIOS.md. This file is the CURRENT truth.

## RULES FROM NIR (must obey)
- Work GRADUALLY. Before each step, tell Nir in plain words what you are about to do. After each step, report.
- NEVER run anything that can freeze or stick the PC (big compiles, many parallel jobs, huge RAM use). If unsure, ask first.
- Explicit "go" from Nir before every download, install, compile, or sudo step.
- NEVER touch his website (Caddy + Cloudflare Tunnel). He shut it down himself after the freeze. It is OFF. Do not turn it on unless he says.
- Short messages, emojis on every line, important thing last. Do only what he says.

## WHAT HAPPENED (the freeze)
- At 13:00 build-fast.sh in ~/zonos started compiling flash-attn, mamba-ssm, causal-conv1d from source with MAX_JOBS=6.
- It ran ~36 min (its tmp folder was last written 13:36). The PC froze, Nir had to shut down his website and reboot at 13:37.
- Cause: heavy 6-job CUDA compile without warning Nir. It never finished. No FASTDONE.
- It was Zonos, NOT Drama 3. Drama 3 is finished.

## STATE OF EACH STUDIO (verified read-only after reboot)
| Studio | Installed | Icons (Desktop) | Status |
|---|---|---|---|
| Drama 3 (~/drama3, 45G) | yes | start, stop, folder, guide, outputs | DONE |
| VoxCPM2 (~/voxcpm2, 12G) | yes | start, stop, folder, guide, outputs | DONE |
| Zonos (~/zonos, 11G) | base env + torch 2.11+cu128 OK; fast parts (flash-attn, mamba-ssm, causal-conv1d) NOT built | none | INCOMPLETE |
| Voicebox (~/voicebox, 283M) | partial (app, bun, env, install-vb.log) | none | INCOMPLETE |

Nothing is running now except normal desktop + neo4j. Website is OFF (by Nir).

## WHAT ZONOS NEEDS
- The 3 packages are CUDA code with no prebuilt wheel for this torch + RTX 4070 Ti, so they must be compiled. Needed only for Zonos Hybrid mode; Transformer mode should work without them (verify in ~/zonos/app/README.md before claiming).
- Option A (safe): compile with MAX_JOBS=2 under `nice -n 19`, in small watched steps, check RAM with free -h, with Nir's go.
- Option B: skip the compile, finish Zonos in Transformer mode only.
- Nir has NOT chosen yet. Ask him.
- Env: ~/zonos/env (uv venv), CUDA toolkit at ~/drama3/cuda, TMPDIR=~/zonos/tmp (may hold junk from the killed build, ask before deleting).

## NEXT STEPS (one at a time, each after Nir's go)
1. Nir chooses Option A or B for Zonos.
2. Finish Zonos, make start/stop/folder/guide/outputs icons like Drama 3 (copy the pattern from ~/.local/share/applications/drama3-*.desktop and ~/drama3/start-drama3.sh, stop-drama3.sh).
3. Check Voicebox install state (read install-vb.log), finish it, make its icons.
4. Test each studio ONE at a time (one big AI thing at a time on the 12 GB card).
5. Update this file after every step and push.
