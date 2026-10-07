# Concept 4: Lemon Cradle - a half-cylinder rocker, name on the flat deck
from common import *
import json
from scipy.integrate import solve_ivp
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
G_=9810.0; GSM=0.0003
R=45.; Ldeck=150.
def parts(coins=0,coin_m=5.1):
    P=[]
    m=np.pi*R*Ldeck*GSM; P.append(dict(n='curved shell',m=m,z=-2*R/np.pi,Io=m*R**2))                 # thin arc about O
    m=2*R*Ldeck*GSM;     P.append(dict(n='deck',m=m,z=0.,Io=m*(2*R)**2/12))
    mc=0.5*np.pi*R**2*2*GSM*2  # two half-disc caps, 600 gsm (2 layers)
    P.append(dict(n='2 end caps (600 gsm)',m=mc,z=-4*R/(3*np.pi),Io=0.5*mc*R**2))
    if coins: P.append(dict(n=f'{coins} coin(s) on deck underside',m=coins*coin_m,z=0.,Io=coins*coin_m*8**2))
    return P
def summarize(P):
    M=sum(p['m'] for p in P); a=-sum(p['m']*p['z'] for p in P)/M; Io=sum(p['Io'] for p in P); Icm=Io-M*a*a
    Ic=Icm+M*(R-a)**2
    w2=M*G_*a/Ic; return dict(M=M,a=a,Io=Io,Icm=Icm,Icontact=Ic,T=2*np.pi/np.sqrt(w2))
def ode(S,th0,zeta=0.02,T=6):
    M,a,Icm=S['M'],S['a'],S['Icm']
    def J(th): return M*(R*R-2*R*a*np.cos(th)+a*a)+Icm
    c=2*zeta*np.sqrt(S['M']*G_*a*S['Icontact'])
    def rhs(t,y):
        th,w=y; return [w,(-M*G_*a*np.sin(th)-M*R*a*np.sin(th)*w*w-c*w)/J(th)]
    s=solve_ivp(rhs,[0,T],[th0,0],max_step=0.004); return s.t,s.y[0]
if __name__=='__main__':
    out={}
    for coins in (0,2,3):
        P=parts(coins); S=summarize(P); out[f'{coins}_coins']={k:float(v) for k,v in S.items()}
        print(coins,'coins',{k:round(float(v),3) for k,v in S.items()})
        for p in P: print('  ',p['n'],round(p['m'],2),'g  z',round(p['z'],1))
    json.dump(out,open(f'{OUT}/c4_results.json','w'),indent=1)
    # plots for the 2-coin tuned design
    S0=summarize(parts(0)); S2=summarize(parts(2))
    fig,ax=plt.subplots(1,3,figsize=(13,3.5),dpi=140)
    th=np.radians(np.linspace(-80,80,321))
    for S,lab,c in ((S0,'paper only',"#1f5fd1"),(S2,'+2 coins under deck (tuned)','#111')):
        h=R-S['a']*np.cos(th); ax[0].plot(np.degrees(th),h,color=c,label=f"{lab}: a={S['a']:.1f} mm",lw=1.8)
    ax[0].set_xlabel('deck tilt (deg)'); ax[0].set_ylabel('CoM height above table (mm)'); ax[0].set_title('CoM rises whenever it tilts: stable, no tipping below 90 deg',fontsize=8.5); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
    for S,lab,c in ((S0,'paper only','#1f5fd1'),(S2,'tuned','#111')):
        t,y=ode(S,np.radians(20)); ax[1].plot(t,np.degrees(y),color=c,label=f"{lab}: T={S['T']:.2f} s",lw=1.4)
    ax[1].set_xlabel('time (s)'); ax[1].set_ylabel('deck tilt (deg)'); ax[1].set_title('flick to 20 deg, full nonlinear rolling, 2 % damping',fontsize=8.5); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3)
    # CoM vs support picture data: a vs R
    aa=np.linspace(0,R,100)
    ax[2].plot(aa,[2*np.pi/np.sqrt(9810*a/(0.5*R*R+(R-a)**2)) if a>0.5 else np.nan for a in aa],color='#111'); ax[2].set_xlabel('CoM depth a below centre of curvature (mm)'); ax[2].set_ylabel('rocking period (s)')
    ax[2].axvline(S0['a'],color='#1f5fd1',lw=1,ls='--'); ax[2].axvline(S2['a'],color='#111',lw=1,ls='--'); ax[2].set_ylim(0,2.5); ax[2].set_title('a > 0 is the only condition; smaller a = slower, floatier',fontsize=8.5); ax[2].grid(alpha=.3)
    plt.tight_layout(); plt.savefig(f'{OUT}/c4_physics.png')
