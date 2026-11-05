import numpy as np, sys
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR=48000; DUR=46.0
rng=np.random.default_rng(7)
out=np.zeros(int(SR*DUR))
def put(t,s,g=1.0):
    i=int(t*SR); n=min(len(s),len(out)-i)
    if n>0: out[i:i+n]+=s[:n]*g
def bp(x,lo,hi):
    return sosfilt(butter(2,[lo,hi],btype='band',fs=SR,output='sos'),x)
def lp(x,hi): return sosfilt(butter(2,hi,btype='low',fs=SR,output='sos'),x)
def noise(d): return rng.standard_normal(int(SR*d))
def whoosh(d=.7):
    n=bp(noise(d),300,4000); t=np.linspace(0,1,len(n)); return n*np.sin(np.pi*t)**2*.5
def thud():
    d=.5; t=np.arange(int(SR*d))/SR; f=38+32*np.exp(-t*14)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7); s[:200]+=rng.standard_normal(200)*.4; return s*.9
def ping():
    d=.5; t=np.arange(int(SR*d))/SR
    return (np.sin(2*np.pi*1320*t)+.6*np.sin(2*np.pi*1980*t))*np.exp(-t*9)*.35
def tick():
    d=.06; t=np.arange(int(SR*d))/SR; return np.sin(2*np.pi*2400*t)*np.exp(-t*80)*.3
def pop():
    d=.18; t=np.arange(int(SR*d))/SR; f=700-400*t/d
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*22)*.6
def shimmer(d=2.0):
    n=bp(noise(d),5000,12000); t=np.linspace(0,1,len(n)); return n*np.sin(np.pi*t)**2*.18
def click():
    d=.12; t=np.arange(int(SR*d))/SR
    return (np.sin(2*np.pi*1800*t)*np.exp(-t*60)+.5*np.sin(2*np.pi*900*t)*np.exp(-t*40))*.5
# room tone / wind
wind=lp(noise(DUR),400)*0.06
t=np.arange(len(wind))/SR; wind*=0.7+0.3*np.sin(2*np.pi*0.13*t)
out+=wind
# events (same timings as HTML)
for tt in [5.7,12.6,22.2,32.2,39.8,42.9]: put(tt,whoosh(.6),.8)
put(13.0,whoosh(1.0),.6)
put(14.5,whoosh(.9),.7)
put(15.0,shimmer(2.5),1)
for tt in [7.0,7.8,8.6,9.4,10.2]: put(tt+.15,ping(),1)
for tt in [6.4,8.6,10.6]: put(tt,tick(),1)
for tt in [19.9,21.9]: put(tt,thud(),.35)
put(24.0,thud(),.9)
for i in range(5): put(35.0+i*.5,pop(),1)
put(33.0,shimmer(3),.8)
put(43.3,click(),1); put(43.4,shimmer(1.5),.6)
pk=np.max(np.abs(out)); out=out/pk*10**(-1.5/20)
fade=int(.6*SR); out[-fade:]*=np.linspace(1,0,fade)
wavfile.write(sys.argv[1],SR,(out*32767).astype(np.int16))
print("sound ok")
