---
type: session-prep
campaign: Perils & Princesses
session: 10
status: prepared, not yet played
---

# Session 10 Asset Checklist — Through the Scorchwoods

> **Prep:** [[session10_prep]] · **Whole adventure:** [[princess_and_dragon_runbook]]
> **Scope:** session 10 plus the complete book rescue, however many sessions it takes. Optional faire assets are deferred. Castle preparation is a later task.
> **Audit:** 2026-09-16. “Exists” means a local source file was found; it does **not** mean imported, assigned, permissioned, or ready in the live Foundry world. This pass does not change the companion module.

## Release follow-up — 2026-09-18

Module **0.5.0** (commit `e2042bc`) adds 28 private GM journals and 9 separately releasable handouts, applies the book corrections and campaign weapon reference fixes, and preserves existing actor/item/scene IDs. Source validation, journal pack round-trip checks and archive checks passed. All packs default to GM-only; previously imported world permissions still need inspection.

The handoff below is retained as the original checklist. Module content/build work is completed; **live import checks, player-map review, and actual character recovery/inventory checks remain pending**. No new maps, art or walls were added. See the sibling module's `CHANGELOG.md` for the release details. This release does not establish any new played campaign events.

## Art and scene update — 2026-09-19

**GM maps confirmed:** Dragon’s Cave, Boneyard, Knight Camp and Gnome Village are already available and in use. Use those maps; no replacement maps are needed. Their absence from this vault/module must not reopen a missing-map task. Pristine Pond remains confirmed separately.

Seven scene backdrops are ready in the vault: refreshed Enchanted Pool (Wish Fish prominent), laughing flowers, crystal orchard, memorial stones and archivist’s cottage; new stump entrance and conclusion. The monster portrait now depicts **one gnomish warrior statue**; the stump encounter still uses four tokens. Previous versions are preserved in adjacent `assets/archive/` folders.

New assets: [[locations/The_Scorchwoods/assets/stump_entrance_scene.png]] and [[locations/The_Scorchwoods/assets/scorchwoods_conclusion_scene.png]]. The other images retain their existing paths below. Module **0.6.0** packages the refreshed images, updated scene dimensions and statue token art, stump/conclusion scenes and all 20 GM scene scripts. Live-world import remains a separate step. Use **Stump Entrance** and **Scorchwoods — The Road Beyond** as the new scene names.

Scenes 15–20 add the flowers, orchard, stones, cottage, rescue finale and outcome-sensitive conclusion. All are prepared, unplayed material; carry unused notes forward rather than forcing the full adventure into session 10.

## Session folder layout

The hub and this checklist are in `prep/session10/`. Twenty individual scene notes live in `prep/session10/scenes/`; use the scene menu in [[session10_prep]]. Each scene includes narration, dialogue and its own asset/setup list. Existing art is linked in place rather than copied. Module 0.6.0 includes these individual scene journals.

## ✅ Available source assets

