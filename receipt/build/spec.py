"""Shared layout spec for the Dinner receipt strips.

One description per strip, rendered twice: to HTML (build_html.py) and to an
Illustrator script with live, editable type (build_jsx.py). Sizes are in cqw,
i.e. percent of the paper width, so both renderers scale them the same way.
"""

# --- type scale --------------------------------------------------------------------------------
# size (cqw), weight, leading, tracking (em), all caps
# Set in Wix Madefor Text, spaced the way the poster is. Measured off the poster against the
# font's own advances and kerning: COLORBLOCK in capitals runs at about +0.17 em, the mixed-case
# names, date and address at about +0.01 em in SemiBold, lists at about 1.1 leading. So: every
# capital line gets +0.17 em, every mixed-case line +0.01 em, kerning stays the font's own.
STYLES = {
    "micro":      (3.2, 600, 1.20, 0.010, False),
    "microCaps":  (3.2, 600, 1.20, 0.170, True),
    "body":       (4.2, 600, 1.15, 0.010, False),
    "bodyStrong": (4.2, 700, 1.15, 0.010, False),
    "bodyCaps":   (4.2, 600, 1.15, 0.170, True),
    "sub":        (5.6, 600, 1.10, 0.010, False),
    "subCaps":    (5.2, 600, 1.10, 0.170, True),
    "brand":      (6.0, 600, 1.10, 0.170, True),
    "name":       (8.4, 600, 1.10, 0.010, False),
    "title":      (8.0, 600, 1.10, 0.010, False),
    "titleCaps":  (8.0, 600, 1.10, 0.170, True),
    "vinfo":      (9.6, 600, 1.10, 0.010, False),
    "side":       (9.0, 600, 1.00, 0.170, True),
    "display":    (13.0, 600, 1.00, 0.010, False),
    "huge":       (17.0, 600, 0.95, 0.010, False),
    "flow":       (3.1, 500, 1.30, 0.010, False),
    "flowBold":   (3.1, 700, 1.30, 0.010, False),
    "sign":       (4.8, 600, 1.20, 0.170, True),
    "stars":      (4.2, 600, 1.00, 0.600, False),
}

# everything black on the lemon paper of the runner
INK = "#000000"
LEMON = "#feed95"

LINEUP = ["Tanya Andrianova", "Igor Zotov", "Andrey Lee", "Sasha Chernikov", "Sophia Zhuravkova"]

NB = " "    # no-break space: keeps numbers with their words
THIN = " "  # thin space: around × in quantities
NBH = "‑"   # non-breaking hyphen: Line-up never splits

DATE = f"10{NB}oct{NB}2026"
ADDR = f"Samokatnaya{NB}4s53"
VENUE = f"DNA{NB}Kitchen"
LINE_UP = f"Line{NBH}up"


def T(style, text, align="left", mt=0, **kw):
    return dict(t="text", style=style, lines=text.split("\n"), align=align, mt=mt, **kw)


def ROW(style, left, right, mt=0, indent=0):
    return dict(t="row", style=style, left=left, right=right, mt=mt, indent=indent)


def RULE(kind="dash", mt=4.6, mb=4.6):
    return dict(t="rule", kind=kind, mt=mt, mb=mb)


def WM(orient="v", width=60, mt=0, mb=0, align="center"):
    return dict(t="wordmark", orient=orient, width=width, mt=mt, mb=mb, align=align)


def COLLAB(style="brand", mt=0):
    return dict(t="collab", style=style, mt=mt)


def BARCODE(width=78, digits=True, height=None, mt=0):
    return dict(t="barcode", width=width, digits=digits, height=height, mt=mt)


def LIST(style, items, numbered=False, qty=None, num_style="micro", mt=0, ruled=False, prefix=None):
    return dict(t="list", style=style, items=items, numbered=numbered, qty=qty,
                num_style=num_style, mt=mt, ruled=ruled, prefix=prefix)


