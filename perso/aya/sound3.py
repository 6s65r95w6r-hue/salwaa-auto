import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
SR=48000; DUR=20.6; N=int(SR*DUR); t=np.arange(N)/SR; rng=np.random.default_rng(29); mix=np.zeros(N)
lp=lambda x,f,o=4: sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
bp=lambda x,a,b,o=2: sosfilt(butter(o,[a,b],'band',fs=SR,output='sos'),x)
db=lambda x:10**(x/20)
def put(s,x,g=1.0):
    i=int(s*SR); j=min(N,i+len(x))
    if i<N: mix[i:j]+=g*x[:j-i]
room=lp(lp(rng.standard_normal(N),110),110); room/=np.abs(room).max()
mix+=room*db(np.interp(t,[0,13,17.8,20,20.6],[-34,-31,-31,-36,-60]))
def whoosh(d=0.45,g=-16):
    n=int(d*SR); x=lp(bp(rng.standard_normal(n),150,1200),900)*np.sin(np.linspace(0,np.pi,n))**2; return x/np.abs(x).max()*db(g)
def thud(g=-8):
    n=int(0.45*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*(75*np.exp(-tt*6)+40)*tt)*np.exp(-tt*9)*db(g)
def swell(d=1.6,g=-18):
    n=int(d*SR); x=lp(lp(rng.standard_normal(n),500),500); return x/np.abs(x).max()*np.sin(np.linspace(0,np.pi,n))**2*db(g)
def ding(f=880,g=-18):
    n=int(0.9*SR); tt=np.arange(n)/SR; return (np.sin(2*np.pi*f*tt)+0.35*np.sin(2*np.pi*f*1.5*tt))*np.exp(-tt*5)*db(g)
def key(g=-28):
    n=int(0.03*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*rng.uniform(380,520)*tt)*np.exp(-tt*180)*db(g)
put(0.06,thud(-9)); put(0.05,whoosh(0.3,-22))
for c,g,sl in [(2.3,3.0,4.6),(5.2,5.9,7.4),(8.0,8.7,10.2)]:
    put(c,thud(-12)); put(g,ding(880,-19)); put(sl,whoosh(0.5,-19))
put(10.8,thud(-14)); put(11.0,thud(-11)); put(11.4,swell(1.6,-17)); put(12.0,ding(660,-17))
put(13.4,whoosh(0.8,-18)); put(13.6,swell(2.2,-15))
for i in range(5): put(13.6+i*0.08,ding(880+i*110,-26))
put(14.2,thud(-12))
put(17.8,whoosh(0.5,-19)); put(17.85,thud(-9))
for i in range(6): put(18.5+i*0.1,key(-26))
mix=lp(mix,9000); mix/=np.abs(mix).max()*1.12
wavfile.write('sfx3.wav',SR,(np.stack([mix,mix],1)*32767).astype(np.int16))
