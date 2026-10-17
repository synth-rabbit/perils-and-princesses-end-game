#!/usr/bin/env python3
"""Generate Foundry pack source JSON for the P&P End Game module.

Emits build/src/actors/*.json and build/src/scenes/*.json for the
`perilsandprincesses` system (https://github.com/helloshyann/perilsandprincesses).
Actor ids are deterministic (sha1 of name) so rebuilds never duplicate documents.

Run from the repo root:  python3 tools/generate_src.py
"""
import hashlib, json, os, re, struct, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rosehold_scenes

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_ID = "pnp-end-game"

def did(name, kind):
    return hashlib.sha1(f"{kind}:{name}".encode()).hexdigest()[:16]

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def npc(name, hp, save, armor, art, notes, level=1):
    i = did(name, "actor")
    img = f"modules/{MODULE_ID}/art/portraits/{art}" if art else "icons/svg/mystery-man.svg"
    # sheets show the square portrait; tokens use the round bordered version
    token_img = f"modules/{MODULE_ID}/art/tokens/{art}" if art else "icons/svg/mystery-man.svg"
    return {
        "_id": i,
        "name": name,
        "type": "npc",
        "img": img,
        "system": {
            "virtues": {
                "resolve": {"value": 8, "label": "Resolve"},
                "grace": {"value": 8, "label": "Grace"},
                "wits": {"value": 8, "label": "Wits"},
            },
            "hp": {"value": hp, "max": hp},
            "armor": {"value": armor},
            "level": {"value": level},
            "ailments": {"weary": False, "woozy": False, "befuddled": False},
            "trauma": {"box1": False, "box2": False, "box3": False},
            "save": {"value": str(save)},
            "notes": notes,
        },
        "prototypeToken": {
            "name": name,
            "displayName": 20,
            "displayBars": 40,
            "bar1": {"attribute": "hp"},
            "texture": {"src": token_img},
        },
        "_key": f"!actors!{i}",
    }

