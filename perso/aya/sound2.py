import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
SR=48000; DUR=14.0; N=int(SR*DUR); t=np.arange(N)/SR; rng=np.random.default_rng(14); mix=np.zeros(N)
lp=lambda x,f,o=4: sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
bp=lambda x,a,b,o=2: sosfilt(butter(o,[a,b],'band',fs=SR,output='sos'),x)
db=lambda x:10**(x/20)
def put(s,x,g=1.0):
    i=int(s*SR); j=min(N,i+len(x))
    if i<N: mix[i:j]+=g*x[:j-i]
room=lp(lp(rng.standard_normal(N),110),110); room/=np.abs(room).max()
mix+=room*db(np.interp(t,[0,3,10.4,13,14],[-34,-30,-30,-36,-60]))
def whoosh(d=0.45,g=-16):
    n=int(d*SR); x=lp(bp(rng.standard_normal(n),150,1200),900)*np.sin(np.linspace(0,np.pi,n))**2; return x/np.abs(x).max()*db(g)
def thud(g=-8):
    n=int(0.45*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*(75*np.exp(-tt*6)+40)*tt)*np.exp(-tt*9)*db(g)
def swell(d=1.6,g=-18):
    n=int(d*SR); x=lp(lp(rng.standard_normal(n),500),500); return x/np.abs(x).max()*np.sin(np.linspace(0,np.pi,n))**2*db(g)
def ping(g=-20):
    n=int(0.6*SR); tt=np.arange(n)/SR; return (np.sin(2*np.pi*660*tt)+0.3*np.sin(2*np.pi*990*tt))*np.exp(-tt*7)*db(g)
def key(g=-28):
    n=int(0.03*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*rng.uniform(380,520)*tt)*np.exp(-tt*180)*db(g)
for s in [0.12,0.52,1.17]: put(s-0.05,whoosh(0.35,-20))
put(1.17,thud(-10))
put(2.8,swell(1.8,-16)); put(3.3,whoosh(0.5,-24))
put(6.4,swell(2.0,-17))
for i in range(5): put(6.8+i*0.32,ping(-23))
put(8.4,whoosh(0.5,-24))
put(10.4,whoosh(0.6,-18)); put(10.55,thud(-9))
for i in range(6): put(11.3+i*0.1,key(-26))
mix=lp(mix,9000); mix/=np.abs(mix).max()*1.12
wavfile.write('sfx2.wav',SR,(np.stack([mix,mix],1)*32767).astype(np.int16))
