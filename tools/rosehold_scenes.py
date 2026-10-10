#!/usr/bin/env python3
"""Rosehold (Queen Morwenna's castle): six dungeon-crawl scenes with walls, doors and lights.

Geometry was measured by eye from the 1536-px painted originals (wall centrelines),
so every coordinate below is in that 1536-px frame and is multiplied by the scene's
scale (4 for the shipped 6144-px maps) when the scene is built. Expect to nudge a
few walls in Foundry: the paintings are not pixel-exact.

Each level is described by:
  boxes    rooms and passages as (x1, y1, x2, y2); their edges become walls,
           shared edges are merged
  doors    (x1, y1, x2, y2, kind) lying on a box edge; kind is one of
           door | locked | secret | open   ("open" is a doorway with no leaf)
  extra    free segments (x1, y1, x2, y2, kind); kind is one of
           wall | cliff (blocks movement only) | bars (blocks movement, not sight)
           | door | locked | secret | barsdoor
  lights   (x, y, dim_ft, bright_ft, colour, animation)
  labels   GM-only text: (x, y, text)
"""
import hashlib, math

WARM, FIRE, COLD, VIOLET, ROSE = "#ffb066", "#ff7733", "#88ccff", "#aa66ff", "#ff88aa"


def _ellipse(cx, cy, rx, ry, gap_from, gap_to, steps=20):
    """Wall segments round an ellipse, leaving a gap between two angles (degrees, y down)."""
    pts, a = [], gap_to
    span = 360 - (gap_to - gap_from)
    for i in range(steps + 1):
        t = math.radians(gap_to + span * i / steps)
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    return [(*pts[i], *pts[i + 1], "wall") for i in range(steps)]


def _pillar(cx, cy, r=20):
    return [(cx - r, cy - r, cx + r, cy - r, "wall"), (cx + r, cy - r, cx + r, cy + r, "wall"),
            (cx + r, cy + r, cx - r, cy + r, "wall"), (cx - r, cy + r, cx - r, cy - r, "wall")]


