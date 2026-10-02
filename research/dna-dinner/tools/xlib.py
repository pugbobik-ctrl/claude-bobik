import math, subprocess, json, datetime, os
S=os.path.dirname(os.path.abspath(__file__))
def token(i):
    x=(int(i)/1e15)*math.pi; digits='0123456789abcdefghijklmnopqrstuvwxyz'
    ip=int(x); fp=x-ip; s=''
    while ip>0: s=digits[ip%36]+s; ip//=36
    s=(s or '0')+'.'
    for _ in range(12): fp*=36; d=int(fp); s+=digits[d]; fp-=d
    return s.replace('0','').replace('.','')
def sfdate(i): return datetime.datetime.utcfromtimestamp(((int(i)>>22)+1288834974657)/1000).strftime('%Y-%m-%d')
def tweet(tid):
    u=f"https://cdn.syndication.twimg.com/tweet-result?id={tid}&lang=en&token={token(tid)}"
    r=subprocess.run(['curl','-sS','-m','25','-A','Mozilla/5.0',u],capture_output=True,text=True)
    try: d=json.loads(r.stdout)
    except Exception: return None
    media=[m.get('media_url_https') for m in d.get('mediaDetails',[])]
    if not media and d.get('video'): media=[d['video'].get('poster')]
    return dict(id=tid,date=sfdate(tid),user=(d.get('user') or {}).get('screen_name'),name=(d.get('user') or {}).get('name'),
                text=d.get('text'),media=media,quoted=(d.get('quoted_tweet') or {}).get('text'))
