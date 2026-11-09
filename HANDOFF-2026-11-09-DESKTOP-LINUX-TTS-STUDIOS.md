# HANDOFF 2026-11-09: text-to-speech studios on desktop-linux (Linux Mint 22, RTX 4070 Ti 12 GB)

Written by the OpenCode session on Nir's DESKTOP Linux PC, for the NEXT OpenCode session on this same PC.
This file REPLACES the idea of following the laptop handoff `HANDOFF-2026-11-07-NIGHT-LINUX-TTS-AND-LATENTSYNC.md`
on this machine. That older file was written for the laptop (RTX 5090, 24 GB VRAM); read it only for the
icon/folder pattern. Everything below is verified for THIS PC unless marked UNVERIFIED.
Nothing in this file contains a password. Nir typed his sudo password in chat today; it is NOT recorded anywhere.
If a step needs sudo, say so plainly and ask him for it again.

## 0. HOW TO TREAT NIR (read first, it matters more than any technical detail)

Nir was angry several times today. Rules, all binding:
- DO ONLY WHAT HE SAYS. He gives an explicit "go" before any download, install, compile or sudo step.
  A plan he agreed in principle is NOT a go. Ask once, plainly: "Shall I start with step N?"
- TALK TO HIM. Never take a strange indirect route to avoid asking. If you need his root password, if you
  need to compile something, if you need a big download: SAY SO FIRST in plain words and wait.
  (Today I installed CUDA "without sudo, into a folder" to avoid asking him. He was furious: "stop being an asshole,
  talk to me". Do not repeat that.)
- HIGH QUALITY EVERYWHERE. When he wants a model, give the best-quality file that fits; never silently pick the
  smallest/lowest one (I picked Q2 on my own; he exploded). Never lecture him about what "fits his GPU".
- ONE SCREEN per reply. He cannot scroll in OpenCode on Linux. Short, simple words. Important thing LAST.
- EMOJIS in every chat line (permanent rule). NO emojis in files, commits, or memory.
- Explain each step in plain words BEFORE doing it, and report during long steps (check every ~45 s, say elapsed).
- When he says stop: stop, zero tool calls. When he says "delete everything": delete everything INCLUDING background
  processes, then verify with ls and ps and tell him disk free before/after.
- Do not cause him worry: report caveats once, calmly, with the good news. He said "is causing me worry your hobby?".
- Do not use sub-agents. Do not use the question tool. Never use `pkill -f` or `pgrep -f` with a pattern that appears in
  your own command line (it kills your own shell). Use `pgrep -x name` or exact PIDs.
- Never run a single tool call longer than ~60 s. Start long jobs with `setsid nohup ... &` and poll in short steps.
- If a tool call is aborted by Nir, assume background jobs may still be running; check with `ps aux` before claiming anything.
- Never write legal-risk language about licences into any file, commit or message that touches GitHub.
- AGENTS.md at /home/nir/AGENTS.md is LOCAL ONLY, never commit it. Push only files by name, never `git add -A`.

## 1. STATE OF THE MACHINE (verified 2026-11-09, ~10:30 local)

- Linux Mint 22 (Ubuntu 24.04 base), NVIDIA GeForce RTX 4070 Ti, 12282 MiB VRAM, driver 595.84, RAM 62 GB.
- `/home` = /dev/sda4, 1.7 TB, about 483 GB free (this is the BIG partition; everything big goes under /home/nir).
  `/` = sda2, 92 GB, small: do not put big things there.
- gcc 13.3.0, cmake 3.28.3, git present. NO `nvcc` (no CUDA toolkit). Ubuntu's apt `nvidia-cuda-toolkit` is
  12.0.140 (too old for gcc 13), so do not use it.
- Already installed here (do not redo): Unsloth Studio (~/.unsloth), Pinokio (~/Apps/Pinokio, apps in ~/pinokio, Wan2GP inside it),
  ComfyUI + FLUX.2-dev (~/ai-art, NOT running), Blender 5.2, Caddy hosting. Their start/stop icon pattern is on the Desktop
  (e.g. unsloth-studio.desktop, stop-unsloth-studio.desktop) with scripts in ~/.local/bin (launch-*.sh, kill-*.sh).
- Only ONE big AI app at a time on the 12 GB card. Before starting any studio, check `nvidia-smi` for VRAM already used.
- NOTHING from the TTS work exists on disk. A first attempt was started and then fully deleted at Nir's order:
  `/home/nir/drama3` does not exist. No background processes are running. Verify with `ls -d ~/drama3; ps aux | grep -E "cuda|wget"`.
- All 8 git repos under /home/nir were pulled and are up to date (strulovitz-website, Anime, crystal-balls, peaktogether-website,
  demoscene-museum, second-opinion, ComfyUI, blender-mcp). At Nir's order, AGENTS.md was deleted from the crystal-balls repo on GitHub.
  Nir does NOT want the repo `strulovitz/claude-memory` touched or looked at unless he asks.

## 2. WHAT NIR WANTS

Install on THIS PC the text-to-speech models from the laptop handoff, each with its own friendly web studio, each in its own
folder with Start and Stop buttons, like the laptop did for ACE-Step, Ruach and LatentSync. He chose to start with
DRAMA 3 (the best, hardest one) at HIGH quality (Q4). The other three come afterwards, one at a time; ask which he wants here.

Standard layout per studio (copy the laptop pattern, but on THIS PC):
- Folder `~/<name>` containing: app code, env, models, `docs/INSTALL-RECORD.txt`, `docs/QUICKSTART.txt`, `outputs/`,
  `start-<name>.sh`, `stop-<name>.sh`. One real folder with subfolders (Nir said that layout was fine).
- Desktop icons (.desktop files, also copied to ~/.local/share/applications): Start, STOP (red X), Outputs folder, Open folder, Quick Guide.
  If menu entries do not appear: taskbar right-click, Troubleshoot, Restart Cinnamon.
- Start script: checks nvidia-smi for busy VRAM, starts the server detached (`setsid nohup`), waits for the port, opens the browser.
  Stop script: kills by exact PID/process name only (never `pkill -f` with self-matching text).
- Bind web servers to 127.0.0.1 only.

## 3. DRAMA 3 - THE RESEARCH (all verified from official pages today)

### 3.1 What it is
Fish Audio "Drama 3": huge text-to-speech model, 40 layers, 256 experts (mixture of experts, 8 used per token), 83 languages,
voice cloning, speaker tags, event tags. Official runtime needs 48 GB VRAM, so we use the community GGUF + audio.cpp.

### 3.2 Which runtime
- audio.cpp, repo https://github.com/0xShug0/audio.cpp . On 2026-11-05 the audio.cpp team posted on the official model page
  (huggingface.co/fishaudio/drama-3, discussion 12): "audio.cpp v0.9.4 supports Drama3 ... RTX 5090: CPU expert offloading cut peak VRAM
  from 22.9 GiB to 6.5 GiB with RTF 0.4199 (faster than real time), Q4_K_S experts, Q8_0 tower projections, eight pinned expert-cache slots.
  Offloading trades speed and host RAM for VRAM." That is the authors' own 5090 test; NO independent 12 GB report was found.
- The doc docs/models/fish_drama3.md on main still shows Windows commands and a clone of JarodMica's branch `drama-3-native`.
  FIRST thing to check: does `0xShug0/audio.cpp` main contain `src/community_models/fish_drama3`? If yes, build FROM MAIN (preferred).
  Fallback: `git clone --branch drama-3-native https://github.com/JarodMica/audio.cpp.git` then init the submodule with
  `git -c submodule.external/audio.cpp-server-frontends.url=https://github.com/0xShug0/audio.cpp-server-frontends.git submodule update --init --recursive`.
  (That clone+submodule took about 30 s and 505 MB today.)
- Linux build (from the generic audio.cpp README; confirm with `scripts/build_linux.sh --help`):
  `scripts/build_linux.sh --backend cuda --model-set custom --models fish_drama3 --target audiocpp_cli --target audiocpp_server`
  Needs gcc 13+, cmake, git, and a CUDA toolkit. The CLI and a server with built-in WebUI are the products.
- audio.cpp has its own web UI. Server config key `"ui": true` serves it. Whether the UI exposes all Drama 3 options is UNVERIFIED;
  the CLI and `POST /v1/audio/speech` always work.

### 3.3 CUDA toolkit (the one blocker)
No nvcc on this PC. Plan WITH Nir's consent and password: install CUDA 12.8 (or newer) from NVIDIA's apt repository
(package `cuda-toolkit-12-8`; it installs under /usr/local and does not change the driver). Tell Nir: "this needs your sudo password,
about 5 GB download". The NVIDIA runfile installer (`cuda_12.8.1_570.124.06_linux.run`, 5.4 GB, URL
https://developer.download.nvidia.com/compute/cuda/12.8.1/local_installers/cuda_12.8.1_570.124.06_linux.run) was tried today; lessons:
run it with `bash file.run --nox11 --silent --toolkit --toolkitpath=... --override`; without `--nox11` it dies with "exec: -title: not found"
when started in the background (it wants an xterm). It did begin installing (1.8 GB written) before Nir stopped it. Download speed was ~41 MB/s.
Do NOT take this indirect route again unless Nir approves; prefer the apt route and ask for the password.
Sampling arch for an RTX 4070 Ti is sm_89; the build script auto-detects it.

### 3.4 Which model file (Nir wants the best quality)
Source: https://huggingface.co/Jmica/Drama-3-GGUF (default revision `main` = "V2", October 29 2026 checkpoint). Files:
| file | size | note |
|---|---|---|
| drama-3-backbone-8bit-F32-routers-BF16-embed-head-experts-Q4_K_S.gguf | 23.87 GiB | BEST: experts Q4, routers FP32, embedding+head BF16 |
| drama-3-backbone-8bit-F32-routers-experts-Q4_K_S.gguf | 22.97 GiB | |
| drama-3-backbone-8bit-experts-Q4_K_S.gguf | 22.91 GiB | the variant audio.cpp measured on the 5090 |
| drama-3-backbone-4bit-experts-Q4_K_S.gguf | 21.77 GiB | |
| ...Q3_K_S 18.93 GiB, ...Q2_K 15.88 GiB | | LOWER quality, Nir does not want these |
Nir chose the BEST one (23.87 GiB). Explain to him in plain words (he asked): "BF16" there only describes two small sensitive parts;
the big expert part is still 4-bit. No file is full precision everywhere; the original is about 41 GB FP8 and cannot fit. This one is the best
compromise available. Download with `hf download Jmica/Drama-3-GGUF <file> --local-dir ~/drama3/models` (use `uv run --with huggingface_hub hf ...`
or install hf). Disk needed in total about 35 GB (toolkit already in /usr/local; source 0.5 GB; build ~2 GB; model 23.9 GB).

### 3.5 Settings for 12 GB VRAM + 62 GB RAM (UNVERIFIED on this card; start here, then tune with real measurements)
Option A (the one the audio.cpp authors measured, recommended first):
```
"session_options": {
  "fish_drama3.disk_experts": true,
  "fish_drama3.pin_experts": true,
  "fish_drama3.expert_cache_size": 8,
  "fish_drama3.cpu_expert_layers": 0,
  "fish_drama3.context_length": 4096
}
```
This holds the expert banks in pinned host RAM (about 17 GB of pinned RAM for the Q4 file; Nir has 62 GB) and keeps 8 expert slots per layer on
the GPU. The PR #927 table: peak VRAM 7.6 to 9.7 GiB on a 5090 with `text_chunk_size=256` giving the lower number. Tight but plausibly fits 12 GB.
Option B (older documented knob): `fish_drama3.cpu_expert_layers` = number of the 40 expert layers kept on CPU. Doc says 24 for a 16 GB card with
Q4 experts; for 12 GB try 32 to 40 (all CPU, slowest). Tested only on a 96 GB GPU by the author; 12 GB is UNTESTED.
Request options worth setting: `text_chunk_size` 128 (default) to 256, `skip_empty_chunks=true`, keep `top_k` at the default 4097 (top_k=30 stalls),
`temperature 1.0`, `top_p 0.9`, a `seed`. Optional `fish_drama3.perf_mode=cuda_perf` (faster, may change sampled audio).
Measure real peak VRAM with `nvidia-smi --query-gpu=memory.used --format=csv -l 1` during the first test and tell Nir the real numbers.
Server config sketch (save as ~/drama3/drama3-server.json; port 8035):
```
{"host":"127.0.0.1","port":8035,"backend":"cuda","threads":8,"lazy_load":true,"max_loaded_models":1,"idle_unload_ms":300000,"ui":true,
 "models":[{"id":"drama-3","family":"fish_drama3","path":"models/<the Q4 file>.gguf","task":"tts","mode":"streaming",
  "session_options":{ ...Option A... },"default_request_options":{"max_tokens":1024}}]}
```
Run: `build/bin/audiocpp_server --config drama3-server.json` (on Linux the binary is in build/<preset>/bin; check the real path after building).
CLI test: `audiocpp_cli --task tts --family fish_drama3 --backend cuda --mode streaming --model <gguf> --text "..." --seed 123 --threads 8 --session-option ... --out speech.wav`.
Ask Nir BEFORE generating the first test sentence. Suggested test sentence from the laptop handoff:
"Hello Nir! Today your Linux computer learned to speak, and now it can talk to you. Thank you for building me a home!"

### 3.6 What Nir was told about reliability (so you do not scare him again)
- Emotion and sound tags are NOT reliable in Drama 3 (official audio.cpp doc says so; it happens with Q4 and the original too). There is NO official
  tag list for Drama 3; Fish staff said "describe the delivery in your own words, try anything". Make several takes and keep the best; a seed
  reproduces a take only with the same settings; `previous_takes` allows editing one sentence.
- `max_tokens` (default 1024 frames per text chunk, about 21.5 frames/s, about 47 s) is only a ceiling and is also clamped by `context_length`
  (default 2048). RAISING IT DOES NOT FIX BAD TAKES (my earlier guess that it might was wrong; I corrected it with Nir). A take that hits the cap is
  usually a take that went wrong. Fish's own program uses 600 per chunk.
- Best data (community 5,000-request test, V2, Q4 experts, FP32 routers, BF16 embed/head, all on GPU): trailing quiet >=2 s: 0 (V1 had 25);
  internal quiet >=2 s: 0 (V1 had 35); cap hit 14/5000 (0.28%); repetition flagged 29/5000 (0.6%). Failures are rare.
- Speaker tags `<|speaker:0|>` to `<|speaker:15|>`; event tags like `[sighs]`; voice cloning with `--voice-ref x.wav --request-option reference_text=...`.
- Calm summary Nir accepted: it will install and run; an odd take is normal, press generate again.

## 4. THE OTHER THREE TTS STUDIOS (from the laptop handoff, re-checked today from their READMEs)

Install each only after Nir says which, one at a time, with the same folder/icons pattern. Python from `uv`, Python 3.12.
1. VoxCPM2 (`~/voxcpm2`): `pip install voxcpm` (code github.com/OpenBMB/VoxCPM); web demo `python app.py --port 8808` (pass `--host 127.0.0.1` if supported;
   upstream defaults to 0.0.0.0); also `python lora_ft_webui.py` on 7860 for fine-tuning. Model `openbmb/VoxCPM2` (2B, 30 languages INCLUDING HEBREW, 48 kHz,
   voice design from a text description, cloning). About 8 GB VRAM. Laptop result: 14 GB on disk. Apache-2.0 weights. Fits this card.
2. Zonos (`~/zonos`): github.com/Zyphra/Zonos; `uv sync`, needs `espeak-ng` (apt, needs sudo: ask Nir); `uv run gradio_interface.py`.
   6 GB+ VRAM; hybrid model needs a 3000-series or newer GPU (4070 Ti qualifies). Languages: English, Japanese, Chinese, French, German ONLY (no Hebrew).
   Models `Zyphra/Zonos-v0.1-hybrid` and `-transformer`.
3. Voicebox (`~/voicebox`): github.com/jamiepine/voicebox, the closest thing to "WanGP for voice": studio with 8 engines (Qwen3-TTS 0.6B/1.7B, Qwen CustomVoice,
   Qwen VoiceDesign, LuxTTS, Chatterbox Multilingual (23 languages incl. Hebrew), Chatterbox Turbo, HumeAI TADA, Kokoro), cloning, stories timeline,
   effects, REST API on port 17493. NO prebuilt Linux binary: build from source (needs Bun, Rust, Python 3.12, Tauri prerequisites, `just`; `just setup`, `just dev`),
   or Docker. Nir said Kokoro is not high quality: do not install/enable Kokoro as a choice he relies on. Chatterbox is marked retired upstream but still works;
   Nir said retired is not bad. Linux NVIDIA uses PyTorch CUDA.
Not chosen: Step Audio EditX, F5-TTS (non-commercial weights), Kokoro. LatentSync (laptop) needs about 20 GB VRAM; it does NOT fit this PC and is not planned here.

## 5. EXACT NEXT STEPS (do them in this order, one at a time, each only after Nir's go)

1. Greet Nir briefly (emojis, one screen). Confirm you read this file. Verify the state: `ls -d ~/drama3` (should not exist), `nvidia-smi` VRAM free,
   `df -h /home`. Say the plan in 5 lines and ask "go?".
2. Tell Nir plainly: CUDA toolkit needs his sudo password and ~5 GB. On his "go" + password: add NVIDIA's CUDA apt repo for Ubuntu 24.04 and install
   `cuda-toolkit-12-8`; verify `/usr/local/cuda/bin/nvcc --version`. (Or, if he prefers, the runfile route with `--nox11` as noted.)
3. `mkdir ~/drama3`, clone audio.cpp (main if it has fish_drama3, else the Jarod branch), report size.
4. Tell Nir "now compiling, about 10 to 20 minutes", build with `scripts/build_linux.sh ...`, poll every 45 s, report errors honestly (the docs only show Windows,
   so Linux problems are possible; say so; fix them openly).
5. Download the 23.87 GiB model (BF16 embed-head Q4_K_S) into `~/drama3/models`, with live progress, tell him the real speed and ETA.
6. Write `drama3-server.json` (Option A), `start-drama3.sh`, `stop-drama3.sh`, five Desktop icons, `docs/INSTALL-RECORD.txt` and `docs/QUICKSTART.txt`
   (plain words, including how to use the web page, where outputs go, the reliability notes in 3.6).
7. Ask Nir "may I generate the test sentence?". Then run it, measure time and peak VRAM, tell him where the WAV is. Nir judges the sound.
8. Only then ask which of VoxCPM2 / Zonos / Voicebox he wants next, and repeat the pattern.
9. At the end update this file with what was done and push ONLY this file (and any new doc) by name after Nir asks; verify with `git status --porcelain`
   and `git log origin/master..HEAD`.

## 6. TECHNICAL TRAPS ALREADY HIT (do not repeat)

- Starting installers/clones from a tool call and then being aborted leaves background processes; always check `ps aux` and kill by PID.
- `kill` of an already-finished PID prints errors, harmless. `rm -rf` fails with "Directory not empty" if an installer is still writing: kill it first.
- `git pull` was blocked once by an untracked file with the same path as a GitHub file; handled by backing the file up under
  /home/nir/backups-of-files-that-blocked-git-pull/ with a README, then pulling. Look for that pattern in the future instead of leaving Nir stuck.
- Reddit blocks the fetch tool (403); GitHub API and Hugging Face API/pages work (`huggingface.co/api/models/<id>/discussions` lists forum threads).
- The laptop handoff mentions NetworkManager and `clawdbot-gateway` errors on the LAPTOP; ignore them here.
