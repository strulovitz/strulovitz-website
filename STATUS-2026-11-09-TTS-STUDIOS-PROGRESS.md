# STATUS 2026-11-09 (13:55): TTS studios on desktop-linux, exact progress

Companion to HANDOFF-2026-11-09-DESKTOP-LINUX-TTS-STUDIOS.md. This file is the CURRENT truth.

## RULES FROM NIR (must obey)
- Work GRADUALLY. Before each step, tell Nir in plain words what you are about to do. After each step, report.
- NEVER run anything that can freeze or stick the PC (big compiles, many parallel jobs, huge RAM use). If unsure, ask first.
- Explicit "go" from Nir before every download, install, compile, or sudo step.
- NEVER touch his website (Caddy + Cloudflare Tunnel). He had to shut it down after the freeze at 13:37; its state changes, so never assume it. Do not start or stop it unless he says.
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
| Zonos (~/zonos, ~19G) | DONE: env, fast parts built (sm_89), espeak-ng (apt), models in ~/zonos/hf, torchcodec 0.11.1+cu128 | start, stop, folder, guide, outputs (Desktop + menu) | DONE, headless test of both models OK; GUI click-test by Nir pending |
| Voicebox (~/voicebox, ~60G) | DONE: fresh reinstall, web mode (dev-web style, no Docker/Rust/Tauri), models in ~/voicebox/hf | start, stop, folder, guide, outputs (Desktop + menu) | DONE, headless checks OK; GUI click-test by Nir pending |

Nothing is running now except normal desktop + neo4j. Website state: not mine to touch, ask Nir.

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

## UPDATE 14:36 (Zonos fast parts, Option A chosen by Nir)
- Cause of the 36-min compile: causal-conv1d and mamba-ssm setup.py hardcode 5-9 GPU archs. RTX 4070 Ti = 8.9. I patched MY copies in ~/zonos/src to build only sm_89 (flash-attn: FLASH_ATTN_CUDA_ARCHS=89 plus a patched "89" branch).
- Safe build script: ~/zonos/build-one.sh <name> <srcdir> (1 job, nice 19, systemd-run MemoryMax=20G, logs BUILD OK / BUILD FAILED). Logs: ~/zonos/build-*.log.
- causal-conv1d: BUILD OK (2m45s, ~1GB RAM), import test OK on GPU.
- mamba-ssm: BUILD OK (~6 min), import test OK on GPU.
- flash-attn: building since ~14:34, 73 pieces, ~1-1.5 min each, est 70-110 min. RAM ~10GB used total, safe.
- Everything lives inside ~/zonos (uninstall = delete the folder; only external thing used is ~/drama3/cuda).
- NEXT: when flash-attn says BUILD OK, import-test it, then a real Zonos generation test, then make Zonos start/stop/folder/guide/outputs icons (pattern: ~/drama3 icons), then Voicebox.

## UPDATE 18:15 (Zonos DONE)
- flash-attn BUILD OK 16:07 (1h34m). All 3 fast parts import-tested on the GPU.
- Icons made: ~/Desktop/zonos-*.desktop and ~/.local/share/applications; scripts ~/zonos/start-zonos.sh / stop-zonos.sh (port 7860, 127.0.0.1 only, HF_HOME=~/zonos/hf).
- espeak-ng installed with apt (needed sudo). Models downloaded to ~/zonos/hf (transformer, hybrid, descript/dac_44khz).
- torchaudio 2.11 needed torchcodec: the PyPI one (0.17, cuda13) broke; installed 0.11.1+cu128 from download.pytorch.org/whl/cu128.
- Headless test (~/zonos/test-zonos.py): both models generated audio (outputs/test-transformer.wav, test-hybrid.wav). Capped build/test runs with systemd-run MemoryMax=30G.
- NEXT: Voicebox (~/voicebox partial). Read ~/voicebox/install-vb.log first. Same rules: gradual, say each step, caps on anything heavy, explicit go for downloads/compiles/sudo.