def FLOW(text, repeat, mt=0):
    return dict(t="flow", text=text, repeat=repeat, mt=mt)


# --- the strips ---------------------------------------------------------------------------------

def classic(caps, theme):
    """The first receipt: classic till layout. caps=True is the original thermal version."""
    b = "bodyCaps" if caps else "body"
    m = "microCaps" if caps else "micro"
    return [
        COLLAB(),
        WM("v", 62 if caps else 60, mt=7),
        ROW(b, "Check no.", "0001", mt=6),
        ROW(b, "Date", DATE),
        ROW(b, "Start", "18:00"),
        RULE(),
        T(m, "Venue"),
        T("subCaps" if caps else "sub", f"{VENUE}\n{ADDR}", mt=0.6),
        RULE(),
        ROW(m, LINE_UP, "Qty"),
        LIST(b, LINEUP, numbered=True, qty="1", num_style=m, mt=1.6),
        RULE(),
        ROW(b, "Items", "5"),
        ROW("titleCaps" if caps else "title", "Total", "Dinner", mt=1.8),
        RULE("double", mt=3.6, mb=6),
        BARCODE(78),
        T("sign" if caps else "sub", "Thank you", "center", mt=8),
    ] + ([T("stars", "***", "center", mt=1.4)] if caps else [])