LEVELS = [
    dict(
        name="Rosehold 0 — The Thornwall", art="maps/map_rosehold_0_thornwall.webp", grid=137, darkness=0.25,
        boxes=[(540, 35, 958, 245)],
        doors=[(700, 35, 770, 35, "door"), (700, 245, 770, 245, "locked")],
        extra=[
            # cliff edges: stop tokens walking into the void, do not block sight
            (478, 368, 478, 245, "cliff"), (478, 245, 540, 245, "cliff"), (958, 245, 1020, 245, "cliff"),
            (1020, 245, 1020, 368, "cliff"), (1020, 368, 845, 368, "cliff"), (845, 368, 845, 755, "cliff"),
            (845, 755, 1082, 755, "cliff"), (1082, 755, 1082, 980, "cliff"), (1082, 980, 400, 980, "cliff"),
            (400, 980, 400, 755, "cliff"), (400, 755, 655, 755, "cliff"), (655, 755, 655, 368, "cliff"),
            (655, 368, 478, 368, "cliff"),
            # the Barrier of Thorns: solid either side, a locked "door" across the breach
            (478, 305, 690, 305, "wall"), (815, 305, 1020, 305, "wall"), (690, 305, 815, 305, "locked"),
        ],
        lights=[(640, 115, 25, 12, WARM, "torch"), (918, 128, 15, 8, WARM, "torch"), (662, 855, 30, 15, FIRE, "torch"),
                (968, 888, 30, 15, FIRE, "torch"), (440, 850, 12, 6, WARM, "torch")],
        labels=[(410, 765, "A1 Muster"), (665, 560, "A2 Causeway"), (700, 312, "A3 Barrier (locked door: open when it shatters)"),
                (550, 45, "A4 Gatehouse"), (700, 15, "to Level 1")],
    ),
    dict(
        name="Rosehold 1 — The Outer Ward", art="maps/map_rosehold_1_outer_ward.webp", grid=120, darkness=0.0,
        boxes=[(128, 35, 1438, 1000), (162, 68, 490, 230), (585, 68, 953, 290), (1172, 68, 1405, 232),
               (162, 270, 495, 568), (162, 605, 495, 940), (1048, 268, 1405, 782), (1048, 825, 1405, 970),
               (648, 815, 892, 968)],
        doors=[(305, 230, 358, 230, "door"), (740, 290, 800, 290, "door"), (1235, 232, 1290, 232, "door"),
               (495, 395, 495, 450, "door"), (495, 742, 495, 798, "door"), (1048, 500, 1048, 558, "door"),
               (740, 815, 800, 815, "door"), (892, 880, 892, 938, "door"), (1048, 880, 1048, 938, "door"),
               (490, 120, 490, 170, "secret"), (128, 860, 128, 910, "secret")],
        extra=[],
        lights=[(430, 160, 10, 5, FIRE, "torch")],
        labels=[(660, 825, "A4 Gatehouse (from Level 0)"), (520, 340, "B1 Court of Frozen Fountains"), (172, 615, "B2 Kennels"),
                (172, 280, "B3 Stables"), (1058, 278, "B4 Briar Court"), (1058, 835, "B5 Barracks (door not painted)"),
                (172, 78, "B6 Armory (secret door east)"), (1182, 78, "B7 Raven Tower"), (595, 78, "C1 Keep Steps: UP to Level 2"),
                (20, 880, "postern (secret)")],
    ),
    dict(
        name="Rosehold 2 — The Hall of the Rose", art="maps/map_rosehold_2_hall_of_the_rose.webp", grid=128, darkness=0.2,
        boxes=[(143, 58, 443, 310), (546, 58, 990, 310), (1092, 58, 1392, 310), (143, 310, 448, 765),
               (448, 310, 1092, 765), (1092, 310, 1392, 765), (612, 765, 925, 958), (443, 150, 546, 222)],
        doors=[(258, 310, 318, 310, "door"), (738, 310, 800, 310, "door"), (1220, 310, 1278, 310, "door"),
               (448, 478, 448, 545, "door"), (1092, 478, 1092, 545, "door"), (728, 765, 808, 765, "locked"),
               (733, 958, 803, 958, "door"), (443, 150, 443, 222, "secret"), (546, 150, 546, 222, "open")],
        extra=[],
        lights=[(1230, 95, 30, 15, FIRE, "torch"), (1265, 165, 15, 8, WARM, "torch"), (1125, 400, 12, 5, COLD, "pulse"),
                (1365, 400, 12, 5, COLD, "pulse"), (1125, 660, 12, 5, COLD, "pulse"), (1365, 660, 12, 5, COLD, "pulse")],
        labels=[(622, 775, "C1 Vestibule (Oath Door: locked)"), (458, 320, "C2 Great Hall"), (1102, 320, "C3 Banquet Hall"),
                (1102, 68, "C4 Kitchens (warm room; dumbwaiter)"), (153, 320, "C5 Hall of Portraits"),
                (153, 68, "C6 Servants' Stair: DOWN to Undercroft"), (556, 68, "C7 Grand Stair: UP to Level 3"),
                (452, 160, "secret passage"), (700, 968, "to Level 1")],
    ),
    dict(
        name="Rosehold U — The Undercroft", art="maps/map_rosehold_u_undercroft.webp", grid=137, darkness=0.5,
        boxes=[(135, 247, 358, 470), (208, 470, 268, 522), (84, 522, 466, 940), (466, 688, 516, 748),
               (516, 622, 986, 940), (652, 572, 712, 622), (516, 310, 822, 572), (692, 258, 748, 310),
               (822, 412, 872, 470), (872, 310, 1414, 572), (1172, 572, 1240, 650), (1043, 650, 1414, 940),
               (986, 752, 1043, 808)],
        doors=[(208, 470, 268, 470, "door"), (208, 522, 268, 522, "open"), (466, 688, 466, 748, "open"),
               (516, 688, 516, 748, "door"), (652, 572, 712, 572, "door"), (652, 622, 712, 622, "open"),
               (692, 310, 748, 310, "locked"), (692, 258, 748, 258, "open"), (822, 412, 822, 470, "door"),
               (872, 412, 872, 470, "open"), (1172, 572, 1240, 572, "secret"), (1172, 650, 1240, 650, "open"),
               (986, 752, 986, 808, "open"), (1043, 752, 1043, 808, "locked")],
        extra=(
            _ellipse(752, 130, 160, 108, 78, 102)
            + [(785, 236, 748, 258, "wall"), (719, 236, 692, 258, "wall"),
               # cell block: bars block movement, not sight; each cell front is a locked barred door
               (675, 632, 675, 737, "bars"), (825, 632, 825, 737, "bars"), (675, 805, 675, 930, "bars"),
               (825, 805, 825, 930, "bars"),
               (526, 737, 675, 737, "barsdoor"), (675, 737, 825, 737, "barsdoor"), (825, 737, 976, 737, "barsdoor"),
               (526, 805, 675, 805, "barsdoor"), (675, 805, 825, 805, "barsdoor"), (825, 805, 976, 805, "barsdoor")]
        ),
        lights=[(160, 275, 20, 10, WARM, "torch"), (330, 275, 20, 10, WARM, "torch"), (115, 557, 20, 10, WARM, "torch"),
                (435, 557, 20, 10, WARM, "torch"), (110, 730, 20, 10, WARM, "torch"), (562, 355, 20, 10, WARM, "torch"),
                (710, 450, 15, 8, WARM, "torch"), (795, 530, 20, 10, WARM, "torch"), (898, 342, 20, 10, WARM, "torch"),
                (1385, 342, 20, 10, WARM, "torch"), (582, 645, 15, 8, WARM, "torch"), (745, 645, 15, 8, WARM, "torch"),
                (886, 645, 15, 8, WARM, "torch"), (1075, 680, 20, 10, WARM, "torch"), (1383, 680, 20, 10, WARM, "torch"),
                (1073, 893, 20, 10, WARM, "torch"), (1385, 893, 20, 10, WARM, "torch"), (652, 72, 15, 8, WARM, "torch"),
                (850, 68, 15, 8, WARM, "torch"), (637, 197, 15, 8, WARM, "torch"), (866, 197, 15, 8, WARM, "torch"),
                (1218, 790, 15, 5, VIOLET, "pulse")],
        labels=[(145, 257, "D0 Stair: UP to C6"), (94, 532, "D1 Cistern (Bannik's tunnel, SW corner)"), (526, 760, "D2 Cold Cells"),
                (526, 320, "D3 Jailer's Guardroom (dumbwaiter)"), (882, 320, "D4 Crypt"), (1053, 660, "D5 Relic Vault (glyph on west door)"),
                (600, 20, "D6 Frostbind Well (thorn-sealed: locked)"), (1250, 600, "secret")],
    ),
    dict(
        name="Rosehold 3 — The Galleries", art="maps/map_rosehold_3_galleries.webp", grid=128, darkness=0.2,
        boxes=[(143, 42, 537, 325), (577, 42, 966, 325), (1005, 42, 1397, 512), (143, 365, 537, 935),
               (577, 365, 966, 678), (577, 678, 966, 935), (1005, 555, 1397, 935),
               (537, 142, 577, 198), (312, 325, 372, 365), (742, 325, 800, 365), (537, 460, 577, 518),
               (966, 428, 1005, 486), (537, 750, 577, 808), (966, 750, 1005, 808)],
        doors=[(537, 142, 537, 198, "secret"), (577, 142, 577, 198, "open"), (312, 325, 372, 325, "door"),
               (312, 365, 372, 365, "open"), (742, 325, 800, 325, "door"), (742, 365, 800, 365, "open"),
               (537, 460, 537, 518, "door"), (577, 460, 577, 518, "open"), (966, 428, 966, 486, "open"),
               (1005, 428, 1005, 486, "door"), (740, 678, 800, 678, "door"), (537, 750, 537, 808, "door"),
               (577, 750, 577, 808, "open"), (966, 750, 966, 808, "open"), (1005, 750, 1005, 808, "door")],
        extra=[
            # the Luminaries' Rooms: corridor walls and bedroom partitions
            (1168, 42, 1168, 95, "wall"), (1168, 95, 1168, 140, "door"), (1168, 140, 1168, 250, "wall"),
            (1168, 250, 1168, 295, "door"), (1168, 295, 1168, 400, "wall"), (1168, 400, 1168, 445, "door"),
            (1168, 445, 1168, 512, "wall"), (1005, 190, 1168, 190, "wall"), (1005, 338, 1168, 338, "wall"),
            (1282, 42, 1282, 130, "wall"), (1282, 130, 1282, 175, "door"), (1282, 175, 1282, 370, "wall"),
            (1282, 370, 1282, 415, "door"), (1282, 415, 1282, 512, "wall"), (1282, 265, 1397, 265, "wall"),
        ],
        lights=[(1220, 105, 35, 18, FIRE, "torch"), (350, 195, 15, 5, VIOLET, "pulse")]
               + [(1048 + 60 * i, 640, 8, 3, "#ff4422", "pulse") for i in range(6)],
        labels=[(587, 688, "E7 Upper Landing: DOWN to C7"), (587, 375, "E1 Gallery of Mirrors"), (153, 375, "E2 Map Room & Library"),
                (1015, 565, "E3 Ulrik's Workshop"), (1015, 52, "E4 Luminaries' Rooms (warm room)"), (153, 52, "E5 Winter Conservatory"),
                (587, 52, "E6 Queen's Solar: UP to Spire; dumbwaiter"), (540, 120, "secret")],
    ),
    dict(
        name="Rosehold 4 — The Frozen Spire", art="maps/map_rosehold_4_frozen_spire.webp", grid=128, darkness=0.0,
        boxes=[(133, 246, 885, 670), (885, 345, 990, 585), (266, 670, 755, 985), (387, 985, 637, 1276)],
        doors=[(472, 670, 545, 670, "door"), (472, 985, 545, 985, "door"), (885, 400, 885, 490, "locked")],
        extra=_pillar(305, 345) + _pillar(375, 285) + _pillar(650, 285) + _pillar(722, 345),
        lights=[(510, 300, 25, 8, "#66aaff", "pulse"), (885, 445, 15, 5, ROSE, "pulse")],
        labels=[(397, 995, "F1 Stair of Vows: DOWN to E6"), (276, 680, "F2 Antechamber"), (143, 256, "F3 Throne Room"),
                (895, 320, "F4 Rose Window (iced shut: locked)"), (250, 375, "Vow Pillars x4")],
    ),
]