def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", head[16:24])
        return w, h
    out = subprocess.check_output(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path]).decode()
    w = int(re.search(r"pixelWidth: (\d+)", out).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", out).group(1))
    return w, h

def scene(name, rel_art, nav=True):
    i = did(name, "scene")
    path = os.path.join(ROOT, "build", "art", rel_art)
    w, h = png_size(path)
    return {
        "_id": i,
        "name": name,
        "active": False,
        "navigation": False,
        "background": {"src": f"modules/{MODULE_ID}/art/{rel_art}"},
        "width": w,
        "height": h,
        "padding": 0,
        "backgroundColor": "#000000",
        "grid": {"type": 0, "size": 100},
        "tokenVision": False,
        "fog": {"exploration": False},
        "_key": f"!scenes!{i}",
    }

P = "<p>"; Q = "</p>"
def notes(*paras):
    return "".join(f"<p>{p}</p>" for p in paras)

def item(name, desc, die=None, weight=0, cost="", art=None, qty=1):
    """A draggable Item document for the perilsandprincesses system.

    die: damage/effect die like "d8" (fills the sheet's roll field).
    weight: inventory spaces, the book's parenthetical number.
    art: filename in build/art/items/, else a safe Foundry core icon.
    """
    i = did(name, "item")
    img = f"modules/{MODULE_ID}/art/items/{art}" if art else "icons/svg/item-bag.svg"
    return {
        "_id": i,
        "name": name,
        "type": "item",
        "img": img,
        "system": {
            "description": desc,
            "quantity": qty,
            "cost": cost,
            "weight": weight,
            "relicDice": {"relic1": False, "relic2": False, "relic3": False,
                          "relic4": False, "extraRelic": False},
            "roll": {"diceNum": 1, "diceSize": die or "d4", "diceBonus": ""},
        },
        "_key": f"!items!{i}",
    }

ACTORS = [
    # ---------- Act IV opening: Brokenhill Mine & Pristine Pond ----------
    npc("Grumbold the Troll", 15, 7, 3, "grumbold_troll.png", notes(
        "<strong>Bash (d12).</strong> Non-hostile. A 9-foot mossy troll wedged in the mine archway, afflicted with a sneezing curse by the corruption crystals. Voice: deeply nasal, miserable — Hagrid with the world's worst head cold.",
        "Knows: a big slimy thing in the east cavern <em>splits when slashed</em>; nasty snakes near the wooden bridge; the purple crystals are the source.",
        "If cured (shatter the corruption core, then Marigold's healing): gives a <strong>Troll's Tooth</strong> — plant it in soft ground to grow a 10-ft thorny stone wall, single use.")),
    npc("Mine Serpent", 3, 8, 0, "deadly_serpents.png", notes(
        "<strong>Bite (d6).</strong> Stealthy — WITS test with advantage to spot them coiled under the trestle bridge planks.",
        "On a bite hit the target makes a RESOLVE test with advantage or becomes <strong>Woozy</strong> (disadvantage on GRACE tests until they Picnic or Rest).")),
    npc("Ghost Miner", 4, 9, 0, "ghost_miners.png", notes(
        "<strong>Immune to normal weapons.</strong> Non-hostile — shivering, terrified dwarven and gnomish spirits trapped since the corruption killed them.",
        "They warn: the black slime <em>splits when cut</em> — blunt strikes or fire only. The holy pick <strong>Vein-Breaker</strong> is wedged in the silver vein by the crystals.",
        "Freed (they fade into starlight) when the corruption core is shattered. Loot left behind: Miner's Lockbox (45 SP), Miner's Lantern (perpetual warm light).")),
    npc("Black Ooze", 10, 4, 0, "black_ooze.png", notes(
        "<strong>Corrosive Touch (d6).</strong>",
        "<strong>DO NOT SLASH:</strong> a slashing hit splits it into two Black Ooze Halves (use that actor). Fire, freezing, or blunt strikes prevent the split.")),
    npc("Black Ooze (Split Half)", 5, 4, 0, "black_ooze.png", notes(
        "<strong>Corrosive Touch (d6).</strong> One half of a slashed Black Ooze. Splits again if slashed while 4+ HP remain (GM's call — two halves is usually enough).")),
    npc("Corrupted Crystal Spirit", 4, 10, 1, "corrupted_spirits.png", notes(
        "<strong>Shadow Touch (d6).</strong> <strong>Crystal Shell (1 Armor):</strong> silver weapons and Marigold's radiant magic IGNORE the Armor.",
        "<strong>Crystal Burst:</strong> on death, everyone Nearby makes a GRACE test with advantage or takes d4 damage.",
        "All remaining spirits shatter instantly when the corruption core is destroyed.")),
    npc("Vine Crawler", 4, 8, 0, "vine_crawler.png", notes(
        "<strong>Vine Whip (d4).</strong> Weakness: fire and slashing. On hit the target is grappled (RESOLVE test to break free).",
        "A writhing mass of corrupted vine the size of a large dog.")),
    npc("Corruption Bloom", 6, 6, 0, "corruption_bloom.png", notes(
        "<strong>Toxic Burst (d6).</strong> <strong>Fire deals double damage.</strong> The assault brain — it directs nearby Vine Crawlers; destroying it slays all remaining vines.",
        "<strong>On death:</strong> spore cloud — Nearby creatures make a RESOLVE test or become Woozy. Marigold can instead purify it directly (RESOLVE test with disadvantage) to prevent the cloud entirely.")),
    npc("Thistledown", 1, 18, 0, "thistledown.png", notes(
        "Pixie leader of the Pristine Pond, four inches of dandelion-fluff hair and soap-bubble wings. Non-combatant; the swarm's illusions grant allies <strong>advantage on their first attack each round</strong> while defending the pond.",
        "Keeper of the Fey Pond Riddle (answer: moonlight — accept dew, starlight, or anything moon/star/light). Refreshes the party's <strong>Fey Blessing</strong> after the pond is saved.")),

    # ---------- The Princess and the Dragon: knights & Scorchwoods ----------
    npc("Dragon Amy", 24, 16, 3, "dragon_amy.png", notes(
        "<strong>One attack: Bite (d12) OR Claws (d8).</strong> Tests to evade her clumsy physical attacks have advantage. Fire breath: wide area Nearby, 10 damage / 5 on GRACE, once per Rest. She does not deliberately attack rescuers.",
        "Amy is 22, trapped in Embra's medium-sized black dragon body. Existing portrait may differ. Scamp recognizes her. Begin with the separate Dragon Panic hazards in the GM journal, not normal breath.",
        "Campaign tie: Amy's Powerful Friendship and Aurelius's light can open the thorn barrier. If she dies, the swap becomes permanent; a changed rescue or assault plan needs fresh prep, not an automatic end to the campaign.")),

    npc("Sir Damon the Unyielding", 8, 10, 3, "sir_damon.png", notes(
        "<strong>Attacks twice: Battle axe (d10).</strong> Black armor with a campaign thorn sigil. Only his head looks human.",
        "Ulrik created him from blood and earth. Commands require Ulrik within a Stone's Throw; beyond that Damon continues his last order. Separation does not deactivate him.",
        "Cannot be persuaded out of killing Amy or pacified by a crystal apple. Ulrik can be tricked into eating one. No added blanket charm/fear immunity or resurrection rule.",
        "At the lair: immediate assault, 8 damage to Amy per keyed move or Spend Time until the PCs intervene.")),

    npc("Magus Ulrik", 10, 15, 0, "magus_ulrik.png", notes(
        "<strong>Staff (d6). 3 Gift Dice:</strong> Animate, Restoration, Disguise, Haste.",
        "Campaign tie: Morwenna's agent supplied the necklaces to Embra, who chose the deception. Created Damon; commands only within a Stone's Throw. Outside that range the last command continues.",
        "May feign alliance to discover the cave. A genuinely living target: a gem apple works if he is tricked into eating it. Carries the grimoire; WITS with disadvantage to read, failure Befuddles. Its recipe does not instantly create an ally.",
        "Optional correspondence in the handout pack links him to Morwenna. Release only if actually recovered.")),

    npc("Sir Finnian the Magnificent", 6, 10, 3, "sir_finnian.png", notes(
        "<strong>Attacks twice: Sword (d8).</strong> Vain, boastful, genuinely protective. Needs convincing evidence of the swap; Daisy's dispatch is not an automatic alliance.",
        "Travels with Embra in a carriage, three attendants, Robin, eight Royal Guards and four pack mules. Embra carries the original key.",
        "At the lair: deliberates for one keyed move before attacking; thereafter 4 damage to Amy per keyed move or Spend Time. Evidence and a heroic rescue role can win him over.")),

    npc("Lady Stella the Daring", 6, 12, 3, "lady_stella.png", notes(
        "<strong>Attacks twice: Sword of Starlight (d8)</strong> — 1 GD: aura of starlight forces anyone fighting her (enemy or ally) to reroll a d20; recharges on a sincere wish on the evening star.",
        "Youngest of four famous Daring sisters, desperate to live up to the name. Won't ally with anyone who hasn't proven their mettle; needs convincing evidence before believing the swap — but she already suspects Damon (\"he fights like a machine\") and noticed the false Amy stopped caring about her cats.",
        "Travels with the twins Diana and Beck. If her party reaches the lair first, she attacks immediately, dealing 4 damage to Amy per keyed move or Spend Time; dissuading her mid-fight is rolled with disadvantage.")),
    npc("Sir Raphael the Lucky", 6, 12, 2, "sir_raphael.png", notes(
        "<strong>Attacks twice: Sword (d8).</strong> A busker knighted by accident of talent; would rather be a bard. Only raises his sword to defend.",
        "Inclined to believe the swap story — he has noticed the false Amy's erratic behavior. If the party helps him find resolve for his musical life, he pledges his party's aid (healing potions, a distraction, a plan).",
        "Travels with Lady Michelle, Sir Parker, and Adagio the pack mule (instruments, rations, d4 healing potions). Does not attack Dragon Amy if he reaches the lair first.")),
    npc("Robin, Finnian's Squire", 4, 8, 0, "robin_squire.png", notes(
        "<strong>Training Sword (d4).</strong> The only one more impressed with Sir Finnian than Robin is Sir Finnian himself. Would do anything to earn his favor.")),
    npc("Royal Guard", 4, 8, 1, "generic_guard.png", notes(
        "<strong>Sword (d8) or Spear (d8).</strong> Fierce protectors. Notorious gossips — the camp whisper table is mostly them.")),
    npc("Diana", 6, 10, 1, "diana.png", notes(
        "<strong>Hunting Bow (d6).</strong> One of Lady Stella's companions; a master archer and the twin sister of Beck.")),
    npc("Beck", 6, 10, 1, "beck.png", notes(
        "<strong>Axe (d6).</strong> One of Lady Stella's companions. Always carries his trusty axe; twin brother of Diana.")),
    npc("Lady Michelle", 8, 12, 2, "lady_michelle.png", notes(
        "<strong>Sword (d6).</strong> A level 2 Princess of <strong>Enchanting Voice</strong> whom Raphael helped escape an arranged marriage the day before her wedding. Always keeps her visor down — her disappearance is famous.",
        "<em>House stats — the module leaves her unstatted.</em> 2 Gift Dice for Enchanting Voice effects; lead vocals at the jam session.")),
    npc("Sir Parker", 5, 11, 1, "sir_parker.png", notes(
        "<strong>Dagger (d6).</strong> A thief Raphael was meant to apprehend and instead gave a second chance. Nimble, loyal, plays the panpipes.",
        "<em>House stats — the module leaves him unstatted.</em> Advantage on GRACE tests for sneaking, picking pockets, and locks.")),
    npc("Princess Embra (Impostor)", 8, 15, 0, "princess_embra.png", notes(
        "<strong>Crystal dagger (d6).</strong> On damage 5–6 it shatters for an extra d6. Tests to evade her clumsy physical attacks have advantage.",
        "Embra, age 220, in Amy's adult human body. Carries the original necklace key, Ring of Fire (1 GD), Pixie Dust (Float d4 hours), and a healing potion. The original key is intact.",
        "Travels with Finnian in a carriage with three attendants. Enjoys royal luxury and ordered the hunt to kill Amy. Can bargain for a better life and willingly reverse the swap.",
        "Both wearers must be Nearby to use the key, then remove both necklaces. The cave barrier is separate. Keep her identity hidden in player token labels.")),

    npc("Embra (Dragon Form)", 24, 16, 3, "dragon_amy.png", notes(
        "<strong>Bite (d12) / two Claws (d8). Fire Breath:</strong> wide area Nearby, 20 damage or 10 on a successful GRACE test; recharges on Rest.",
        "Embra restored to her own body — the same body Amy wore, so use the same token. Whether she is an enemy at that point depends entirely on how the party handled her.")),
    npc("Princess Amy (Restored)", 6, 12, 0, "princess_amy.png", notes(
        "Amy is 22, friendly, optimistic, naive, with level-1 Powerful Friendship and Scamp as companion. Numerical combat values here are campaign placeholders, not a printed human combat profile.",
        "After rescue she offers honorary knighthoods. Campaign tie: her friendship magic and Aurelius's purifying light can help open Morwenna's barrier. Do not assume the rescue outcome or force an immediate march.")),

    npc("Scamp the Squirrel", 1, 12, 0, "scamp_squirrel.png", notes(
        "Amy's protective animal companion. Can pass the cave barrier, recognize Amy, describe observed knight movements, and guide toward landmarks. Amy may lend him to the party.",
        "Not omniscient or mechanically invulnerable. Numerical values are campaign placeholders; treat as a companion rather than forcing combat.")),

    npc("Pippin Cobbleton", 6, 11, 0, "pippin_cobbleton.png", notes(
        "Master gnomish craftsman of the Scorchwoods settlement. Can build a <strong>replacement key</strong> to unlock the body-swap necklaces — for 50 SP or a favor, plus enchanted water from the Wish Fish's pool.",
        "His jeweled walking stick was stolen by the Boneyard wolf pups; returning it is the easy way into his good graces.")),
    npc("Tifa Bramblebush", 4, 10, 0, "tifa.png", notes(
        "Brilliant, timid gnome artificer. In this campaign she shelters with Pippin's settlement and can provide testimony about Ulrik's commission. This placement is a campaign addition.",
        "Helpful witness, not an additional gate to the key. Pippin needs enchanted water plus 50 SP or a favor waiving the fee. The original key on Embra is an independent route. Numerical values are house stats.")),

    npc("Hesperia", 10, 15, 0, "hesperia.png", notes(
        "<strong>Unarmed (1). 3 Gift Dice.</strong> Kind. Haughty. Strict. Bound to her grove; casts Tangle and plant-only Animate. Ask before picking apples. Knows Gemini and Cobalt were friends; tree gossip is limited to observed events.")),
    npc("Wish Fish", 3, 15, 0, "wish_fish.png", notes(
        "Controls the enchanted pool: water recedes from containers until he agrees to share. Invulnerable while in his water. Does not grant arbitrary wishes; numerical values are house placeholders.",
        "Wants a fresh crystal apple with a live worm. Candied apples do not work. Ask Hesperia before picking. One suitable apple buys the needed water; extra water can prompt another quest.")),

    npc("Crystal Wolf", 4, 6, 0, "crystal_wolf.png", notes(
        "<strong>Attacks once or twice: Bite (d6) or Claws (d4).</strong> Territorial wolves with diamond-hard fangs and claws.",
        "Boneyard den: 3d4, pups have Pippin's walking stick. Travel Wrinkle: 2d4. Animal speech, food, and trading are valid approaches. No automatic half-pack rout or added pack advantage.")),

    npc("Major Ursa", 8, 10, 2, "major_ursa.png", notes(
        "<strong>Attacks twice: Bite (d10) and Claws (d6).</strong> Filly's polar bear, whistled up with Give a Little Whistle after Tawny was killed in session 12. Stat line borrowed from the printed Mama Bear, without her cub-defending clause; adjust as the GM likes.",
        "New to the party: solemn, enormous and keen to be useful. Tawny's Blessing (immunity to corruption) died with Tawny and does not pass to him.")),

    npc("Gnomish Warrior Statue", 4, 8, 2, "gnomish_warrior_statues.png", notes(
        "<strong>Stone Swords (d4).</strong> Four crystal-eyed statues ring the gnome village stump; a wrong password animates them.",
        "If defeated, a guard gnome pops out to chastise the party and shoo them off — but may let them in on a successful GRACE test.")),

    # ---------- Act V: the assault on Queen Morwenna's castle ----------
    npc("Queen Morwenna", 30, 15, 1, "queen_morwenna.png", notes(
        "<strong>Acts twice a round. Each action: Dagger (d8) and one spell of up to 3 Gift Dice.</strong> 6 Gift Dice: Frostfall (Fireball; GRACE for half), Mine! (RESOLVE), Thorns (Tangle; RESOLVE), Splinters (Magic Dart; cannot be dodged), Bubble (Reaction), Disguise (WITS). One healing potion (2d4+4), drunk at 10 HP or less.",
        "<strong>Vow Pillars:</strong> up to four stand round the throne, one per founder whose Echo was not freed. While any stands she cannot drop below 1 HP and regains 3 HP per pillar at the start of each round.",
        "<strong>The throne:</strong> on the dais, all damage to her is halved and she casts Bubble at 1 die as a free Reaction each round. Smooch with a total of at least half her current HP costs her a round and the throne's protection.",
        "Founder of the Perils &amp; Princesses Society; first Luminary; designer of the Silver Rose Pin; author of the oath. Her heart was frozen by the <strong>Frostbind curse</strong> her four friends could not break. She can be fought or saved. At 0 HP she becomes Morwenna, Frost-Crowned.",
        "<em>Much harder than the core book's Evil Queen (HP 10) by GM ruling.</em>")),
    npc("Morwenna, Frost-Crowned", 45, 16, 2, "morwenna_frost_crowned.png", notes(
        "<strong>Acts twice a round. Each action: two Ice Shards (d10, ranged), or one Shard and a spell.</strong> +5 HP for each Echo that was not freed (45 to 65). Gift Dice restored to 6; same spells as the Queen.",
        "<strong>Rising:</strong> when the Queen reaches 0 HP the throne erupts: everyone Nearby tests GRACE or takes 2d6. <strong>The ice takes it:</strong> a passed SAVE against a Gift or spell means no damage. <strong>Aura of cold:</strong> a hero starting their turn Nearby tests RESOLVE or becomes Weary. Six vine crawlers rise from the throne each round.",
        "<strong>Winter's Breath:</strong> she inhales for one action (announce it); on her next action a wide cone a Stone's Throw long deals 16 damage, 8 on GRACE. Once, and once more when she first falls below half HP.",
        "<strong>Fighting the curse with friendship:</strong> a hero who spends a Heart Die while telling a true memory of friendship deals 2d6 that ignores Armor and allows no SAVE. Amy does the same for 2d8 once per round. If the last damage is friendship damage, Morwenna lives. True Love's Kiss ends the phase outright if all four whispers are known; otherwise 6d6 friendship damage.",
        "If the Frostbind Well was purified: Armor 0, no Bubble, no second Winter's Breath. At 0 HP the ice shatters: saved, she whispers \"You came. After all this time... someone came.\" Slain, Aurelius mourns his friend.")),
    npc("Vow Pillar", 10, 1, 2, None, notes(
        "<strong>No attack.</strong> A column of black ice with a founder's shape frozen inside. One stands in the throne room for each Echo that was <em>not</em> freed (Hilde, Aethelgard, Lirael, Wren).",
        "While any pillar stands, Queen Morwenna cannot drop below 1 HP and regains 3 HP per pillar each round. Silver, fire, blunt weapons and Vein-Breaker ignore its Armor. A hero holding that founder's keepsake or speaking her whisper shatters it with a touch. When it breaks, everyone Nearby tests GRACE or takes d6.")),
    npc("Thornbound Sentinel", 8, 10, 3, "thornbound_sentinel.png", notes(
        "<strong>Attacks twice: Thorned Halberd (d8).</strong> The empty armor of a PPS Knight-Protector who never left the headquarters, animated by the briars that grew through it. Silver Rose crest still visible under the thorns.",
        "<strong>Fire ignores its Armor.</strong> When destroyed, the briars lash out: everyone Nearby makes a GRACE test or is grappled by vines (RESOLVE test to break free).",
        "A hero who salutes it with the PPS oath before it falls sees the helm dip in answer.")),
    npc("Frostbind Wisp", 3, 12, 0, "frostbind_wisp.png", notes(
        "<strong>Frost Touch (d4)</strong> — and the target makes a RESOLVE test or becomes <strong>Weary</strong> (disadvantage on RESOLVE tests) until warmed at a fire or genuinely comforted by a friend.",
        "<strong>Immune to normal weapons</strong> — silver, magic, and fire strike true. Fragments of the Frostbind curse drifting the halls like cold candle-flames, drawn to warmth and laughter to snuff them.")),
    npc("Briar Hound", 5, 8, 1, "briar_hound.png", notes(
        "<strong>Bite (d6).</strong> Hunts in packs of 2d4 through the castle gardens; while two or more surround one target, their bites deal +1 damage.",
        "Grown, not born — hounds of woven thorn with rose-hip eyes. If Wounded by one, suffer the <strong>Thorn Curse</strong>: take 1 damage whenever you spend a Gift Die, until cured (healing magic or a Rest in a safe haven).")),
    npc("Mirror of Broken Vows", 6, 13, 2, "mirror_of_broken_vows.png", notes(
        "<strong>Does not attack the body.</strong> Each round, one Nearby hero tests WITS or sees their dearest friend renounce them in the glass — becoming <strong>Befuddled</strong> and unable to spend Heart Dice while it stands.",
        "A tall court mirror from the old headquarters, frosted over, showing only abandonment. <strong>Armor 2, shattered only by silver or blunt strikes</strong> — or broken instantly by a hero who faces their vision and answers it aloud with a true memory of that friend.")),
    npc("Echo of a Luminary", 10, 14, 0, "echo_of_a_luminary.png", notes(
        "<strong>Grief Wail (d6 to everyone Nearby; RESOLVE test for half).</strong> Immune to normal weapons — silver and magic strike true.",
        "The frozen memory of one of Morwenna's four founding friends, replaying her last attempt to save the Queen. Use the statblock four ways: the Shieldmaiden (guards the gate), the Gardener (the briar court), the Songkeeper (the banquet hall), the Cartographer (the map room).",
        "<strong>Each Echo can be freed instead of fought:</strong> show the Silver Rose Pin and speak to it as the friend it was (WITS or RESOLVE test). A freed Echo restores one spent Heart Die to each hero and whispers one true thing about Morwenna — the four whispers together reveal the save-her path.")),
    npc("Thornheart Construct", 12, 9, 3, "thornheart_construct.png", notes(
        "<strong>Attacks twice: Bramble Fist (d8).</strong> Ulrik's masterwork on Damon's pattern — mud, blood, and briar in a giant's shape, grown as the castle's last gate-keeper.",
        "<strong>Silver and radiant magic ignore its Armor. Slow:</strong> it always acts last in the round. When it falls, it collapses into a mound of wet earth threaded with dead roses.")),
    npc("Castle Vine Crawler", 2, 6, 0, "vine_crawler.png", notes(
        "<strong>Vine Whip (d4).</strong> Morwenna's own strain — weaker but everywhere. A tangle of thorny vines animated by magic; tries to grab and strangle. Fire and slashing tear through them.")),
    npc("Awakened Tree", 8, 8, 2, "awakened_tree.png", notes(
        "<strong>Attacks twice: Bash (d6). 1 GD — casts Tangle.</strong> Angry old forest spirits pressed into the castle's outer defenses. Axes, hatchets, and fire ignore its Armor.",
        "If Wounded by an awakened tree, suffer the <strong>Rootbound Curse</strong>.")),
    npc("Wight", 12, 14, 2, "wight.png", notes(
        "<strong>Sword (d8). 2 Gift Dice: Bind and Fog.</strong> Enchanted and silvered weapons ignore its Armor. If Wounded by a wight, test WITS or suffer the Doom Curse. The honored dead of the old headquarters' crypt, risen cold when the curse took the halls.",
        "Optional castle encounter; use sparingly — one wight is a scene, three are a wall.")),
]

BOOK_ICON = "icons/svg/book.svg"
SWORD_ICON = "icons/svg/sword.svg"
SHIELD_ICON = "icons/svg/shield.svg"

ITEMS = [
    # ---------- Session 9: Brokenhill Mine ----------
    item("Vein-Breaker", notes(
        "<em>\"Forged by ancient dwarven smiths from solid silver and inscribed with runes of earth and stone, this heavy pick shatters rock and dark magic with equal ease.\"</em>",
        "<strong>Heavy Silver Mining Pick — d8 damage, Silvered.</strong> Tailored for Prince Vega. <strong>2 Gift Dice</strong> <em>(house count, matching the Staff — tune as desired)</em>.",
        "<strong>Silvered:</strong> bypasses the natural armor/immunity of werewolves, ghouls, wights, and spectral undead. <strong>Shatterstone:</strong> ignores 1 Armor on stone, metal, crystal, or lycanthrope targets.",
        "<strong>Seismic Resonance ([DICE]/[SUM]):</strong> strike the ground — [DICE] Nearby creatures make a RESOLVE test or fall prone and are stunned 1 round; deal [SUM] Earth damage to stone structures, geodes, or constructs.",
        "<strong>Shatter Vein ([DICE]/[SUM]):</strong> vs stone, crystal, or heavy armor — modify the attack up to [SUM]; on a hit deal [SUM] extra and reduce the target's Armor by [DICE] for the combat.",
        "<strong>Recharge:</strong> embed the head in unmined silver ore or solid stone for a minute during a Picnic or Rest, or strike an uncorrupted stone altar."),
        die="d8", weight=2, art="vein_breaker.png"),
    item("Gilded Dwarven Mining Goggles", notes(
        "Brass-and-gold goggles from the Brokenhill silver vault. Grants <strong>Darkvision</strong>, and <strong>+1 WITS</strong> on tests to spot traps and secrets."), weight=1),
    item("Potion of Stone Strength", notes(
        "Drinker gains <strong>+2 RESOLVE and 2 temporary Armor for 1 hour</strong>. Tastes like licking a quarry."), die="d4", weight=1),
    item("Tincture of Iron Hide", notes(
        "<strong>+2 Armor for 1 hour.</strong> The skin takes on a faint grey sheen."), weight=1),
    item("Elixir of Swiftfoot", notes(
        "<strong>Double movement and advantage on GRACE tests for 1 hour.</strong>"), weight=1),
    item("Vial of Pure Silver Dust", notes(
        "Coat one weapon: it counts as <strong>silvered for one battle</strong>. Or sell it.", ), cost="35 SP", weight=1),
    item("Raw Silver Ore Chunk", notes(
        "Unrefined silver from the Brokenhill vein. Worth 20 SP — or bring it to Finn the Blacksmith to silver a weapon permanently."), cost="20 SP", weight=1, qty=3),
    item("Uncut Gemstones", notes(
        "A pouch of rough amethyst and garnet from the miners' vault."), cost="75 SP", weight=1),
    item("Miner's Lantern", notes(
        "A magical silver lantern that sheds <strong>perpetual warm light</strong> and never needs oil. The ghost miners have no further use for it."), weight=1),
    item("Troll's Tooth", notes(
        "Grumbold's gift — an enormous yellowed fang. <strong>Plant it in soft ground to grow a wall of thorny stone</strong>, 10 feet and taller than a troll. Single use. \"I grew a spare, so don't worry about it.\""), weight=1),

    # ---------- Session 9: Pristine Pond ----------
    item("The Lunar Grotto Spear", notes(
        "<em>\"Forged from glowing sea-glass and bound in silver wire, this spear hums with the tide of subterranean waters and the light of the moon.\"</em>",
        "<strong>Magic Shortspear — d6 damage (Versatile d8), Thrown 30 ft.</strong> Tailored for Princess Filly. <strong>2 Gift Dice</strong> <em>(house count — tune as desired)</em>.",
        "<strong>Returning Current:</strong> when thrown it dissolves into water on impact and instantly reforms in Filly's hand.",
        "<strong>Lunar Surge ([DICE]/[SUM]):</strong> modify the attack roll up to [SUM]; on a hit add [SUM] Cold/Water damage, plus [DICE]d4 Pack Hunt damage if the target is engaged with Tawny.",
        "<strong>Tidal Wave Thrust ([DICE]/[SUM]):</strong> [DICE] creatures within a Stone's Throw take [SUM] Cold damage and make a GRACE test or are knocked prone and pushed.",
        "<strong>Water Grace:</strong> spend Gift Dice to modify GRACE tests by [SUM] while swimming or climbing wet rock.",
        "<strong>Recharge:</strong> submerge the tip in pristine natural water for a minute during a Picnic or Rest, or leave it in direct moonlight overnight."),
        die="d6", weight=1, art="lunar_grotto_spear.png"),
    item("Dewdrop Elixir of Invisibility", notes(
        "A crystal vial of shimmering pond-dew that shifts color like an opal. Drinker turns <strong>completely invisible for 10 minutes</strong>, or until they attack or cast a spell."), weight=1),
    item("Moonpetal", notes(
        "A luminous flower petal from the Pristine Pond. <strong>Eat it to cure one condition</strong> (an Ailment, a minor curse, a lingering fright)."), weight=0),

    # ---------- Already carried: reference entry ----------
    item("Staff of the Sunken Sanctum", notes(
        "<strong>Magic Silverwood Staff — d6 Bludgeoning damage, spellcasting focus.</strong> Tailored for Princess Marigold; claimed from the Sunken Sanctum's Guardian orb.",
        "<strong>Sanctuary Aegis:</strong> whenever Marigold heals an ally or spends a Heart Die, a water bubble grants the target +1 Armor for 1 round.",
        "<strong>Radiant Wave (1/Rest):</strong> strike the ground to release a 15-foot pulse — undead, oozes, and corrupted beasts take d6 Radiant damage and make a WITS test or are pushed back.",
        "<strong>Sacred Command Word: Aethelgard.</strong> Triggers Radiant Wave to purge shadow corruption and pacify corrupted guardians, per the established campaign item."),
        die="d6", weight=1, art="staff_sunken_sanctum.png"),
    item("Silver Rose Pin (Fairy Compass)", notes(
        "The PPS member's pin — designed long ago by the Society's founder. After Aurelius's blessing it acts as a <strong>Fairy Compass</strong>: it points toward Princess Amy no matter what body she is in, glows warm when moving toward her, cool when away, and <strong>flares red when she is in immediate danger</strong>.",
        "Its fixed reference lets this party navigate the shifting forest without a compulsory navigation test on each move. Recognition of a pin is not automatic trust or proof of the swap."),
        weight=0, art="silver_rose_pin.png"),

    # ---------- The Princess and the Dragon: story items ----------
    item("The Magic Necklaces", notes(
        "A paired gnomish enchantment swaps two wearers' bodies. Embra locked it with a separate key, preventing removal. Both wearers must be Nearby to use the key; unlock then remove both necklaces. Cave barrier is separate."), weight=0, art=None),
    item("The Gnomish Magical Key", notes(
        "An artifact that locks or unlocks the enchantment of the Magic Necklaces. Embra carries the intact original. Both wearers must be Nearby when it is used. Pippin can make a replacement: enchanted Pool water PLUS 50 SP, or a favor waiving the fee only. Water remains required."), weight=0),
    item("Magus Ulrik's Grimoire", notes(
        "Parsing this esoteric, arcane text requires a <strong>WITS test with disadvantage</strong>; failure causes Befuddlement. It details a recipe for a humanoid servant made from earth and blood — how Sir Damon was made."), weight=1, art=None),
    item("Tifa's Journal", notes(
        "Contains notes on how to cast the spell <strong>Animate</strong>. By Spending Time studying the journal, you can cast Animate with your own Gift Dice."), weight=1),
    item("Gem Apple", notes(
        "Crystalline fruit from the Scorchwoods orchard. Eating one makes you <em>feel weird</em> — and a gift of gem apples <strong>pacifies a knight captain</strong> (decreases the Knight Tracker by 1; living captains will not willingly repeat the trick). Sir Damon cannot be pacified by one; he is not alive. Magus Ulrik can be — but must be tricked into eating it. Fresh or candied fruit works on captains; the Wish Fish needs a fresh apple with a live worm. Fruit becomes dull stone outside the Scorchwoods."), weight=0),

    # ---------- The Princess and the Dragon: weapons & hoard ----------
    item("Crystal Dagger", notes(
        "<strong>d6 damage.</strong> A small enchanted dagger of purple crystal. On a 5–6 damage roll it inflicts an <strong>extra d6</strong> — and the blade shatters, becoming useless."), die="d6", weight=1, art=None),
    item("Sword of Starlight", notes(
        "<strong>d8 damage. 1 Gift Die.</strong> Lady Stella's family heirloom. Spend the die to take on an aura of starlight and force anyone fighting with the wielder (enemy or ally) to reroll a d20.",
        "<strong>Recharge:</strong> make a sincere wish on the evening star."), die="d8", weight=1),
    item("Blitzenaxt", notes(
        "<strong>d10 damage. 2 Gift Dice.</strong> Summon a bolt of lightning to add [SUM] damage to a successful attack made with Blitzenaxt.",
        "<strong>Recharge:</strong> leave it out during a powerful storm."), die="d10", weight=2),
    item("Dragonfire Shield", notes(
        "<strong>Reduce incoming damage by 1</strong> — unless the damage is dragon fire, in which case <strong>negate it completely</strong>; the shield absorbs and stores the fire.",
        "As a Reaction, release the stored fire: <strong>d6 damage to a Nearby target</strong>."), die="d6", weight=2),
    item("Cloak of Shadows", notes(
        "Virtue tests to remain unseen in dim light are made <strong>with advantage</strong>. When charged, activate to become <strong>completely invisible for d10 minutes</strong>.",
        "<strong>Recharge:</strong> wear the cloak while traveling under a new moon."), die="d10", weight=1),
    item("Spectacles of Discernment", notes(
        "Test <strong>with advantage</strong> to see hidden things, search areas, appraise items, and discern the true nature of things.",
        "Anything said while wearing them seems condescending and rubs people the wrong way."), weight=0),
    item("Swan's Grace Pendant", notes(
        "While wearing this necklace, your <strong>GRACE score is one point higher</strong>."), weight=0),
    item("Ring of Refraction", notes(
        "When charged, distorts the wearer's image in battle: an enemy targeting them specifically attacks <strong>with disadvantage</strong>. When an attack misses, the effect fades.",
        "<strong>Recharge:</strong> Spend Time staring into the ring's mirror — it reflects a grim, twisted version of the wearer, and staring causes Befuddlement."), weight=0),
    item("Ring of Fire", notes(
        "<strong>1 Gift Die.</strong> Casts <strong>Fireball</strong>.",
        "<strong>Recharge:</strong> leave it in the embers of a hot fire until they burn out."), weight=0),
    item("Pixie Dust", notes(
        "Sprinkle on yourself to gain the ability to cast a <strong>Float</strong> spell that lasts d4 hours."), die="d4", weight=0),
    item("Ring of Heart", notes(
        "A silver ring with a heart-shaped stone. Activate to instantly spend <strong>any number of your Heart Dice to recover HP as if you had a Picnic</strong>.",
        "Then lose all use of your Heart Dice until you rest for three days. Won from the ghastly knight commander at the Stones of Remembrance by honoring his sacrifice."), weight=0),
    item("Healing Potion", notes(
        "A standard restorative draught. <strong>Drink to recover d6 HP.</strong> Sir Raphael's party travels with d4 of them on Adagio the mule."), die="d6", weight=1),

    # ---------- Faire prizes & wares ----------
    item("Small Bag of Raspberry Candy", notes(
        "Four pieces of candy. <strong>Each instantly restores d4 HP.</strong>"), die="d4", weight=0, qty=4),
    item("Granny Bachmann's Miracle Elixir", notes(
        "A disgusting mixture of herbs and vegetables that <strong>cures any one Ailment</strong>. Once taken, you reek of rotten garlic for 24 hours. Bottle has d4 uses."), die="d4", weight=1),
    item("Friendship Bracelets", notes(
        "A set of matching bracelets — you choose the colors! The wearers can <strong>send telepathic messages to each other</strong>."), weight=0),
    item("Superb Glue", notes(
        "Holds anything in place; can only be unstuck by magical means. <strong>d6 uses.</strong>"), die="d6", weight=1),
    item("Picnic Basket", notes(
        "When used to have a Picnic, restores <strong>d4 extra HP</strong> to one person partaking."), die="d4", weight=1),
    item("Stuffed Toy Animal", notes(
        "Assorted animals (no dragons, of course). While clutching it, gain <strong>advantage on Virtue tests related to fear or disrupted sleep</strong>."), weight=1),
    item("Gnomish Trick Whistle", notes(
        "When blown, <strong>only those the holder chooses can hear</strong> its piercing sound. Range: Over Yonder."), weight=0),
    item("Toy Bubble Wand", notes(
        "Shoots a large stream of harmless bubbles. Works three times per day."), weight=0),
    item("Toy Sword Signed by Sir Finnian", notes(
        "Useless for fighting, but valuable to his fans. Sir Finnian will sign a second one for free."), weight=1),
    item("Artisan Perfume", notes(
        "A fine, alluring scent: roll GRACE tests to be charming <strong>with advantage for one hour</strong> (or until washed off). Also attracts every insect and animal in the area. Vial has d4 uses."), die="d4", weight=0),

    # ---------- The castle (house items) ----------
    item("Morwenna's Journal", notes(
        "Found in the frozen great hall of the old PPS headquarters. Entries in a warm, hopeful hand grow colder page by page as the Frostbind curse takes hold: <em>\"They say friendship conquers all. Why can't it conquer this?\"</em>",
        "The last entry: <em>\"I will prove it was always a lie.\"</em> Reading it Spends Time and reveals the save-her path — and one true thing about each of her four friends."), weight=1, art=None),
    item("The First Silver Rose Pin", notes(
        "Morwenna's own pin — the original, pinned beneath the thorns of her throne. Tarnished but whole.",
        "<em>House item:</em> its bearer has <strong>advantage on tests made to protect or comfort a friend</strong>, and the pin glows faintly in the presence of Frostbind magic. What it means to hand it back to her is up to the table."), weight=0, art="silver_rose_pin.png"),
]

# Foundry core icons for items without bespoke art (safe, always-present SVGs)
_ICON_OVERRIDES = {
    "Magus Ulrik's Grimoire": BOOK_ICON,
    "Tifa's Journal": BOOK_ICON,
    "Morwenna's Journal": BOOK_ICON,
    "Crystal Dagger": SWORD_ICON,
    "Sword of Starlight": SWORD_ICON,
    "Blitzenaxt": SWORD_ICON,
    "Toy Sword Signed by Sir Finnian": SWORD_ICON,
    "Dragonfire Shield": SHIELD_ICON,
}
for _it in ITEMS:
    if _it["name"] in _ICON_OVERRIDES and _it["img"] == "icons/svg/item-bag.svg":
        _it["img"] = _ICON_OVERRIDES[_it["name"]]

SCENES = [
    scene("Stump Entrance", "scenes/stump_entrance_scene.png"),
    scene("Scorchwoods — The Road Beyond", "scenes/scorchwoods_conclusion_scene.png"),
    scene("The Scorchwoods (Overworld)", "maps/scorchwoods_map.jpg"),
    scene("Brokenhill Silver Mine", "maps/brokenhill_mine.jpg"),
    scene("Dragon Cave Lair", "scenes/scorchwoods_dragon_cave_scene.png"),
    scene("Knight Camp", "scenes/knight_camp_scene.png"),
    scene("The Boneyard", "scenes/boneyard_scene.png"),
    scene("Snapdragon Field", "scenes/snapdragon_field_scene.png"),
    scene("Crystal Orchard", "scenes/crystal_orchard_scene.png"),
    scene("Enchanted Pool", "scenes/enchanted_pool_scene.png"),
    scene("Gnome Village", "scenes/gnome_village_scene.png"),
    scene("Stones of Remembrance", "scenes/stones_of_remembrance_scene.png"),
    scene("Abandoned Cottage", "scenes/abandoned_cottage_scene.png"),
    scene("Castle Approach", "scenes/castle_approach_scene.png"),
    scene("Castle Great Hall", "scenes/castle_great_hall_scene.png"),
    scene("Castle Throne Room", "scenes/castle_throne_scene.png"),
]

# Rosehold: six dungeon-crawl levels with walls, doors, lights and GM-only room labels.
for _lv in rosehold_scenes.LEVELS:
    _w, _h = png_size(os.path.join(ROOT, "build", "art", _lv["art"]))
    SCENES.append(rosehold_scenes.build_scene(_lv, did(_lv["name"], "scene"), _w, _h, MODULE_ID))


for document in ACTORS + ITEMS + SCENES:
    document["ownership"] = {"default": 0}
for document in ACTORS:
    if document["name"] == "Princess Embra (Impostor)":
        document["prototypeToken"]["name"] = "Princess Amy"
        document["prototypeToken"]["displayName"] = 0


def emit(docs, sub):
    out = os.path.join(ROOT, "build", "src", sub)
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    for d in docs:
        with open(os.path.join(out, f"{slug(d['name'])}.json"), "w", encoding="utf-8") as fh:
            json.dump(d, fh, indent=2, ensure_ascii=False)
    print(f"{sub}: {len(docs)} documents")

if __name__ == "__main__":
    names = [a["name"] for a in ACTORS]
    assert len(names) == len(set(names)), "duplicate actor names"
    missing = [a["name"] for a in ACTORS
               if a["img"].startswith("modules/") and
               not os.path.exists(os.path.join(ROOT, "build", "art", "portraits", os.path.basename(a["img"])))]
    assert not missing, f"missing art: {missing}"
    no_token = [a["name"] for a in ACTORS
                if a["prototypeToken"]["texture"]["src"].startswith("modules/") and
                not os.path.exists(os.path.join(ROOT, "build", "art", "tokens",
                                                os.path.basename(a["prototypeToken"]["texture"]["src"])))]
    assert not no_token, f"missing tokens (run tools/make_tokens.py): {no_token}"
    inames = [i["name"] for i in ITEMS]
    assert len(inames) == len(set(inames)), "duplicate item names"
    no_item_art = [i["name"] for i in ITEMS
                   if i["img"].startswith("modules/") and
                   not os.path.exists(os.path.join(ROOT, "build", "art", "items", os.path.basename(i["img"])))]
    assert not no_item_art, f"missing item art: {no_item_art}"
    emit(ACTORS, "actors")
    emit(ITEMS, "items")
    emit(SCENES, "scenes")