| Use | Existing source | Readiness / limits |
|---|---|---|
| Pristine Pond scene | **Existing Foundry world scene — GM confirmed** | Already created; not included in the module. No new pond map or scene is needed. No vault file path was supplied. |
| Source adventure | [[books/The Princess and the Dragon - Digital Pages.pdf]] | Full adventure; printed page numbers are PDF page numbers minus 2. The linked Markdown extract is only an item excerpt, so it is not a sufficient GM script. |
| Session and adventure scripts | [[session10_prep]], [[princess_and_dragon_runbook]] | Ready in the vault; includes all ten locations, all four hunting parties, both key routes, and endings. |
| GM tracking and staged handouts | [[princess_and_dragon_tracker]], [[princess_and_dragon_handouts]] | Ready as Markdown. Handout master contains GM answers; share only selected player text. |
| Scorchwoods overview | [[maps/princess_and_the_dragon/Scorchwoods Map.jpg]], [[maps/princess_and_the_dragon/ForestMapFull.jpg]] | GM reference. Inspect/crop before player use; source map includes secret routes. No wall or grid configuration implied. |
| Cave and Boneyard | [[locations/The_Scorchwoods/assets/scorchwoods_dragon_cave_scene.png]], [[locations/The_Scorchwoods/assets/boneyard_scene.png]] | Scene illustrations, not verified tactical maps. |
| Gnomes and Pool | [[locations/The_Scorchwoods/assets/gnome_village_scene.png]], [[locations/The_Scorchwoods/assets/enchanted_pool_scene.png]] | Scene illustrations. Pool is book location 5, distinct from the session 10 Pristine Pond. |
| Flowers and Orchard | [[locations/The_Scorchwoods/assets/snapdragon_field_scene.png]], [[locations/The_Scorchwoods/assets/crystal_orchard_scene.png]] | Scene illustrations. |
| Stones, Cottage, Camp | [[locations/The_Scorchwoods/assets/stones_of_remembrance_scene.png]], [[locations/The_Scorchwoods/assets/abandoned_cottage_scene.png]], [[locations/The_Scorchwoods/assets/knight_camp_scene.png]] | Scene illustrations; do not present the Stones as an automatic Wight fight. |
| Pond enemies | [[monsters/assets/vine_crawler.png]], [[monsters/assets/corruption_bloom.png]] | Art exists; six crawler tokens and one Bloom needed for the full defense. Stats: [[Vine_Crawler]], [[Corruption_Bloom]]. |
| Pond/grove/courier NPCs | [[npcs/assets/thistledown.png]], [[npcs/assets/unicorn_aurelius_full_power.png]], [[npcs/assets/nim_the_badger.png]] | Verify live token/image assignments later. |
| Filly's reward and compass | [[items/assets/lunar_grotto_spear.png]], [[prep/assets/pps_silver_rose_pin_1783108203964.png]] | Art exists; use current [[The_Lunar_Grotto_Spear]] and [[Silver_Rose_Fairy_Compass]] rules. Rewards remain unawarded until played. |
| Amy and Embra | [[npcs/assets/dragon_amy.png]], [[npcs/assets/princess_amy.png]], [[npcs/assets/princess_embra.png]] | Shared dragon portrait updated: larger black dragon, blue necklace, no text. Amy is 22; review human portrait separately. Token labels and journals must not spoil the swap. |
| Four captains and Ulrik | [[npcs/assets/sir_finnian.png]], [[npcs/assets/lady_stella.png]], [[npcs/assets/sir_raphael.png]], [[npcs/assets/sir_damon.png]], [[npcs/assets/magus_ulrik.png]] | Art exists. Book statistics and optional-rider corrections are in the runbook. |
| Gnomish and forest contacts | [[npcs/assets/pippin_cobbleton.png]], [[npcs/assets/tifa.png]], [[npcs/assets/hesperia.png]], [[npcs/assets/wish_fish.png]] | Art exists; Pippin is not established as this pair of necklaces' original maker. |
| Wolves, statues, guards | [[monsters/assets/crystal_wolf.png]], [[monsters/assets/gnomish_warrior_statues.png]], [[npcs/assets/generic_guard.png]] | Use corrected [[Crystal_Wolf]] and book [[Drakenshire_Royal_Guard]], not the older generic guard profile. |
| Optional faire | [[maps/princess_and_the_dragon/Faire Map.jpg]], [[monsters/assets/stone_dragon.png]], [[princess_and_dragon_faire_reserve]] | Reserve only; no festival inserted during the active rescue. [[Stone_Dragon]] now matches the book. |

**GM-confirmed correction:** Pristine Pond already exists in the live world. Do not reopen its creation as a missing-asset task based on old checklists, missing vault art, or absence from the module. Optional module packaging would be a separate request.

## ❌ Gaps and decisions

Suggested paths are targets, **not claims that a file exists**. Simple sketches, ordinary counters, and existing illustrations are sufficient to run the adventure; polished art is optional.

