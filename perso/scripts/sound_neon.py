import sys, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

import sys
SR = 48000; VID = sys.argv[1]; DUR = {'8':22.5,'9':20.5,'10':23.5}[VID]
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


def heart(g=-8):
    n = int(0.42 * SR); tt = np.arange(n) / SR
    b = lambda d: np.where(tt >= d, np.sin(2*np.pi*52*(tt-d)) * np.exp(-(tt-d)*22), 0)
    return (b(0) + 0.7 * b(0.16)) * db(g)
def sea(d, g=-30):
    n = int(d * SR); x = lp(bp(rng.standard_normal(n), 200, 900), 700); tt = np.arange(n) / SR
    x = x / np.abs(x).max() * (0.6 + 0.4 * np.sin(2 * np.pi * 0.28 * tt))
    return x * db(g)
if VID == '8':
    put(0.0, thud(-8)); put(0.5, pop(520, -14)); put(0.8, pop(700, -14)); put(1.0, whoosh(0.6, -18))
    k = 1.3
    while k < 8.4:
        put(k, key(-27)); k += rng.uniform(0.09, 0.2)
    for i in range(7): put(1.5 + i * 0.8 + 0.4, stamp(-13 + i * 0.6)); put(1.5 + i * 0.8, whoosh(0.35, -22))
    put(1.5, swell(3.0, -20)); put(3.0, thud(-18))
    for i in range(4): put(6.0 + i * 1.45 + 0.42, thud(-11)); put(6.0 + i * 1.45 + 0.44, pop(420 + 40 * i, -16))
    for i, s in enumerate([8.95, 9.05, 9.18, 9.3, 9.42, 9.55, 9.7]): put(s, stamp(-7 - i * 0.6))
    put(8.9, whoosh(0.8, -10)); put(9.6, thud(-5))
    put(12.4, ping(-12)); put(12.4, swell(2.0, -16))
    for i in range(4): put(12.4 + i * 0.12, pop(760 + 90 * i, -14))
    put(14.4, whoosh(0.7, -12)); put(14.8, swell(2.6, -17)); put(15.6, pop(600, -15)); put(17.8, pop(900, -16))
    put(19.3, whoosh(0.6, -12)); put(19.6, thud(-9)); put(20.5, click(-9)); put(20.8, pop(980, -14))
elif VID == '9':
    put(0.0, thud(-10))
    for i in range(6):
        t0 = 0.55 + i * 0.8
        put(t0, whoosh(0.4, -20)); put(t0 + 0.42, thud(-10 + i * 1.1)); put(t0 + 0.44, stamp(-16 + i))
    k, gap = 2.4, 0.9
    while k < 7.2:
        put(k, heart(-16 + (k - 2.4) * 1.6)); k += gap; gap = max(0.5, gap * 0.9)
    put(5.3, stamp(-8)); put(6.3, whoosh(0.7, -14)); put(7.2, whoosh(0.9, -14)); put(8.1, thud(-12))
    put(7.9, swell(4.0, -14))
    for j in range(6): put(8.3 + j * 0.38, pop(520 + 90 * j, -13)); put(8.3 + j * 0.38, whoosh(0.5, -22))
    k = 8.4
    while k < 16.4:
        put(k, heart(-22)); k += 1.05
    put(11.4, swell(3.0, -17)); put(11.85, pop(640, -15)); put(12.4, pop(720, -15)); put(14.6, pop(900, -17))
    put(16.5, whoosh(0.6, -12)); put(17.0, thud(-9)); put(17.9, click(-9)); put(18.2, pop(980, -14))
else:
    put(0.0, thud(-10)); put(0.25, swell(1.4, -18)); put(0.7, pop(640, -15))
    put(0.0, sea(13.8, -31) * np.interp(np.arange(int(13.8 * SR)) / SR, [0, 1.5, 12.5, 13.8], [0, 1, 1, 0.6]))
    for i in range(100):
        put(1.6 + (i + 1) * 0.12 - 0.01, pop(500 + i * 3.6, -21 + i * 0.05))
    for m in (25, 50, 75): put(1.6 + m * 0.12, ping(-17)); put(1.6 + m * 0.12, thud(-16))
    put(13.6, thud(-5)); put(13.6, ping(-10)); put(13.6, swell(2.6, -13)); put(13.75, whoosh(1.2, -10))
    put(14.5, pop(760, -11)); put(15.3, pop(600, -16)); put(17.2, pop(900, -17))
    put(20.1, whoosh(0.6, -12)); put(20.5, thud(-9)); put(21.4, click(-9)); put(21.7, pop(980, -14))

mix = mix / np.abs(mix).max() * db(-1.5)
f = int(0.5 * SR); mix[-f:] *= np.linspace(1, 0, f)
wavfile.write(sys.argv[2], SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
