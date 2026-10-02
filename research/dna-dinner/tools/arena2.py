import json, subprocess, urllib.parse, re, sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
import iglib
def api(path):
    for i in range(2):
        r=subprocess.run(['curl','-sS','-m','40',f'https://api.are.na/v2/{path}'],capture_output=True,text=True)
        try: return json.loads(r.stdout)
        except Exception: time.sleep(1)
    return {}
out_path=os.path.join(iglib.S,'arena_hits.jsonl'); chan_path=os.path.join(iglib.S,'arena_channels.txt')
seen=set(); done_ch=set()
if os.path.exists(out_path):
    for l in open(out_path): seen.add(json.loads(l)['url'])
if os.path.exists(chan_path): done_ch=set(open(chan_path).read().split())
qs=sys.argv[1].split('|')
with open(out_path,'a') as out, open(chan_path,'a') as chf:
    for q in qs:
        d=api(f"search/channels?q={urllib.parse.quote(q)}&per=40")
        chans=[c for c in d.get('channels',[]) if 15<=(c.get('length') or 0)<=3000 and c.get('status')!='private']
        nq=0
        for c in chans[:12]:
            slug=c['slug']
            if slug in done_ch: continue
            done_ch.add(slug); chf.write(slug+'\n')
            L=c.get('length') or 0; pages=min(4,(L+99)//100)
            # newest blocks are usually at the end: fetch last pages
            total_pages=(L+99)//100
            for page in range(max(1,total_pages-pages+1), total_pages+1):
                cd=api(f"channels/{slug}/contents?per=100&page={page}")
                for b in cd.get('contents',[]):
                    src=((b.get('source') or {}).get('url') or '')
                    m=re.search(r'instagram\.com/(?:[A-Za-z0-9_.]+/)?(?:p|reel|tv)/([A-Za-z0-9_-]{11})',src)
                    x=re.search(r'(?:x|twitter)\.com/([A-Za-z0-9_]+)/status/(\d+)',src)
                    if not (m or x) or src in seen: continue
                    seen.add(src)
                    rec=dict(q=q,ch=slug,url=src,sc=m.group(1) if m else None,date=iglib.sc2date(m.group(1)) if m else None,
                             title=(b.get('title') or '')[:150],img=((b.get('image') or {}).get('display') or {}).get('url'),
                             desc=(b.get('description') or '')[:300])
                    out.write(json.dumps(rec,ensure_ascii=False)+'\n'); nq+=1
        print(f"{q!r}: channels={len(chans)} +{nq}",flush=True)
