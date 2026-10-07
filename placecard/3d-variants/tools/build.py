"""Assemble the 3D viewer site: data/<set>.json (fold specs with sizes), tex/<set>/*.webp,
plus index.html, fold.js and scene.js.

    python3 build.py SITE_DIR SET_DIR [SET_DIR ...]

Each SET_DIR holds final/ (SVGs + index.json) and fold3d/ (one spec per SVG).
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

SETS = {"system": "Система", "fold": "Сгиб", "edge": "Край", "optic": "Оптика"}
# rank (as the authors ranked them), name, one line for the index
DESIGNS = {
    "system": [("v2_wrap", "Wrap", "Створки углом к гостю, имя одной строкой переходит через ребро."),
               ("v4_receipt_mass", "Receipt Mass", "Домик: имя и фамилия на всю ширину, строка как в чеке."),
               ("v5_lineup_band", "Line-up Band", "Пять домиков в ряд, общая полоса через все карточки."),
               ("v1_downstream", "Downstream", "Имя вертикально, как DINNER на афише, уходит на ножку."),
               ("v3_concertina", "Concertina", "Гармошка: одна буква на грань."),
               ("v6_quiet_lockup", "Quiet Lockup", "Крупно COLORBLOCK × DNA, имя мелко на ножке.")],
    "fold": [("ridge", "Ridge", "Низкий домик: строка собирается на коньке, сзади тянется потёками."),
             ("napkin-flag", "Napkin flag", "Флажок из кольца салфетки, фамилия ложится на рулон."),
             ("crenel", "Crenel", "Шесть ступенчатых полос: имя собирается только с места гостя."),
             ("elbow", "Elbow", "Одна складка, имя через сгиб."),
             ("slope", "Slope", "Клин: имя на скате, выпрямляется в руках."),
             ("bridge", "Bridge", "Фамилия снизу полки, читается в зеркальной плитке.")],
    "edge": [("e1-overhang", "Overhang", "Буквы стоят над сгибом, фамилия свисает за края."),
             ("e6-drip", "Drip", "Фамилия свисает с полосы отдельными буквами."),
             ("e5-pop", "Pop-up", "Имя откинуто вверх, в карточке остаётся окно букв."),
             ("e2-halo", "Halo", "Карточка вырезана по контуру имени."),
             ("e3-bend", "Bend", "Огромные буквы перегибаются через тарелку."),
             ("e4-slot", "Slot", "Лента с именем выходит из-под тарелки через прорезь.")],
    "optic": [("v4_vault", "Vault", "Карточка аркой, имя искажено и читается с места ровно."),
              ("v1_standup", "Standup", "Плоская карточка, имя будто встаёт над столом."),
              ("v6_runway", "Runway", "Полоса вдоль взгляда, имя как дорожная разметка."),
              ("v2_relay", "Relay", "Имя делится между карточкой и прозрачной пластиной."),
              ("v3_scanimation", "Scanimation", "Решётка на плёнке: имя плавится, если качнуть головой."),
              ("v5_barlens", "Bar lens", "Сплющенное имя под акриловым бруском.")],
}


def viewbox(svg):
    head = svg.read_text()[:4000]
    vb = re.search(r'viewBox="([^"]+)"', head).group(1)
    return [float(v) for v in re.split(r"[ ,]+", vb.strip())][2:]


def main(site, set_dirs):
    site = pathlib.Path(site)
    (site / "data").mkdir(parents=True, exist_ok=True)
    for f in ("index.html", "fold.js", "scene.js"):
        shutil.copy(ROOT / f, site / f)
    for sd in map(pathlib.Path, set_dirs):
        sid = sd.name
        idx = json.loads((sd / "final" / "index.json").read_text())
        idx = idx if isinstance(idx, list) else idx.get("files", idx.get("cards", []))
        artist_of = {pathlib.Path(e["file"]).name: e.get("artist") for e in idx}
        tex = site / "tex" / sid
        specs = sorted((sd / "fold3d").glob("*.json"))
        todo, todo_clear = [], []
        designs = []
        for rank, (key, title, blurb) in enumerate(DESIGNS[sid], 1):
            cards = []
            for sp in specs:
                spec = json.loads(sp.read_text())
                stem = spec["svg"][:-4]
                if not (stem == key or stem.startswith(key + "_")):
                    continue
                svg = sd / "final" / spec["svg"]
                spec["size"] = viewbox(svg)
                spec.setdefault("title", title)
                slug = re.split(r"_(?=[a-z]+[-_][a-z]+$)", stem)[-1]
                name = artist_of.get(spec["svg"]) or slug
                if name == name.lower():                       # a slug, not a name
                    name = " ".join(w.capitalize() for w in re.split(r"[-_ ]", name))
                cards.append({"artist": name, "spec": spec})
                acetate = any(s.get("stock") == "acetate" for s in spec["sheets"])
                (todo_clear if acetate else todo).append(str(svg))
            if cards:
                order = ["Tanya Andrianova", "Igor Zotov", "Andrey Lee", "Sasha Chernikov", "Sophia Zhuravkova"]
                cards.sort(key=lambda c: order.index(c["artist"]) if c["artist"] in order else 9)
                designs.append({"id": key, "rank": rank, "title": title, "blurb": blurb, "cards": cards})
        for files, extra in ((todo, []), (todo_clear, ["--clear"])):
            if files:
                subprocess.run(["python3", str(HERE / "textures.py"), str(tex), *files, *extra], check=True)
        for f in tex.glob("*.size.json"):
            f.unlink()
        (site / "data" / f"{sid}.json").write_text(json.dumps(
            {"set": sid, "title": SETS[sid], "designs": designs}, ensure_ascii=False, separators=(",", ":")))
        print(sid, [(d["id"], len(d["cards"])) for d in designs])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
