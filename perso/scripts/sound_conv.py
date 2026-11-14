import sys, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

import sys
SR = 48000; VID = sys.argv[1]; DUR = {'11':13.0,'12':12.8,'13':13.0}[VID]
N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(21)
mix = np.zeros(N)
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def db(x): return 10 ** (x / 20)
def put(s, x, g=1.0):
    i = int(s * SR); j = min(N, i + len(x))
    if i < N: mix[i:j] += g * x[: j - i]

# fond grave et doux (bureau), jamais de souffle aigu
room = lp(lp(rng.standard_normal(N), 110), 110); room /= np.abs(room).max()
mix += room * db(np.interp(t, [0, DUR-2, DUR], [-36, -38, -60]))

def pop(f, g=-14):
    n = int(0.12 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * f * (1 + 0.5 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 30) * db(g)
def thud(g=-6):
    n = int(0.45 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * (75 * np.exp(-tt * 6) + 40) * tt) * np.exp(-tt * 9) * db(g)
def whoosh(d=0.45, g=-14):
    n = int(d * SR); x = lp(bp(rng.standard_normal(n), 150, 1200), 900) * np.sin(np.linspace(0, np.pi, n)) ** 2
    return x / np.abs(x).max() * db(g)
def key(g=-30):
    n = int(0.03 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * rng.uniform(380, 520) * tt) * np.exp(-tt * 180) * db(g)
def stamp(g=-8):
    n = int(0.18 * SR); tt = np.arange(n) / SR
    return (lp(bp(rng.standard_normal(n), 120, 900), 900) * np.exp(-tt * 35) * 0.6 + np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 25)) * db(g)
def step(g=-20):
    n = int(0.12 * SR); tt = np.arange(n) / SR
    return lp(rng.standard_normal(n), 600) * np.exp(-tt * 45) * db(g) * 3
def ping(g=-14):
    n = int(0.25 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 880 * tt) + 0.4 * np.sin(2 * np.pi * 1320 * tt)) * np.exp(-tt * 14) * db(g)
def swell(d=1.6, g=-18):
    n = int(d * SR); x = lp(lp(rng.standard_normal(n), 500), 500)
    return x / np.abs(x).max() * np.sin(np.linspace(0, np.pi, n)) ** 2 * db(g)
def click(g=-8):
    n = int(0.09 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1600 * tt) * np.exp(-tt * 90) + np.sin(2 * np.pi * 800 * tt) * np.exp(-tt * 60) * 0.6) * db(g)



def ctasnd(t):
    put(t - 0.3, whoosh(0.6, -12)); put(t, thud(-8)); put(t + 0.5, pop(760, -11))
    for i in range(6): put(t + 1.1 + i * 0.115, key(-20))
    put(t + 1.5, pop(900, -14)); put(t + 1.8, click(-9)); put(t + 2.0, swell(1.4, -18))
if VID == '11':
    put(0.0, thud(-9)); put(0.0, ping(-16))
    for s in (0.45, 0.95, 1.4): put(s, whoosh(0.3, -13))
    put(1.8, stamp(-5)); put(1.85, thud(-5)); put(2.0, ping(-11)); put(2.2, pop(700, -14))
    put(3.8, whoosh(0.7, -13)); put(3.95, swell(2.4, -15)); put(4.2, pop(880, -13))
    put(6.3, whoosh(1.2, -15)); put(6.5, pop(640, -15)); put(7.0, pop(760, -15)); put(7.5, pop(900, -14))
    ctasnd(9.3)
elif VID == '12':
    put(0.0, thud(-7)); put(0.45, pop(600, -12)); put(0.9, pop(760, -12))
    for i in range(35):
        put(1.9 + i * 0.13 + 0.02, pop(480 + i * 11, -17))
        if i % 5 == 4: put(1.9 + i * 0.13 + 0.05, ping(-15)); put(1.9 + i * 0.13 + 0.05, thud(-15))
    put(6.5, swell(1.8, -14)); put(6.8, whoosh(0.6, -12)); put(7.4, thud(-8)); put(7.45, ping(-11))
    ctasnd(9.5)
else:
    put(0.0, thud(-7)); put(0.0, ping(-14)); put(0.3, ping(-18)); put(0.5, pop(520, -14)); put(0.7, pop(700, -14))
    for i in range(6): put(1.5 + i * 0.85 + 0.42, stamp(-13 + i * 0.5)); put(1.5 + i * 0.85, ping(-22))
    put(1.7, pop(900, -10)); put(1.75, thud(-10)); put(2.3, whoosh(0.7, -15)); put(3.1, whoosh(0.6, -18)); put(3.9, whoosh(0.7, -17)); put(4.6, thud(-15))
    put(4.0, swell(2.4, -17)); put(6.3, ping(-10)); put(6.3, pop(980, -11))
    put(7.0, stamp(-4)); put(7.05, thud(-5)); put(7.5, pop(600, -15))
    ctasnd(9.5)

mix = mix / np.abs(mix).max() * db(-1.5)
f = int(0.5 * SR); mix[-f:] *= np.linspace(1, 0, f)
wavfile.write(sys.argv[2], SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
