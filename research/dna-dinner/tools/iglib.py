import re, json, html, subprocess, datetime, os, time, hashlib
S=os.environ.get("IG_DATA", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
UA="Mozilla/5.0"
A="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
def sc2date(sc):
    n=0
    for ch in sc[:11]: n=n*64+A.index(ch)
    return datetime.datetime.utcfromtimestamp(((n>>23)+1314220021721)/1000).strftime('%Y-%m-%d')
def get(url, out=None, ua=UA, timeout=30):
    out = out or os.path.join(S,'cache',hashlib.md5(url.encode()).hexdigest())
    os.makedirs(os.path.dirname(out),exist_ok=True)
    if os.path.exists(out) and os.path.getsize(out)>2000: return open(out,'rb').read()
    r=subprocess.run(['curl','-sS','-L','-m',str(timeout),'-A',ua,'-o',out,'-w','%{http_code}',url],capture_output=True,text=True)
    if not os.path.exists(out): return b''
    return open(out,'rb').read()
def _context(h):
    i=h.find('"contextJSON":')
    if i<0: return None
    s=h[i+len('"contextJSON":'):]
    val,_=json.JSONDecoder().raw_decode(s)
    return json.loads(val) if isinstance(val,str) else val
def walk(o):
    if isinstance(o,dict):
        yield o
        for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
def profile(username):
    h=get(f"https://www.instagram.com/{username}/embed/").decode('utf-8','ignore')
    ctx=_context(h)
    posts=[]; info={}
    if not ctx: return info,posts
    for d in walk(ctx):
        if 'shortcode' in d and 'taken_at_timestamp' in d:
            cap=''
            try: cap=d['edge_media_to_caption']['edges'][0]['node']['text']
            except Exception: pass
            posts.append(dict(sc=d['shortcode'],ts=datetime.datetime.utcfromtimestamp(d['taken_at_timestamp']).strftime('%Y-%m-%d'),
                type=d.get('__typename'),img=d.get('display_url') or d.get('thumbnail_src'),cap=cap,
                user=(d.get('owner') or {}).get('username',username)))
        if d.get('username')==username and 'edge_followed_by' in d:
            info=dict(followers=d['edge_followed_by'].get('count'),bio=d.get('biography'),full=d.get('full_name'))
    seen=set(); uniq=[]
    for p in posts:
        if p['sc'] in seen: continue
        seen.add(p['sc']); uniq.append(p)
    return info,uniq
def post(sc):
    h=get(f"https://www.instagram.com/p/{sc}/embed/captioned/").decode('utf-8','ignore')
    cap=''; user=''; img=''
    m=re.search(r'class="UsernameText"[^>]*>([^<]+)',h); user=m.group(1) if m else ''
    i=h.find('class="Caption"')
    if i>=0:
        seg=h[i:i+20000]; seg=seg[:seg.find('class="CaptionComments"') if 'class="CaptionComments"' in seg else 6000]
        cap=re.sub(r'\s+',' ',html.unescape(re.sub(r'<br\s*/?>','\n',re.sub(r'<(?!br)[^>]+>',' ',seg)))).strip()
    m=re.search(r'<img class="EmbeddedMediaImage"[^>]*src="([^"]+)"',h); img=html.unescape(m.group(1)) if m else ''
    ctx=_context(h)
    if ctx:
        for d in walk(ctx):
            if d.get('shortcode')==sc:
                try: cap=d['edge_media_to_caption']['edges'][0]['node']['text']
                except Exception: pass
                img=d.get('display_url') or img
                user=(d.get('owner') or {}).get('username',user)
                break
    return dict(sc=sc,date=sc2date(sc),user=user,cap=cap,img=img)
def fetch_img(url,name):
    out=os.path.join(S,'imgs',name)
    os.makedirs(os.path.dirname(out),exist_ok=True)
    if not os.path.exists(out) or os.path.getsize(out)<1000:
        subprocess.run(['curl','-sS','-L','-m','40','-A',UA,'-o',out,url],capture_output=True)
    return out
