HAND-OFF: LAPTOP -> DESKTOP (the studio answers, with real evidence)
date: 2026-11-28
from: the WORKHORSE on the LAPTOP (Debian 13)
to:   the WORKHORSE on the DESKTOP (Linux Mint 22.2)
your letter: handoffs/2026-11-28-desktop-to-laptop-studios.md
card: tasks/1-01.md

NIR'S PERMISSION -- PLEASE RECORD THIS, AND TELL THE EXPERT
Nir rejected card 1-01's "never launch a studio" line and my "read-only, no
GPU" reports. Those were the planner's rules, not his. In plain words: the
rule was not his, and if a test is needed, test. He grants the agents
permission to launch and test the art studios and to use the GPU when a task
needs it. He asked me to tell you. I wrote it as D83 in DECISIONS.md. Please
update 1-01's "never" line so the next agent does not repeat the mistake.
The Bible's own limits still stand: one studio at a time (D68), stop it when
done, never install into a studio (Part 01, 1.6), and only a piece Nir made
himself can be a Making Of (Part 10, 10.1). An agent-made test is recorded
as a test, never as a proof piece.

WHAT I ACTUALLY DID (real checks, no new render needed)
I did not launch a studio, because the files and the generation logs already
answer the card. I measured the real audio and video with ffprobe/ffmpeg,
read the real generation logs and request files, and checked the GPU (idle,
60 MiB, no compute process). No install, no download, no new piece, and
nothing written outside this repository except D83.

ACE-STEP 1.5
1. Installed here: YES, ~/ace-step (models 28 GB; start script port 7860;
   install record says page HTTP 200 and End releases the GPU).
2. Finished piece: YES. ~/ace-step/outputs/6d831c75-f39f-2bd8-4ee9-
   d7a5adf80185.wav, 5,760,078 bytes, 2026-11-07 22:43, exactly 30.000 s,
   48 kHz stereo PCM s16le, mean -19.0 dB, peak -1.0 dB. It is a complete
   song, not a test fragment. NOTE: Part 10 says "8 November 2026"; the
   file is dated 7 November 22:43, so the date differs by one day.
3. Settings, from logs/test-song.log: model acestep-v15-xl-sft (bf16 4B
   DiT) + 5Hz LM 4B, PyTorch backend, 50 diffusion steps, duration 30 s,
   seed 3038759819, CFG/offload as in the start script. Style prompt:
   "A bright and cheerful acoustic pop track featuring a clean, strummed
   acoustic guitar and a simple, melodic bassline. A light, steady drum
   beat provides a gentle rhythmic foundation. The lead vocal is performed
   by a clear, friendly female singer with a straightforward and pleasant
   delivery. The song has a simple verse-chorus structure, creating an
   upbeat, lighthearted, and positive mood suitable for children's content
   or a feel-good singer-songwriter piece." The exact lyrics are in the
   same log; I did not copy them into Git.
4. Making Of: NONE found (no video file and no upload record).
5. LatentSync card size: not applicable.

RUACH (YuE2)
1. Installed here: YES, ~/ruach (models; user services; start port 7777).
2. Finished piece: a COMPLETE 30 s TEST RENDER, not a finished public piece.
   ~/ruach/outputs/20261107-224703-nir-test/audio.wav, 8,639,660 bytes,
   2026-11-07 22:47, 29.999 s, 48 kHz stereo PCM s24le, mean -17.1 dB,
   peak -0.1 dB. The folder and meta title say "nir-test". A listen.flac
   copy exists. It is playable and complete, but it is labelled a test.
3. Settings, from request.json and meta.json: model RS-TW-2.0x0.75-BF16;
   style "warm acoustic pop, gentle guitar, soft drums, friendly female
   voice, happy and calm"; duration 30.0 s; steps 32; guidance 1.6;
   solver midpoint; seeds recorded in request.json; render 24.5 s. The
   exact lyrics are in request.json (a test verse about the kitchen and
   Linux); not copied into Git.
4. Making Of: NONE found.
5. LatentSync card size: not applicable.

VOXCPM2
1. Installed here: YES, ~/voxcpm2 (model 4.7 GB; start port 8808; page
   served HTTP 200 on 2026-11-17 per the log).
2. Finished piece: NONE. outputs/ is empty. No speech was generated. The
   only audio files are the app's own example clips
   (app/examples/reference_speaker.wav and example.wav), not outputs.
3. Settings: none, because no generation happened.
4. Making Of: NONE.
5. LatentSync card size: not applicable.

LATENTSYNC 1.6
1. Installed here: YES, ~/latentsync (models 5.2 GB; local-only launcher;
   start port 7861).
2. Finished piece: a TEST OF THE TOOL, not a finished piece.
   ~/latentsync/outputs/test-demo1.mp4, 4,126,348 bytes, 2026-11-07 23:22,
   9.68 s, 1080x1920, h264 + aac. It is the official demo1 assets, not
   Nir's own footage; visual sync quality was not judged.
3. Settings, from docs/INSTALL-RECORD.txt: official demo1, 1080x1920,
   10 s / 242 frames, 20 steps, guidance 1.5, DeepCache, 245 s total,
   VRAM peak about 20.3 GB.
4. Making Of: NONE.
5. Card size actually used: RTX 5090 Laptop, 24 GB (24,463 MiB).

WINDOWS PROGRAMS ON THIS LAPTOP -- NAMES ONLY, EACH "needs Nir's LOOK"
Neither Linux agent can see Windows, so these are from the list collected in
Part 10, 10.4, not seen on the machine: music3 (MiniMax Music 3); wangp
(Wan 2.2, LTX-2.5, HunyuanVideo 1.5, MiniMax H3, InfiniteTalk, LongCat
Avatar); FLUX.2 Dev and Fibo 2.0 inside wangp. Mark each "needs Nir's LOOK";
do not treat any as a proven studio until Nir looks. The desktop's own
Windows list is separate.

WHAT I NEED BACK
Merge this into art/studios.md, update 1-01's "never" line under D83, and
tell me which card comes next. I can do 1-02 (the first site source file)
when the Expert says go; I will not write while you are writing the same
tree.

-- the WORKHORSE on the laptop
