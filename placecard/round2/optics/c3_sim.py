from c3 import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
xt,zc=design('1 RUB'); parts=assemble('1 RUB',xt,zc); M,xc,zcm,Ip=props(parts)
res={'design':dict(xt=float(xt),zc=float(zc),M_g=float(M),com=[float(xc),float(zcm)],d_below_pivot_mm=float(-zcm),Ip=float(Ip),period_s=float(2*np.pi*np.sqrt(Ip/(M*G_*-zcm))))}
# 1) other coins in the SAME geometry
tab=[]
for name in list(COINS)+['no coin']:
    pp=[dict(p) for p in parts]
    if name=='no coin': pp=[p for p in pp if not p['n'].startswith('coin')]
    else:
        m,dia=COINS[name]; pp[-1]=dict(n='coin',m=m,x=xt,z=zc,I=m*(dia/2)**2/2)
    Mx,x_,z_,I_=props(pp)
    th0=np.degrees(np.arctan2(-x_,-z_))     # equilibrium: CoM straight below pivot -> rotate by this angle (CCW +)
    stable=z_<0
    tab.append(dict(coin=name,M=float(Mx),com_x=float(x_),com_z=float(z_),eq_tilt_deg=float(th0),stable=bool(stable),
                    period=float(2*np.pi*np.sqrt(I_/(Mx*G_*np.hypot(x_,z_)))) if stable else None))
res['coins']=tab
# 2) card gsm tolerance: 250 .. 350 gsm
gs=[]
global_gsm=GSM
import c3
for g in (250,300,350,400):
    c3.GSM=g/1e6
    pp=assemble('1 RUB',xt,zc); Mx,x_,z_,I_=props(pp)
    gs.append(dict(gsm=g,com_x=float(x_),com_z=float(z_),eq_tilt_deg=float(np.degrees(np.arctan2(-x_,-z_)))))
c3.GSM=GSM; res['gsm']=gs
# 3) potential energy and ring-down
th=np.radians(np.linspace(-60,60,241))
h=xc*np.sin(th)+zcm*np.cos(th)       # CoM height rel. pivot (mm)
U=M*G_*h*1e-6                          # mJ  (g*mm/s^2*mm =1e-9 J ... in g*mm2/s2 -> *1e-9 kg*... ) just relative
def rhs(t,y,zeta=0.035):
    th,w=y; wn2=M*G_*(-zcm)/Ip
    tau=-M*G_*(xc*np.cos(th)-zcm*np.sin(th))/Ip
    return [w,tau-2*zeta*np.sqrt(wn2)*w]
sol=solve_ivp(rhs,[0,4],[np.radians(22),0],max_step=0.002)
t,thT=sol.t,np.degrees(sol.y[0])
# coin/wall contact: glass profile
def wall(z): return 14*np.sin(np.pi*np.clip(-z,0,100)/100)**0.9   # right wall x(z), z in [-100,0]
hits=0; prev=False; hit_t=[]
for tt,a in zip(t,sol.y[0]):
    cx=xt*np.cos(a)-zc*np.sin(a); cz=xt*np.sin(a)+zc*np.cos(a)
    edge=cx+10.25
    inside=edge>wall(cz) if cz<0 else edge>0
    if inside and not prev: hits+=1; hit_t.append(float(tt))
    prev=inside
res['ringdown']=dict(start_deg=22,zeta=0.035,tink_events=hits,tink_times=hit_t[:6])
# amplitude half-life
pk=[(t[i],abs(thT[i])) for i in range(1,len(t)-1) if abs(thT[i])>abs(thT[i-1]) and abs(thT[i])>abs(thT[i+1])]
res['ringdown']['peaks']=[(round(a,2),round(b,1)) for a,b in pk[:8]]
json.dump(res,open(f'{OUT}/c3_results.json','w'),indent=1)
print(json.dumps(res,indent=1)[:2500])
fig,ax=plt.subplots(1,2,figsize=(10,3.6),dpi=140)
ax[0].plot(np.degrees(th),h,color='#111',lw=2); ax[0].axvline(0,color='#d4281c',lw=1,ls='--')
ax[0].set_xlabel('card tilt (deg, + = panel leans toward the glass)'); ax[0].set_ylabel('height of centre of mass above rim (mm)')
ax[0].set_title(f'CoM height vs tilt: one stable minimum, {-zcm:.0f} mm below the rim',fontsize=9)
for name,c in (('2 RUB','#1f5fd1'),('10 RUB','#2a9d3a')):
    d=[r for r in tab if r['coin']==name][0]
    ax[0].plot(np.degrees(th),d['com_x']*np.sin(th)+d['com_z']*np.cos(th),color=c,lw=1,label=f'{name} coin instead')
ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
ax[1].plot(t,thT,color='#111',lw=1.4); ax[1].set_xlabel('time (s)'); ax[1].set_ylabel('card tilt (deg)')
ax[1].set_title(f'nudged to 22 deg, damping 3.5 %: period {res["design"]["period_s"]:.2f} s, {hits} glass tinks',fontsize=9)
for tt in hit_t[:6]: ax[1].axvline(tt,color='#e0a800',lw=.8)
ax[1].grid(alpha=.3)
plt.tight_layout(); plt.savefig(f'{OUT}/c3_physics.png'); print('saved')
