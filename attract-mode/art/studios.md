THE STUDIO LIST (Part 10, section 10.4)
Written 2026-11-28 from real checks on both PCs.

HOW TO READ IT. Every claim says what it is based on:
  SEEN     measured on the machine (file exists, ffprobe, log, size, date)
  REPORTED taken from a survey or from Part 10, not re-checked here
  LOOK     only Nir's eyes can answer it (Windows programs, the screen)

A piece is "finished" only when a playable file exists and is not labelled a
test. A program that is installed is not a piece. Nir alone makes proof
pieces (Part 10, 10.1); an agent-made test is a test.

--------------------------------------------------------------------------------
SOUNDTRACK
--------------------------------------------------------------------------------

## ace-step
department: soundtrack
makes: songs
where: laptop-linux
installed: yes, ~/ace-step, models 28 GB, start script on port 7860
evidence: SEEN 2026-11-28 on the laptop (files, generation log, ffprobe)
proof: a FINISHED 30-second song
  file: ~/ace-step/outputs/6d831c75-f39f-2bd8-4ee9-d7a5adf80185.wav
  5,760,078 bytes, 2026-11-07 22:43, exactly 30.000 s, 48 kHz stereo PCM,
  mean -19.0 dB, peak -1.0 dB
made-with: acestep-v15-xl-sft (4B DiT) + 5 Hz LM 4B, PyTorch backend,
  50 diffusion steps, duration 30 s, seed 3038759819
proven-on: 24 GB (RTX 5090 Laptop)
making-of: none yet
note: Part 10 says "8 November 2026"; the file is dated 7 November 22:43.
  The lyrics stay on that machine and are not copied into Git.
source: the studio's own page -- to be collected by the Expert

## ruach
department: soundtrack
makes: songs
where: laptop-linux
installed: yes, ~/ruach, start script on port 7777
evidence: SEEN 2026-11-28 on the laptop
proof: a complete 30-second TEST render, not a finished public piece
  file: ~/ruach/outputs/20261107-224703-nir-test/audio.wav
  8,639,660 bytes, 2026-11-07 22:47, 29.999 s, 48 kHz stereo PCM s24le,
  mean -17.1 dB, peak -0.1 dB
made-with: RS-TW-2.0x0.75-BF16, 32 steps, guidance 1.6, midpoint solver, 30 s
proven-on: 24 GB (RTX 5090 Laptop)
making-of: none yet
note: the folder and its meta title say "nir-test". Part 10 calls it a
  proven song; the evidence says a test render.
source: the studio's own page -- to be collected by the Expert

--------------------------------------------------------------------------------
VOICE
--------------------------------------------------------------------------------

## voxcpm2
department: voice
makes: speech in a cloned voice; speaks Hebrew
where: laptop-linux (also installed on desktop-linux)
installed: yes on the laptop, ~/voxcpm2, model 4.7 GB, port 8808
evidence: SEEN 2026-11-28 on the laptop
proof: NONE. outputs/ is empty; no speech was ever generated.
status: the page answered 200 on 2026-11-17; that is a test of the app, not
  a piece
making-of: none
source: the studio's own page -- to be collected by the Expert

## latentsync
department: voice (lip sync)
makes: a talking head from a picture and a sound file
where: laptop-linux
installed: yes, ~/latentsync, models 5.2 GB, port 7861, local only
evidence: SEEN 2026-11-28 on the laptop
proof: the TOOL'S OWN DEMO, not Nir's own footage
  file: ~/latentsync/outputs/test-demo1.mp4
  4,126,348 bytes, 2026-11-07 23:22, 9.68 s, 1080x1920, h264 + aac
made-with: official demo1 assets, 242 frames, 20 steps, guidance 1.5,
  DeepCache, 245 s, VRAM peak about 20.3 GB
proven-on: 24 GB (RTX 5090 Laptop)
making-of: none
note: Part 10 says "needs about 20 GB"; the real run peaked at 20.3 GB, so
  the limit is REAL, not an estimate.
source: the studio's own page -- to be collected by the Expert

--------------------------------------------------------------------------------
DESKTOP-LINUX, SEEN ON THIS PC (2026-11-28)
--------------------------------------------------------------------------------

  drama-3    ~/drama3     installed; no finished piece recorded
  voxcpm2    ~/voxcpm2    installed; no finished piece recorded
  zonos      ~/zonos      installed; tests passed per the survey; no piece
  voicebox   ~/voicebox   installed; includes Whisper Large v3; no piece
  comfyui    ~/ai-art/ComfyUI  FLUX.2-dev; not running; no finished picture
  unsloth    ~/.unsloth   a training and chat studio, not a Making Of
  pinokio    ~/pinokio    runs WanGP (video); no finished video recorded
  source: the desktop survey, machines/desktop.md

--------------------------------------------------------------------------------
WINDOWS -- NEITHER LINUX AGENT CAN SEE IT. EACH NEEDS NIR'S LOOK.
--------------------------------------------------------------------------------

  laptop-windows: music3 (MiniMax Music 3); wangp with Wan 2.2, LTX-2.5,
    HunyuanVideo 1.5, MiniMax H3, InfiniteTalk, LongCat Avatar; FLUX.2 Dev
    and Fibo 2.0 inside wangp. REPORTED by Part 10; nobody has looked.
  desktop-windows: unknown. Part 10 says "when Nir is next there, he answers
    one LOOK request: which studios are installed".

--------------------------------------------------------------------------------
WHAT THIS MEANS FOR STAGE 1 (Part 10, section 10.6)
--------------------------------------------------------------------------------

1. SOUNDTRACK opens first: ace-step has the only finished song, and ruach
   has a complete test render. So the first Making Of is the ACE-Step song.
2. VOICE comes next: the studios are installed and their apps answer, but
   not one has produced a piece. A piece must be made before a Making Of.
3. CINEMATICS and CONCEPT ART wait for a first piece on Nir's PC.
4. D83 (Nir, 2026-11-28): an agent may launch and test a studio and use the
   graphics card when a card needs it. One studio at a time (D68), stop it
   after the work, never install into a studio (Part 01, 1.6).