| Priority | Need / decision | Suggested target or action |
|---|---|---|
| 🔴 HIGH — before session 10 | Rest, wounds, sheet inventory, silver spike, and allocation of 76 SP checked | Use the preflight in [[session10_prep]]. Do not resolve unknown wounds or add unconfirmed mine loot in an import. |
| 🔴 HIGH — later Foundry prompt | Actors, item text, GM journals, and handout permissions match this prep | Follow the handoff below; module rebuild/import/live verification remain pending. |
| 🔴 HIGH — before sharing a map | Inspect or prepare a player-safe forest map without secret tunnel/answer information | `maps/princess_and_the_dragon/scorchwoods_player.png`. Keep the original GM map private. |
| 🟢 LOW | Review human Amy portrait for adult depiction | Dragon art is complete at `npcs/assets/dragon_amy.png`; only the human portrait remains to review. |
| 🟢 LOW | Individual retinue / animal tokens where module art is generic | Review existing actor assignments before creating art. Reuse guard/animal markers for Robin, Diana, Beck, Michelle, Parker, Scamp, attendants, and mules as appropriate. |
| 🟢 LOW | Styled physical clues and a visible six-step tracker | Player-only exports from [[princess_and_dragon_handouts]] to `prep/assets/princess_and_dragon/`; keep [[princess_and_dragon_tracker]] GM-only. Markdown and six counters already work. |
| 🟢 LOW — only if faire selected | Three color-coded stone-dragon tokens, paper dragons, tickets, and Tifa's Journal | `prep/assets/princess_and_dragon/faire/`; existing statue art can be reused three times. Add a book-stat actor later if needed. |

## Future Foundry handoff — no changes made here

Read the companion module's README and local guidance before starting the separate update. Its source manifest is `build/module.json`; source generation is `tools/generate_src.py`. Generated pack files live in `build/src/`. Correct the generator/source rather than only patching regenerated JSON. Keep vault checks and module tests separate.

The inspected module snapshot is **0.4.0**, with **42 actors, 44 items, and 14 scene sources**. Every inspected scene has zero walls. A scene document or illustration does not establish a tactical map, journal link, permission, grid, lighting, token setup, or live installation. Reinspect the module when the update begins; these are observations, not permission to overwrite newer changes.

### Content corrections and additions

- [ ] **Amy/Embra:** Amy is 22; dragon body is medium and black. Dragon Amy: HP 24 / SAVE 16 / Armor 3; one bite d12 **or** claws d8; breath 10, halved on GRACE, once per Rest. Embra's human body is **HP 8 / SAVE 15 / Armor 0**, dagger d6 (5–6 breaks for extra d6), physical-evasion advantage, Ring of Fire 1 GD, pixie dust, healing potion, original key. Replace the module's noncombatant-only human description. See [[Dragon_Amy]] and [[Embra]].
- [ ] **Necklaces and keys:** remove the false “original key destroyed” claim from item and journal text. Embra has it. Both wearers must be Nearby, then unlock and remove both necklaces. Pippin's replacement requires enchanted water **plus** 50 SP or a favor in lieu of the fee. The cave barrier is separate from the necklaces. Use [[The_Magic_Necklaces]].
- [ ] **Knight behavior:** import all four retinues and exact tracker/lair-arrival rules from the runbook. Damon follows Ulrik within a Stone's Throw and otherwise continues the last command. Disable unrequested fear/charm immunity and resurrection/silver-radiant riders. Restore Ulrik's living vulnerability to a willingly eaten crystal apple. Do not automate a reset at tracker 6.
- [ ] **Wolves and guards:** [[Crystal_Wolf]] is 4 / 6 / 0, bite d6 and/or claws d4 (one or two attacks); no automatic half-pack morale rule added as book canon. Use [[Drakenshire_Royal_Guard]] at 4 / 8 / 1 for Finnian's eight guards. Keep older campaign variants distinct.
- [ ] **Pond:** ensure six crawler tokens and one Bloom can be staged, with the linked campaign profiles and pixie aid. Queue spear, Moonpetal, blessing, and riddle reward; do not automatically award them during import.
- [ ] **Compasses:** existing pins gain the fairy-compass function in play; point toward Amy independent of body, red in danger. Remove any compulsory WITS check for every keyed-location movement.
- [ ] **Wish Fish:** magical Pool-water bargain for a **fresh crystal apple with a live worm**; candied apples do not work. Invulnerable while in its water. Do not turn colorful “wish” language into an unlimited wish-granting ability.
- [ ] **Scamp:** helpful companion and scout, not an omniscient guide or an invulnerable plot object. Remove the module's unsupported “must not be harmed” rule if it is presented mechanically.
- [ ] **Gnomes/stones/cottage:** original-key route remains valid; no extra Tifa gate. Dain's resolution uses the truth about his sacrifice, not a mandatory generic Wight encounter. Include all four cottage clues and mark the archivist's claim unreliable.
- [ ] **Faire only if requested:** current module actor list lacks a Stone Dragon. Use [[Stone_Dragon]] 8 / 8 / 3, two attacks bite d8 + claws d6, glide/no flight/no breath, fairground boundary. Do not enable this encounter during the rescue.

