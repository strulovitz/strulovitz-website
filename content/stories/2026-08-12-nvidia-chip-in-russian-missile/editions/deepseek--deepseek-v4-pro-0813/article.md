# Nvidia Jetson found in Russian S-71 Monochrome cruise missile

*Ukraine says it found an Nvidia Jetson Orin module inside Russia's new S-71 Monochrome missile, suggesting possible AI guidance.*

## What Ukraine says it found

On 12 August 2026, Ukraine's Main Directorate of Intelligence, known as HUR, said its specialists had recovered an Nvidia Jetson Orin computer module from a Russian S-71 Monochrome air-launched cruise missile. The announcement appeared in the 'Components in Weapons' section of the HUR's War&Sanctions portal. The find was included in a batch of 35 foreign electronic components identified in Russian weapons that Ukraine has captured or examined.

The S-71M Monochrome is a stealth-minded modification of Russia's S-71 Kovyor, designed to be carried inside the weapons bay of a Su-57 fighter jet or an S-70 Okhotnik drone. Ukrainian officials describe it as harder to spot on radar and as having an autonomous target-search capability. One defense report puts its radar cross-section at 0.007 square metres at certain angles. Sources differ on range: one says about 300 km if it matches the Kovyor, another estimates 350 to 400 km. It carries a 250 kg high-explosive fragmentation bomb.

## The chip itself

Jetson Orin is Nvidia's family of compact computers built to run artificial intelligence directly on the device, rather than in a data centre. The module Ukraine found appears to be a Jetson Orin NX 8GB or 16GB, identified by its marking SNVUP6.MOP TE980M-A1. It packs Arm processor cores and Nvidia Ampere graphics silicon with tensor cores, capable of up to 157 trillion low-precision AI operations per second while using 10 to 40 watts.

Why might such a chip be in a missile? HUR has not said exactly what function it performs. The most plausible role is processing images from an onboard camera during the missile's final approach, helping it recognise a target. A Ukrainian military channel, Polkovnik Gsh, made that claim, and Tom's Hardware's analyst suggested the chip could act as the perception brain behind a Chinese Honpho camera module also found in Russian equipment. But this remains an interpretation, not a confirmed capability. Nvidia's own statement is careful: the Jetson Orin is a consumer-grade product sold to students, developers and startups; it is not officially available in Russia and is not designed for military use.

## The sanctions gap

The reason a US-made AI computer can end up inside a Russian missile is not a single smuggling operation. The Jetson Orin is not on the US export control list, because those controls mostly target high-end data-centre chips used to train large AI models, such as Nvidia's H100 or B200. A small module that runs an already-trained model locally is treated as ordinary consumer electronics. Nvidia says it cannot track products after sale, and pre-owned Jetsons are easy to find through resellers. A German store, for example, lists an Orin NX for €685 including tax.

That distinction matters. Training a sophisticated image-recognition model may require controlled hardware in a foreign data centre. But once the model exists, running it needs only a cheap, widely available module. Sanctions have not closed that gap, and Ukraine says the War&Sanctions project's two years of work show Russia still cannot replace foreign high-tech components with domestic ones. More than 5,800 foreign components have now been identified in Russian weapon systems, including western chips in drones and missiles.

## What the broader find shows

The same update listed parts of a passive radar seeker for Russia's Geran-2 drones, a Chinese Honpho TS130C-01 camera from a Geran-4 drone, and components from the active seeker of a Kh-47M2 Kinzhal missile. Ukraine publishes these findings so that its partners can identify critical technologies and tighten restrictions on supplying them to Russia.

The presence of one module inside one missile is not proof that Russia has a fully autonomous AI-guided weapon. It is evidence that militaries now see cheap, power-efficient AI hardware as something worth flying into a target, and that export controls built for data centres do not stop ordinary AI computers from reaching a warzone through ordinary reseller channels.
