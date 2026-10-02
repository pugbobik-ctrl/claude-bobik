import sys, json, time, os, re
sys.path.insert(0, os.path.dirname(__file__))
import iglib
handles=[h.strip().lstrip('@') for h in sys.argv[1].split(',') if h.strip()]
db_path=os.path.join(iglib.S,'profiles.jsonl')
done=set()
if os.path.exists(db_path):
    for l in open(db_path): 
        try: done.add(json.loads(l)['handle'])
        except: pass
with open(db_path,'a') as db:
    for h in handles:
        if h in done: print('skip',h); continue
        try:
            info,posts=iglib.profile(h)
        except Exception as e:
            info,posts={'err':str(e)},[]
        rec=dict(handle=h,info=info,posts=posts)
        db.write(json.dumps(rec,ensure_ascii=False)+'\n'); db.flush()
        last=posts[0]['ts'] if posts else '-'
        print(f"{h:28s} posts={len(posts)} last={last} followers={info.get('followers')}")
        for p in posts[:8]:
            ment=sorted(set(re.findall(r'@([A-Za-z0-9_.]+)',p['cap'])))
            print(f"   {p['ts']} {p['sc']} {(p['cap'] or '').replace(chr(10),' ')[:110]}  {('@'+' @'.join(ment)) if ment else ''}")
        time.sleep(1.5)
