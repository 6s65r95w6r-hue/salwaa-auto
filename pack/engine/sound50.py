import numpy as np, sys
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR=48000; DUR=50.0
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
# events
for tt in [4.6,10.7,18.7,25.7,33.7,37.7,43.0,46.6]: put(tt,whoosh(.6),.7)
put(2.1,thud(),.9)
def grind(d=.9):
    n=bp(noise(d),70,380); t=np.linspace(0,1,len(n)); return n*np.sin(np.pi*t)**2*.9
for tt in [13.4,21.9,29.9]: put(tt,grind(1.0),.7)
put(34.1,grind(1.6),1.0); put(34.4,shimmer(3),.8); put(35.6,thud(),.5)
for tt in [12.0,19.8,26.8]: put(tt,pop(),.6)
put(46.8,click(),1); put(46.9,shimmer(1.5),.6)
pk=np.max(np.abs(out)); out=out/pk*10**(-1.5/20)
fade=int(.6*SR); out[-fade:]*=np.linspace(1,0,fade)
wavfile.write(sys.argv[1],SR,(out*32767).astype(np.int16))
print("sound ok")
