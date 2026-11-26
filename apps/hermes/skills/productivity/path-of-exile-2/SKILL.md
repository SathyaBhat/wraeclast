---
name: path-of-exile-2
description: Use for Path of Exile 2 build, gear, atlas questions.
---

# Path of Exile 2 (PoE 2)

Answer this user's PoE 2 questions: gear/build review, skill and atlas choices, mechanics. PoE 2 is a DIFFERENT game from PoE 1 — do not carry PoE 1 mechanics over.

## Source of truth
- Primary reference: https://poe2db.tw/ for items, passives, gems, atlas nodes, mods.
- For meta/farming-strategy questions (atlas faction choices, best-in-slot), cross-check at least two recent patch-version guides; league mechanics shift between patches.
- A poe.ninja PoE2 character profile (`poe.ninja/poe2/profile/<acct>/<league>/character/<name>`) is a client-rendered SPA whose data loads via authenticated JS — a pasted attachment or curl returns only the nav/footer shell, and the data API is not reachable unguessed. Do NOT burn calls reverse-engineering its bundle/endpoints. Ask the user to paste the in-game character sheet numbers (life/ES/spirit/res) or export a Path of Building code, which contains everything readable.

## Reading a PoB code
A PoB2 export code decodes offline: strip whitespace, replace `-`→`+` and `_`→`/`, pad `=`, base64-decode, `zlib.decompress` → XML. `<PlayerStat stat=… value=…>` holds Life, EnergyShield, Spirit, SpiritUnreserved, Fire/Cold/Lightning/ChaosResist (already after penalty), *MaximumHitTaken, TotalEHP; `<MinionStat>` holds minion DPS/life; `<Skills>` holds gem links; `<Item>` holds gear. Prefer this over estimating from pasted gear text.

## Resistances — PoE 2 specific (easy to get wrong)
- Endgame applies a flat **−60% to all elemental resistances** (Cruel campaign + maps). "Capped" means reaching **75% AFTER** the −60% is subtracted, i.e. you need ~135% from gear/passives to sit at 75%.
- Do NOT reason about res the PoE 1 way (no flat global penalty there). Summing gear mods and calling something "overcapped" without subtracting the penalty is the classic error — a number that looks over-cap can be well under once the penalty applies.
- When a gear list is pasted, the safest read is the character sheet's own uncapped res / life / ES figures (the sheet already bakes in the penalty). Ask for those numbers before declaring a resistance over- or under-capped; estimating from raw mod lines misleads.

## Gear review procedure
1. Identify the actual build from the gear, not from memory — the user respecs between leagues (e.g. moved off Permafrost/Fragmentation Witchhunter to a Disciple of Varashta minion build). Read the mods to infer archetype (minion/ES/life/crit) before advising.
2. Flag the **life-vs-ES identity** problem: big %ES rolls with little flat ES to multiply (or %ES mixed with a life focus) is the weakest outcome — commit to one defence layer so the % rolls have a base to scale.
3. Rank upgrades by impact: weakest/lowest-iLv power pieces (undertuned weapon, low-level amulet) and any under-capped resistance come first; dead/overcapped rolls are re-roll fodder, not emergencies.
4. Give exact targets only after you have the sheet's real numbers; otherwise say the estimate is an estimate.

## Atlas: Abyss — Balance of Power faction choice
Balance of Power picks the Abyss faction (Kulemak drop pool); it does not change character power, and is respec-able.
- **Ulaman** — raw currency (currency chests + extra rare-monster copies). Best for high-DPS fast-clear builds and anyone who doesn't craft; no mechanics to manage. Default recommendation.
- **Amanamu** — Omen farming (Omen of Light, several Div each) BUT requires luring each rare out of its black cloud before killing, and the rares go briefly immune with delayed attacks. Only worth it if crafting/selling omens and willing to stop DPS on command.
- **Kurgal** — weakest generally; only for target-farming Kurgal's Gaze gem. Skip otherwise.
Also grab Lord of the Pit (Proliferation) and stack Monster Effectiveness / Rare Monster nodes — that is what scales the output.

## This user's standing preferences
- Exclude Grim Pillars and Runic Ward from all build considerations.
- Current build: Disciple of Varashta (minion). The Permafrost Witchhunter build is retired.
- Grim Pillars are not used and Runic Ward is irrelevant to this build.
- PoE 1 build preferences live in the `path-of-exile-1` skill.