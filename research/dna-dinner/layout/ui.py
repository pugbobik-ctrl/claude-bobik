"""Shared look of the boards: poster palette, Inter, idea panels with their references."""
import html, os, json
from lib import load, V2
Y = '#FEED95'; CREAM = '#F6E7C8'; MUTE = '#C9A27A'; BG = '#2B140A'
CAR = '#C68B4E'; CRUST = '#7A462A'; DARK = '#452213'; WHITE = '#F4EEE3'
TONES = [Y, CAR, CRUST, DARK]
try:
    REF = json.load(open(os.path.join(V2, 'refs', 'index.json')))   # thumbnails of the research works, not in git
except FileNotFoundError:
    REF = []
def ref_img(code):
    for o in REF:
        if code in o['name']:
            return 'refs/' + o['name'] + '.jpg', o['label']
    return 'refs/' + code + '.jpg', code
# client references 3..9 and the poster are not stored in git; point to them with env vars
CLIENT_DIR = os.environ.get('DNA_CLIENT_IMG', '../img')
CLIENT = {n: f'{CLIENT_DIR}/{n-1:02d}.jpg' for n in range(3, 10)}   # client refs 3..9 -> 02.jpg..08.jpg
POSTER = os.environ.get('DNA_POSTER', 'poster.jpg')
CSS = f'''
:root{{--y:{Y};--cream:{CREAM};--mute:{MUTE};--bg:{BG}}}
*{{box-sizing:border-box}}
body{{margin:0;background:{BG};font-family:Inter,system-ui,sans-serif;color:{CREAM};-webkit-font-smoothing:antialiased}}
.board{{width:1600px;position:relative;overflow:hidden;background:{BG};padding:56px 64px 60px}}
.board::before{{content:"";position:absolute;inset:0;background:url(bg_dark.jpg) center top/cover;opacity:.9;z-index:0}}
.board>*{{position:relative;z-index:1}}
.kick{{font-size:14px;font-weight:500;letter-spacing:.02em;color:{Y};opacity:.85}}
h1{{margin:10px 0 0;font-size:46px;line-height:1;font-weight:500;letter-spacing:-.01em;color:{Y};text-transform:uppercase}}
.lead{{margin:16px 0 0;max-width:860px;font-size:17px;line-height:1.45;color:{CREAM}}}
.grid{{display:grid;gap:44px 56px;margin-top:40px}}
.idea{{display:flex;flex-direction:column;gap:14px;min-width:0}}
.ih{{display:flex;align-items:baseline;gap:14px;border-top:1px solid rgba(254,237,149,.35);padding-top:14px}}
.il{{font-size:15px;font-weight:600;color:{Y}}}
.ih h3{{margin:0;font-size:24px;line-height:1.15;font-weight:600;color:{Y};letter-spacing:-.005em}}
.iv{{position:relative}}
.iv svg,.iv img{{display:block;max-width:100%;height:auto}}
.it{{margin:0;font-size:15.5px;line-height:1.45;color:{CREAM}}}
.it b{{font-weight:600;color:{Y}}}
.prod{{font-size:13.5px;line-height:1.45;color:{MUTE}}}
.refs{{display:flex;gap:10px;align-items:flex-start}}
.refs figure{{margin:0;width:92px}}
.refs img{{width:92px;height:92px;object-fit:cover;display:block;border-radius:2px}}
.refs figcaption{{margin-top:5px;font-size:11.5px;line-height:1.3;color:{MUTE};overflow-wrap:anywhere}}
.two{{display:grid;grid-template-columns:1fr 1fr}}
.ib{{display:grid;grid-template-columns:1fr auto;gap:26px;align-items:start}}
.ib .prod{{margin-top:8px}}
.three{{display:grid;grid-template-columns:repeat(3,1fr)}}
.three .ib{{grid-template-columns:1fr;gap:14px}}
'''
def page(body, height=None, extra_css=''):
    hh = f'height:{height}px;' if height else ''
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">'
            f'<style>{CSS}{extra_css}</style></head><body><div class="board" style="{hh}">{body}</div></body></html>')
def header(kick, title, lead):
    return f'<div class="kick">{kick}</div><h1>{title}</h1><p class="lead">{lead}</p>'
def refs(items):
    """items: list of (src, caption)"""
    return '<div class="refs">' + ''.join(
        f'<figure><img src="{html.escape(s)}"><figcaption>{html.escape(c)}</figcaption></figure>' for s, c in items) + '</div>'
def idea(letter, title, visual, text, prod, ref_items, style=''):
    return (f'<section class="idea" style="{style}"><div class="ih"><span class="il">{letter}</span><h3>{title}</h3></div>'
            f'<div class="iv">{visual}</div><div class="ib"><div><p class="it">{text}</p><div class="prod">{prod}</div></div>'
            f'{refs(ref_items)}</div></section>')
def shadow_filter(id_, dx=0, dy=6, blur=7, op=0.45):
    return (f'<filter id="{id_}" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{blur}" flood-color="#120600" flood-opacity="{op}"/></filter>')