### Journals, scenes, and access

- [ ] Import/link the session 10 script, full adventure runbook, ten location cards, retinue references, and tracker as **GM material**.
- [ ] Split Handouts A–F into individually releasable entries. Answers, release conditions, key location, Ulrik/Morwenna links, and PPS history must not inherit player permissions.
- [ ] Keep misleading in-world testimony distinguishable from GM facts. Avoid labels such as “Embra in Amy's body” on a player-visible token before discovery.
- [x] Pristine Pond world scene already created — GM confirmed. Its absence from the module is not an asset gap.
- [x] GM already has Dragon’s Cave, Boneyard, Knight Camp and Gnome Village maps; no replacement maps needed.
- [ ] Assign the new stump/conclusion backdrops during the later module update. Inspect the existing forest overview before making it player-visible. Configure walls/lighting only where the chosen map supports them.
- [ ] Set opening token counts without duplicating imported actors/items in the live world. Keep campaign PC sheets and their exact HP/money authoritative.

### Acceptance checks for that later update

1. Open a fresh import and verify art, linked notes, stats, and item descriptions; test from a player view that GM secrets and the map's secret paths remain hidden.
2. Walk the **original-key route**: get Embra's key → bring both wearers Nearby → unlock/remove both → handle cave barrier independently. No Pippin quest required.
3. Walk the **replacement-key route**: access gnomes → obtain fresh wormy apple with Hesperia's permission → trade for Pool water → pay Pippin or earn fee waiver → craft key. No mandatory original-maker or Tifa dependency.
4. Exercise the tracker once: ordinary movement alone costs no point; Spend Time adds 1 and checks for a Wrinkle; overnight adds 2; alliance lowers 1 and removes that party from the danger roll. Check Finnian's grace interval, Stella's 4 damage, Damon's 8 damage, and Raphael's friendly arrival. Use the precise book/table-ruling distinctions in the runbook.
5. Check the pond's purification alternative, spear recharge, Dragon Panic's separate hazards, and a peaceful resolution with Embra. Do not substitute normal dragon breath for the panic sneeze.
6. Run the module's documented validation/build checks, then verify actual installed/imported behavior separately. Record unresolved asset gaps rather than claiming readiness from a successful build alone.

## At the table, then between sessions

Open [[session10_prep]], the pond location, and the spear before play. Use the standalone scene scripts when the cave begins; [[princess_and_dragon_runbook]] is an optional cross-reference. Start [[princess_and_dragon_tracker]] only when the hunt procedure begins; record the actual starting point and every change. At each later session, check Amy's HP, knights' dispositions and locations, key/water/necklace holders, player knowledge, consumables, and the selected next destination. Do not pre-roll an outcome or advance campaign state from these plans.
