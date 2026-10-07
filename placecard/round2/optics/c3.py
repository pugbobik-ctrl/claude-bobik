# Concept 3: Rim Walker - name panel perched on a wine-glass rim, counterweight coin hanging inside the glass
from common import *
import json
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp
G_=9810.0   # mm/s^2
GSM=0.0003  # g per mm^2 (300 gsm card)
PANEL_W,PANEL_H=90.,45.
STRIP_W=10.
XP=36.      # panel plane x (outside the rim)
COINS={'1 RUB':(3.2,20.5),'2 RUB':(5.1,23.0),'5 RUB':(6.0,25.0),'10 RUB':(5.63,22.0)}

def _unused_build(coin="1 RUB",xt=None,zc=None,tail_len=None,extra_pocket=0.25):
    m_coin,dia=COINS[coin]
    parts=[]
    mp=PANEL_W*PANEL_H*GSM; parts.append(dict(n='panel',m=mp,x=XP,z=PANEL_H/2,I=mp*PANEL_H**2/12))
    return parts

def assemble(coin,xt,zc):
    """xt: x of the hanging tail/coin ; zc: z of coin centre (negative)."""
    m_coin,dia=COINS[coin]
    parts=[]
    mp=PANEL_W*PANEL_H*GSM; parts.append(dict(n='panel',m=mp,x=XP,z=PANEL_H/2,I=mp*PANEL_H**2/12))
    L=XP-xt; ms=STRIP_W*L*GSM; parts.append(dict(n='strip',m=ms,x=(XP+xt)/2,z=0.,I=ms*L**2/12))
    tl=-zc+dia/2-3; mt=STRIP_W*tl*GSM+0.25; parts.append(dict(n='tail+pocket',m=mt,x=xt,z=-tl/2,I=mt*tl**2/12))
    parts.append(dict(n=f'coin {coin}',m=m_coin,x=xt,z=zc,I=m_coin*(dia/2)**2/2))
    return parts

def props(parts):
    M=sum(p['m'] for p in parts); xc=sum(p['m']*p['x'] for p in parts)/M; zc=sum(p['m']*p['z'] for p in parts)/M
    Ip=sum(p['I']+p['m']*(p['x']**2+p['z']**2) for p in parts)
    return M,xc,zc,Ip

# design: coin 1 RUB, choose xt so x_cm = 0 with strip/tail positions consistent, choose zc for d = 9 mm
def design(coin='1 RUB',d_target=15.0):
    def eq(v):
        xt,zc=v; M,xc,zc_,Ip=props(assemble(coin,xt,zc)); return [xc,zc_+d_target]
    sol=fsolve(eq,[-14,-22]); return sol
if __name__=='__main__':
    xt,zc=design('1 RUB'); parts=assemble('1 RUB',xt,zc); M,xc,zcm,Ip=props(parts)
    print('design xt,zc',xt,zc,'M',M,'CoM',xc,zcm,'Ip',Ip)
    T=2*np.pi*np.sqrt(Ip/(M*G_*(-zcm))); print('pitch period s',T)
    for p in parts: print(p)
