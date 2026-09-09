# Ukraine finds Nvidia AI module inside Russia's S-71 Monochrome missile

*Ukraine's intelligence says it found an Nvidia Jetson Orin AI computer inside Russia's new S-71 cruise missile, one of 35 foreign parts.*

On August 12, 2026, Ukraine's military intelligence service, known as HUR, announced an unusual piece of salvage: inside Russia's newest cruise missile, its technicians had found a small American computer of the kind sold openly to students, robotics hobbyists and startups. The part was an Nvidia Jetson Orin, a compact module built to run artificial-intelligence software aboard whatever machine it is installed in. Its presence suggests the weapon may use AI to see where it is going.

## What the teardown found

The module appeared in the latest release of HUR's War&Sanctions portal, a running catalog of foreign parts recovered from Russian weapons. This batch listed 35 electronic components, most from the United States and the rest from Switzerland, Japan, Belarus and China. Alongside the Nvidia module were parts of a passive radar seeker that Russia has begun fitting to Geran-2 drones to help them find and strike Ukrainian air-defense systems and radars; a Chinese Honpho TS130C-01 camera recovered from a jet-powered Geran-4 drone; and components from the active seeker of a Kh-47M2 Kinzhal missile.

According to Tom's Hardware, the markings on the recovered unit — SNVUP6.MOP TE980M-A1 — appear to match a Jetson Orin NX, a module that has been shipping since 2023, and the markings indicate it was packaged in March 2025. That date matters: this was fresh stock, not old surplus, and it reached Russia years after sanctions were tightened.

## The missile

The S-71 Monochrome is a modification of the S-71K Kovyor cruise missile, reshaped to fit the internal weapons bays of Russia's Su-57 fighter jet and its S-70 Okhotnik drone. It is built to be hard to detect and is claimed to be able to search for targets on its own. Its warhead is a 250-kilogram high-explosive fragmentation bomb, which Militarnyi identifies as an OFAB-250-270.

Reported performance differs. Militarnyi gives a range of up to 300 kilometers, assuming the Monochrome's specifications match the Kovyor's; United24 Media estimates 350–400 kilometers at a speed of 500–600 km/h and cites a claimed radar cross-section of just 0.007 square meters. Both sets are claims about a missile that, by United24's account, has been used only in limited numbers since the start of 2026.

## The chip's likely job

HUR was careful in what it asserted: the module's presence “may indicate” the use of AI, and the agency did not disclose what the hardware actually does in flight. But the plausible role is not hard to see.

A cruise missile that steers only by satellite positioning and inertial guidance can be dragged off course by jamming, and it can strike only coordinates fixed before launch. A camera changes that. A vision model, trained in advance to recognize particular objects or scenes, can look at the ground in the final seconds of flight, match what it sees against what it was sent to find, and steer onto it. That last stretch is called terminal guidance, and recognizing images in real time on a small, low-power device is precisely what the Jetson Orin line is built for. The family ranges up to 275 trillion operations per second — the standard measure of AI hardware — while drawing between 15 and 60 watts in its largest model and 10 to 40 in the NX.

The Ukrainian military channel Polkovnik Gsh reported that the module works with an onboard camera to guide the missile through this final stage. Tom's Hardware sketches the same architecture: the Jetson as the weapon's eyes, recognizing what the camera sees and passing the result to a separate system that does the steering. Nor is this a first find — HUR previously reported Jetson Orin NX modules in Russia's Shahed MS001 drones, used for local decision-making and terminal guidance, and United24 notes similar technology in the V2U system and the Shahed-236 attack drone.

## Why sanctions didn't stop it

Nvidia, in a statement to Tom's Hardware, said Jetson Orin modules are “consumer-grade products sold to students, developers, and startups,” are “not available in Russia,” and are “not designed for military purposes.” Pre-owned units circulate through many resellers; the company cannot track products after they are sold, and says it will take action against customers that violate export controls.

None of that is evasive, and that is the uncomfortable part. Jetson modules are not on export-control lists, because those lists aim at a different class of chip: the giant datacenter accelerators — Nvidia's H100 and B200 among them — used to train AI models. The cheaper, mass-produced hardware that merely runs a finished model is not covered. Once trained, a model travels as a file, and the computers able to run it ship by the hundreds of thousands for robots, factory cameras and student projects. Controls built around the top of the AI stack have little grip at the bottom, where weapons live.

## The wider pattern

HUR and Ukrainian research institutions have spent two years dismantling captured weapons and tracing their parts, and the agency's conclusion is that Russia still cannot fully replace foreign high-tech components with domestic ones. The tally has passed 5,800 foreign parts — 5,816 across 202 weapon systems as of August 2026, according to United24. The exceptions are telling: in the Oreshnik ballistic missile, every component identified came from companies in Russia or Belarus. The dependence is real, but not uniform.

The module itself is neutral hardware — the same board that might steer a student's robot through a maze. What separates the lab bench from the weapons bay is not the chip but the software loaded onto it and the intent of the buyer, and nothing in today's supply chain is designed to notice the difference.
