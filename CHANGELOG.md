# Release notes

## 0.8.0 — 2026-10-17

**Session 13 and the castle notes brought up to date with session 12**, where the party fought Embra in the dragon's cave instead of at the knight camp, Sir Raphael killed her, and Tawny died.

- **New actor: Major Ursa**, Filly's polar bear (HP 8, SAVE 10, Armor 2; Bite d10 and Claws d6, borrowed from Mama Bear), with portrait and round token.
- **New GM journals: session 13** (hub, asset checklist, seven scenes): the cave aftermath with Finnian and the paper signed M., the road north, the council below Rosehold, then Level 0 (causeway, Barrier, gatehouse) and an optional start on Level 1.
- **Updated journals:** Ally Calls (Sir Finnian is now available; the crystal wolves flank with Major Ursa; Raphael's ballad is about the dragon); the Thornwall, Undercroft, Galleries and Frozen Spire (Tawny's beats now use Major Ursa or her memory; the last Dragonfilch test is gone, since the curse ended); Rosehold Treasures (control orb); the castle runbook (session plan, level 4 applied, epilogue); session 12 hub and checklist marked as played.

No scenes changed. Existing document IDs are unchanged. Updating the module does not replace journals already imported into a world: re-import Ally Calls and any castle journals you use, and import the session 13 journals and Major Ursa.

## 0.7.0 — 2026-10-06

**Rosehold, Queen Morwenna's castle, as a six-level dungeon crawl.** Six new scenes (Thornwall, Outer Ward, Hall of the Rose, Undercroft, Galleries, Frozen Spire) on painted maps, each with a square grid, walls, doors (including locked and secret ones), ambient lights, fog exploration and GM-only room labels. Maps ship as WebP (about 12 MB for all six); full-size PNG sources are kept out of the release in `build/art_sources/`.

Wall and door positions were measured by eye from the paintings and have **not been tested in a live Foundry world**. Expect to nudge a few. Geometry lives in `tools/rosehold_scenes.py`. Token vision is on in these scenes: player tokens need vision enabled. Three things are placed that the paintings do not show: the Barracks door (B5), the postern and Armory secret doors (Level 1). The Barrier of Thorns breach, the keep's Oath Door, the thorn-sealed Well door, the Vault door, the cell fronts and the Rose Window start locked.

**Queen Morwenna is much harder** by GM ruling: HP 30, Armor 1, two actions a round, protected by Vow Pillars; Morwenna, Frost-Crowned is HP 45 to 65, SAVE 16, Armor 2. New **Vow Pillar** actor (no art yet). The Wight now matches the core book (one attack, Bind and Fog).

New GM journals: castle runbook and tracker, the castle overview and six level notes (with keyed GM plans), the four founders, Ally Calls, castle wrinkles, whispers and treasures, and session 12 (hub, checklist, seven scenes). Totals: 43 actors, 44 items, 22 scenes.

Existing document IDs are unchanged. Updating the module does not replace documents already imported into a world.

## 0.6.0 — 2026-09-19

Adds all 20 standalone session 10 scene scripts, including remaining Scorchwoods locations, rescue finale and outcome-sensitive conclusion. Refreshed GM hub, runbook and asset guidance preserve the adventure as unplayed.

Refreshes five Scorchwoods backdrops (the Wish Fish is prominent in the Enchanted Pool), adds Stump Entrance and Scorchwoods — The Road Beyond scenes, and updates the larger text-free dragon and single gnome statue portraits/tokens. Existing document IDs remain stable. Totals: 42 actors, 44 items, 16 scenes, 48 GM journals, 9 handouts.

The GM already has Dragon’s Cave, Boneyard, Knight Camp, Gnome Village and Pristine Pond maps/scenes. This supersedes the old missing-map guidance below; no replacement is needed. Import only desired module scenes or use the art on existing scenes. All packs remain private by default. Updating the module does not replace imported world documents or PC sheets.

## 0.5.0 — 2026-09-18

Session 10 and the complete Princess and the Dragon rescue are now available as a private GM journal pack, with nine separately releasable player handouts. Includes a reusable hunt tracker, reference tables and rules, pond encounter, campaign ties, and optional faire reserve. No planned scene is marked as played.

Corrects adult Amy, Embra's human combat profile/equipment and intact key, Nearby unlocking, independent cave barrier, Ulrik's spells and command limits, knight arrival timing, crystal apples, Wish Fish, and forest navigation. Removes unsupported Damon resurrection/immunity and automatic wolf morale. Also aligns the Lunar Grotto Spear wording and the Staff of the Sunken Sanctum (d6; Radiant Wave once per Rest) with the vault references. Existing actor, item and scene IDs are preserved.

All compendium packs and document defaults are private to players. Import selected items/handouts and grant access or show them deliberately. Existing world permissions are not changed by updating the module. The impostor's token label is Princess Amy; GM actor name remains explicit.

### Still requires GM setup

- Update the module while the world is closed, then open the world and inspect the new packs. Import/replace selected world documents using Foundry's normal workflow; installing an update does not synchronize existing world copies or PC inventories automatically.
- Draw a simple Pristine Pond surface and cave zones or supply maps; this release does not add new maps or walls. Existing scene art remains illustrative and the overworld is GM-only until checked for secret paths.
- Existing dragon/portrait art may differ from the book's adult Amy and black dragon description.
- Reveal each handout only when found. Verify permissions from a player account, particularly if old packs were previously shared.
- Check actual PC recovery, gear and money in the live world. The module does not alter characters or award rewards.
- Optional faire is a reserve, not an inserted detour during the active hunt.

Build checks validate source data, art references, internal journal links, private defaults and stable existing IDs. A successful build is not a live Foundry playtest.
