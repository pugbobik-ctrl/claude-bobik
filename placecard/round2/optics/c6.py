# Concept 6: Slip - moire name reveal with a sliding line screen
from common import *
import cv2, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
P=1.2          # grating pitch mm
DUTY=0.5
GAIN=0.06      # dot gain per ink edge, mm (offset-press typical ~ 0.05)
RW,RH=150.,60.
SS=20          # px/mm supersample
CAP=17.0
def letters_mask():
    l1=text_poly('Sophia',CAP,700,0.02,'c'); l2=text_poly('Zhuravkova',CAP,700,0.02,'c')
    G=unary_union([affinity.translate(l1,0,9.5),affinity.translate(l2,0,-14.5)])
    w,h=int(RW*SS),int(RH*SS); m=np.zeros((h,w),np.uint8)
    def tp(c): return np.round(np.c_[(np.array(c)[:,0]+RW/2)*SS,(RH/2-np.array(c)[:,1])*SS]*16).astype(np.int32)
    for p in G.geoms:
        cv2.fillPoly(m,[tp(p.exterior.coords)],255,shift=4)
        for i in p.interiors: cv2.fillPoly(m,[tp(i.coords)],0,shift=4)
    return m>127, G
M,GEO=letters_mask()
H_,W_=M.shape
X=(np.arange(W_)+.5)/SS; Xg=X[None,:].repeat(H_,0)
Y=(np.arange(H_)+.5)/SS; Yg=Y[:,None].repeat(W_,1)
L_LEMON=0.83; L_INK=0.035
def base_ink(gain=GAIN):
    ph=np.mod(Xg,P)
    w=P*DUTY+2*gain
    bg=ph<w                      # background lines ink at phase [0,w)
    ph2=np.mod(Xg-P*DUTY,P)      # letters: shifted half a pitch
    lt=ph2<w
    return np.where(M,lt,bg)
def overlay_opaque(s,angle_deg=0.0,gain=GAIN):
    xs=Xg-s-np.tan(np.radians(angle_deg))*(Yg-RH/2)
    ph=np.mod(xs-P*DUTY,P)   # opaque bars at the half-pitch phase
    return ph<(P*DUTY+2*gain)
def composite(s,angle_deg=0.0,gain=GAIN):
    bi=base_ink(gain); ov=overlay_opaque(s,angle_deg,gain)
    L=np.where(ov|bi,L_INK,L_LEMON)
    return L
def view(L,ppmm=6):
    sm=cv2.GaussianBlur(L.astype(np.float32),(0,0),SS*0.12)   # printing + eye blur ~0.12 mm
    return cv2.resize(sm,(int(RW*ppmm),int(RH*ppmm)),interpolation=cv2.INTER_AREA)
def srgb(L): L=np.clip(L,0,1); return np.where(L<=0.0031308,12.92*L,1.055*L**(1/2.4)-0.055)
def tint(L): 
    lem=np.array([0xfe,0xed,0x95])/255.; ink=np.array([0.05,0.05,0.05])
    t=(L-L_INK)/(L_LEMON-L_INK); t=np.clip(t,0,1)[...,None]
    return (ink**2.2)*(1-t)+(lem**2.2)*t
if __name__=='__main__':
    res={}
    offs=[('0',0),('p/4',P/4),('p/2',P/2),('3p/4',3*P/4)]
    tiles=[]
    for name,s in offs:
        L=composite(s); v=view(L); 
        lm=M; Lm=L[lm].mean(); Lb=L[~lm].mean()
        res[name]=dict(letters=float(Lm),background=float(Lb),michelson=float((Lm-Lb)/(Lm+Lb)))
        cv2.imwrite(f'{OUT}/c6_s{name.replace("/","_")}.png',(srgb(tint(v))[...,::-1]*255+.5).astype(np.uint8)); print(name,res[name])
    # skew frame
    L=composite(P/2,1.0); v=view(L); cv2.imwrite(f'{OUT}/c6_skew.png',(srgb(tint(v))[...,::-1]*255+.5).astype(np.uint8))
    L=composite(P/2,0.08); v=view(L); cv2.imwrite(f'{OUT}/c6_skew_small.png',(srgb(tint(v))[...,::-1]*255+.5).astype(np.uint8))
    # contrast vs shift, and dot gain sensitivity
    ss=np.linspace(0,2*P,49); fig,ax=plt.subplots(1,2,figsize=(10,3.2),dpi=140)
    for g,c in ((0.0,'#1f5fd1'),(0.06,'#111'),(0.12,'#d4281c')):
        mm=[]
        for s in ss:
            L=composite(s,0,g); mm.append((L[M].mean()-L[~M].mean())/(L[M].mean()+L[~M].mean()))
        ax[0].plot(ss,mm,color=c,label=f'dot gain {g:.2f} mm'); 
        if g==0.06: res['contrast_curve']=[float(x) for x in mm]
    ax[0].set_xlabel('slide position (mm)'); ax[0].set_ylabel('name contrast (+ = name lighter)'); ax[0].axhline(0,color='#888',lw=.6); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3); ax[0].set_title('name flips light <-> dark every 0.6 mm of slide, vanishes between',fontsize=8.5)
    angs=np.linspace(0,1.6,33); ab=[]
    for a in angs:
        L=composite(P/2,a); sm=view(L,6); 
        # contrast on left third vs right third of the name: sign flip means skew defeats it
        mm=M[:, :]; left=np.zeros_like(M); left[:H_//3,:]=True; right=np.zeros_like(M); right[2*H_//3:,:]=True
        cl=(L[M&left].mean()-L[~M&left].mean())/(L[M&left].mean()+L[~M&left].mean()); cr=(L[M&right].mean()-L[~M&right].mean())/(L[M&right].mean()+L[~M&right].mean())
        ab.append((a,cl,cr))
    ab=np.array(ab); ax[1].plot(ab[:,0],ab[:,1],color='#1f5fd1',label='top of the name'); ax[1].plot(ab[:,0],ab[:,2],color='#d4281c',label='bottom of the name'); ax[1].axhline(0,color='#888',lw=.6)
    ax[1].set_xlabel('screen rotated relative to print (deg)'); ax[1].set_ylim(-1,0.2); ax[1].set_ylabel('name contrast'); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3); ax[1].set_title('screen skew: top and bottom of the name drift apart in phase',fontsize=8.5)
    res['skew_curve']=ab.tolist()
    plt.tight_layout(); plt.savefig(f'{OUT}/c6_physics.png'); json.dump(res,open(f'{OUT}/c6_results.json','w'),indent=1)