# ---- wall construction -------------------------------------------------------------------

SENSE = {  # move, sight, light, sound, door, door state
    "wall": (20, 20, 20, 20, 0, 0),
    "cliff": (20, 0, 0, 0, 0, 0),
    "bars": (20, 0, 0, 0, 0, 0),
    "door": (20, 20, 20, 20, 1, 0),
    "locked": (20, 20, 20, 20, 1, 2),
    "secret": (20, 20, 20, 20, 2, 0),
    "barsdoor": (20, 0, 0, 0, 1, 2),
}
SNAP = 6


def _merge(intervals):
    out = []
    for a, b in sorted(intervals):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def _subtract(intervals, cuts):
    for ca, cb in cuts:
        nxt = []
        for a, b in intervals:
            if cb <= a or ca >= b:
                nxt.append([a, b])
                continue
            if ca > a:
                nxt.append([a, ca])
            if cb < b:
                nxt.append([cb, b])
        intervals = nxt
    return intervals


def build_segments(level):
    """Return [(x1, y1, x2, y2, kind)] in 1536-frame coordinates."""
    horiz, vert = {}, {}  # line coordinate -> list of intervals
    for x1, y1, x2, y2 in level["boxes"]:
        horiz.setdefault(y1, []).append((x1, x2)); horiz.setdefault(y2, []).append((x1, x2))
        vert.setdefault(x1, []).append((y1, y2)); vert.setdefault(x2, []).append((y1, y2))
    hcuts, vcuts, segs = {}, {}, []
    for x1, y1, x2, y2, kind in level["doors"]:
        if y1 == y2:
            line = min(horiz, key=lambda k: abs(k - y1))
            assert abs(line - y1) <= SNAP, (level["name"], "door off any wall", (x1, y1, x2, y2))
            a, b = sorted((x1, x2)); hcuts.setdefault(line, []).append((a, b))
            if kind != "open":
                segs.append((a, line, b, line, kind))
        else:
            line = min(vert, key=lambda k: abs(k - x1))
            assert abs(line - x1) <= SNAP, (level["name"], "door off any wall", (x1, y1, x2, y2))
            a, b = sorted((y1, y2)); vcuts.setdefault(line, []).append((a, b))
            if kind != "open":
                segs.append((line, a, line, b, kind))
    for y, iv in horiz.items():
        for a, b in _subtract(_merge(iv), hcuts.get(y, [])):
            segs.append((a, y, b, y, "wall"))
    for x, iv in vert.items():
        for a, b in _subtract(_merge(iv), vcuts.get(x, [])):
            segs.append((x, a, x, b, "wall"))
    return segs + list(level["extra"])