STRIPS = {
    "index": dict(
        title="Dinner Receipt", width_px=380, width_mm=80, edge="torn",
        paper=LEMON, ink=INK, pad=(10.2, 7.5, 12.2),
        blocks=classic(True, "paper"),
    ),
    "classic": dict(
        title="Dinner Classic Receipt", width_px=380, width_mm=80, edge="torn",
        paper=LEMON, ink=INK, pad=(11.2, 7.5, 13.2),
        blocks=classic(False, "paper"),
    ),
    "poster": dict(
        title="Dinner Poster Strip", width_px=380, width_mm=80, edge="torn",
        paper=LEMON, ink=INK, pad=(12.2, 8, 14.2),
        blocks=[
            dict(t="hero", wm_width=62, side=["COLORBLOCK", "×", "DNA"], mt=0),
            dict(t="vtext", style="vinfo", lines=[LINE_UP] + LINEUP, mt=12),
            dict(t="vtext", style="vinfo", lines=[DATE, ADDR, VENUE, "18:00"], mt=10),
        ],
    ),
    "tickets": dict(
        title="Dinner Ticket Roll", width_px=340, width_mm=72, edge="stubs",
        paper=LEMON, ink=INK, pad=(8, 9, 8),
        stubs=[
            dict(blocks=[
                ROW("microCaps", "Colorblock × DNA", f"No.{NB}0001"),
                WM("h", 100, mt=6),
                ROW("micro", "Admit one", "Keep this stub", mt=5),
            ]),
            dict(blocks=[
                ROW("micro", "Saturday", "Start"),
                T("huge", f"10{NB}oct\n2026", mt=2),
                ROW("title", "", "18:00", mt=1),
            ]),
            dict(blocks=[
                T("micro", "Venue"),
                T("name", VENUE, mt=0.6),
                T("body", ADDR, mt=0.6),
            ]),
        ] + [
            dict(compact=True, blocks=[
                ROW("micro", LINE_UP, f"0{i}{NB}/{NB}05"),
                T("name", n, mt=1.6),
            ]) for i, n in enumerate(LINEUP, 1)
        ] + [
            dict(blocks=[
                BARCODE(100, digits=False, height=16),
                ROW("micro", f"2{NB}026101{NB}018001", f"10.10{NB}·{NB}18:00", mt=2),
            ]),
        ],
    ),
    "order": dict(
        title="Dinner Order Ticket", width_px=380, width_mm=80, edge="torn",
        paper=LEMON, ink=INK, pad=(10.2, 6.5, 11.2),
        blocks=[
            dict(t="columns", left=35, gap=5, right=[
                [
                    T("micro", "Order"),
                    T("title", "#0001", mt=0.4),
                    RULE(mt=3.6, mb=3.6),
                    ROW("body", "Table", "All"),
                    ROW("body", "Date", "10.10.26"),
                    ROW("body", "Fire", "18:00"),
                    RULE(mt=3.6, mb=3.6),
                    T("micro", LINE_UP),
                    LIST("body", LINEUP, prefix="1×", mt=1.2),
                ],
                [
                    RULE(mt=3.6, mb=3.6),
                    T("micro", f"{VENUE}\n{ADDR}"),
                    BARCODE(100, digits=False, height=12, mt=3),
                ],
            ]),
            RULE(),
            COLLAB(mt=1.4),
        ],
    ),
    "fiscal": dict(
        title="Dinner Fiscal Receipt", width_px=300, width_mm=57, edge="torn", lang="ru",
        paper=LEMON, ink=INK, pad=(11.6, 7, 15.6), scale=1.08,
        blocks=[
            WM("h", 100),
            COLLAB(mt=5),
            T("body", VENUE, "center", mt=0.4),
            T("body", f"Москва, Самокатная{NB}4с53", "center"),
            RULE("thin", mt=3, mb=3),
            T("title", "Кассовый чек", "center"),
            T("bodyStrong", "Приход", "center", mt=0.4),
            RULE("thin", mt=3, mb=3),
            ROW("body", "Чек", f"№{NB}0001"),
            ROW("body", "Дата", "10.10.26"),
            ROW("body", "Время", "18:00"),
            ROW("body", "Кассир", "Colorblock"),
            RULE("thin", mt=3, mb=3),
            T("bodyStrong", "1. Dinner"),
            ROW("body", f"1{THIN}×{THIN}10.10", "=10.10", indent=6),
        ] + sum([[
            T("bodyStrong", f"{i}. {LINE_UP}: {n}", mt=2.4),
            ROW("body", f"1{THIN}×{THIN}1", "=1", indent=6),
        ] for i, n in enumerate(LINEUP, 2)], []) + [
            RULE("thinDouble", mt=3, mb=3),
            ROW("title", "Итого", "=Dinner"),
            RULE("thinDouble", mt=3, mb=3),
            ROW("body", "Позиций", "6"),
            ROW("body", "Место расчётов", VENUE),
            dict(t="qr", width=52, mt=6),
            T("bodyStrong", "Спасибо за визит", "center", mt=4),
        ],
    ),
    "runner": dict(
        title="Dinner Table Runner", width_px=380, width_mm=80, edge="torn",
        paper=LEMON, ink=INK, pad=(9.2, 6, 9.2),
        blocks=[
            WM("h", 100, mt=2),
            FLOW("unit", 5, mt=5),
            T("display", DATE, "center", mt=5),
            FLOW("unit", 4, mt=4),
            T("display", "18:00", "center", mt=5),
            FLOW("unit", 5, mt=4),
            LIST("name", LINEUP, ruled=True, mt=6),
            FLOW("unit", 4, mt=6),
            WM("v", 46, mt=8),
            FLOW("unit", 5, mt=8),
            T("display", VENUE, "center", mt=5),
            FLOW("unit", 4, mt=4),
            WM("h", 100, mt=5),
        ],
    ),
}

# the runner's repeating sentence; **bold** runs are set in flowBold
FLOW_UNIT = (f"COLORBLOCK × DNA{NB}– **Dinner**{NB}– {DATE}{NB}– 18:00{NB}– {VENUE}{NB}– {ADDR}{NB}– "
             f"{LINE_UP}: " + ", ".join(f"**{n.replace(' ', NB)}**" for n in LINEUP) + f"{NB}– ")

# order the files are laid out in Illustrator, left to right
ORDER = ["index", "classic", "poster", "tickets", "order", "fiscal", "runner"]