## UPDATE 19:55 (Voicebox DONE)
- Old half install deleted, fresh install in ~/voicebox (script install-voicebox.sh, log install-vb.log, "INSTALL ALL OK"). The earlier failure was a network glitch fetching linacodec from GitHub; retry worked.
- Web mode only (Nir's decision): backend uvicorn on 127.0.0.1:17493 + vite web on 127.0.0.1:5173. No Docker, no Rust, no Tauri, no just. Scripts: ~/voicebox/start-voicebox.sh, stop-voicebox.sh.
- Models in ~/voicebox/hf (HF_HOME): whisper-large (= openai/whisper-large-v3, highest Whisper in Voicebox), qwen-tts-1.7B, qwen-custom-voice-1.7B, qwen-voice-design-1.7B, luxtts, chatterbox-tts (multilingual, Hebrew), chatterbox-turbo, tada-1b, tada-3b-ml. NOT installed by Nir's choice: Qwen 0.6B, Kokoro (OmniVoice not requested).
- UPSTREAM BUG: Voicebox generic model-download route (POST /models/download) for TADA always loads 1B, so tada-3b-ml never downloads that way. Worked around by huggingface_hub snapshot_download("HumeAI/tada-3b-ml") with HF_HOME=~/voicebox/hf (download-tada3b.py).
- Trap: the download route also LOADS each model into VRAM (it stacked to 10.9GB); unload with POST /models/unload and /models/<name>/unload after each.
- Checks: web 200, backend sees RTX 4070 Ti CUDA, Whisper Large transcribed the Zonos test wav correctly. Nothing is running now.
- Icons made (5) with the same pattern as Zonos. All three new studios: one big AI app at a time on the 12GB card.
- NEXT: Nir click-tests Start/STOP icons for Zonos and Voicebox. Nothing else pending for the TTS studios.

## UPDATE 20:30 (Voicebox: TADA and LuxTTS removed on Nir's request)
- Deleted from ~/voicebox/hf/hub: HumeAI tada-1b, tada-3b-ml, tada-codec, YatharthS LuxTTS, unsloth Llama-3.2-1B mirror, facebook wav2vec2-large (24G freed).
- Uninstalled from backend/venv: hume-tada, Zipvoice, linacodec and the 21 packages only they needed (computed with a dependency check; lhotse, vocos, tensorboard, piper-phonemize, etc.).
- Verified after: chatterbox (tts, mtl_tts, tts_turbo), qwen_tts, kokoro package, backend.main all import OK. pip check complaints about chatterbox-tts/omnivoice pins are expected (installed --no-deps by upstream design).
- Reproducible install now uses ~/voicebox/requirements-no-lux-tada.txt (install-voicebox.sh updated).
- The Voicebox app UI still lists TADA/LuxTTS (upstream code) but they are not installed. Do not click download on them.
- Chatterbox facts (from the Voicebox README, line ~147): ONLY Chatterbox Turbo interprets inline tags like [laugh]/[sigh]; Multilingual reads them as text; Multilingual has an exaggeration/cfg_weight emotion knob instead (backend/backends/chatterbox_backend.py).

## UPDATE 20:55 (Voicebox: Kokoro removed too, Nir's request)
- Uninstalled kokoro, misaki and the packages only they needed (addict, loguru, spacy tree, en-core-web-sm, unidic-lite, fugashi, mojimoji, pypinyin, ordered-set...). No Kokoro model had been downloaded.
- Kept both Chatterbox versions (Nir's decision). Verified after: chatterbox-turbo and chatterbox-tts load on the GPU via the backend; chatterbox/qwen/backend imports OK. Everything stopped afterwards (GPU idle).
- ~/voicebox/requirements-no-lux-tada.txt no longer lists Kokoro/misaki either.
- Final Voicebox engine set: Qwen TTS 1.7B, Qwen CustomVoice 1.7B, Qwen VoiceDesign 1.7B, Chatterbox Multilingual, Chatterbox Turbo, Whisper Large v3.
