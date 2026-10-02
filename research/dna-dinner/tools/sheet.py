import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import iglib
# usage: sheet.py out.jpg handle1 handle2 ...  (all posts of these handles)  or  out.jpg sc:XXXX sc:YYYY
out=sys.argv[1]; items=sys.argv[2:]
recs={}
for l in open(os.path.join(iglib.S,'profiles.jsonl')):
    r=json.loads(l); recs[r['handle']]=r
files=[]
for it in items:
    if it.startswith('sc:'):
        sc=it[3:]; p=None
        for r in recs.values():
            for q in r['posts']:
                if q['sc']==sc: p=q; p['user']=r['handle']
        if not p:
            p=iglib.post(sc); p['ts']=p['date']
        lst=[p]
    else:
        lst=[dict(q,user=it) for q in recs.get(it,{}).get('posts',[])]
    for p in lst:
        if not p.get('img'): continue
        f=iglib.fetch_img(p['img'],p['sc']+'.jpg')
        if os.path.getsize(f)>1000: files.append((f,f"{p['user'][:18]} {p['ts']} {p['sc']}"))
args=['montage']
for f,l in files: args+=['-label',l,f]
args+=['-tile','6x','-geometry','300x300+4+4','-pointsize','13',out]
subprocess.run(args,check=True); print(out,len(files))