def _id(*parts):
    return hashlib.sha1(":".join(str(p) for p in parts).encode()).hexdigest()[:16]


def build_scene(level, scene_id, width, height, module_id, base=1536, portrait_base=1024):
    """Full Foundry scene document for one level. Scale is derived from the real image width."""
    s = width / (portrait_base if height > width else base)
    grid = level["grid"]
    walls = []
    for n, (x1, y1, x2, y2, kind) in enumerate(build_segments(level)):
        move, sight, light, sound, door, ds = SENSE[kind]
        wid = _id(scene_id, "wall", n)
        walls.append({"_id": wid, "c": [round(x1 * s), round(y1 * s), round(x2 * s), round(y2 * s)],
                      "move": move, "sight": sight, "light": light, "sound": sound, "dir": 0,
                      "door": door, "ds": ds, "flags": {}, "_key": f"!scenes.walls!{scene_id}.{wid}"})
    lights = []
    for n, (x, y, dim, bright, colour, anim) in enumerate(level["lights"]):
        lid = _id(scene_id, "light", n)
        lights.append({"_id": lid, "x": round(x * s), "y": round(y * s), "rotation": 0, "walls": True, "vision": False,
                       "hidden": False,
                       "config": {"dim": dim, "bright": bright, "color": colour, "alpha": 0.4, "angle": 360,
                                  "animation": {"type": anim, "speed": 3, "intensity": 3}},
                       "flags": {}, "_key": f"!scenes.lights!{scene_id}.{lid}"})
    drawings = []
    for n, (x, y, text) in enumerate(level["labels"]):
        did = _id(scene_id, "label", n)
        drawings.append({"_id": did, "x": round(x * s), "y": round(y * s),
                         "shape": {"type": "r", "width": round((len(text) * 30 + 60) * s / 4), "height": round(24 * s)},
                         "text": text, "fontSize": 48, "textColor": "#ffe066", "textAlpha": 1,
                         "fillType": 0, "strokeWidth": 0, "strokeAlpha": 0, "hidden": True, "locked": True,
                         "flags": {}, "_key": f"!scenes.drawings!{scene_id}.{did}"})
    return {
        "_id": scene_id, "name": level["name"], "active": False, "navigation": False,
        "background": {"src": f"modules/{module_id}/art/{level['art']}"},
        "width": width, "height": height, "padding": 0, "backgroundColor": "#000000",
        "grid": {"type": 1, "size": grid, "distance": 5, "units": "ft"},
        "tokenVision": True, "fog": {"exploration": True},
        "environment": {"darknessLevel": level["darkness"],
                        "globalLight": {"enabled": True, "darkness": {"min": 0, "max": 1}}},
        "walls": walls, "lights": lights, "drawings": drawings,
        "_key": f"!scenes!{scene_id}",
    }


if __name__ == "__main__":
    for lv in LEVELS:
        segs = build_segments(lv)
        kinds = {}
        for *_, k in segs:
            kinds[k] = kinds.get(k, 0) + 1
        print(lv["name"], len(segs), kinds, "lights", len(lv["lights"]))
