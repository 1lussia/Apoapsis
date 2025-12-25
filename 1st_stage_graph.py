import math
import matplotlib.pyplot as plt

dt = 1

R = 600_000
mu = 3.5316e12
g0 = 9.81

T = (250 * 2 + 205.161) * 1000
Isp = 195
mdot = T / (Isp * g0)
m = 26.976 * 1000
v = 16.54
r = R + 52
angle = math.sin(math.radians(60))

time_ksp, v_ksp, m_ksp, apo_ksp = [], [], [], []

raw = """Time, Surface Speed (m/s), Mass (t), Apoapsis (m), Vessel DeltaV (m/s)
0,16.54,26.69,100.05,3612,
1,33.44,26.32,168.46,2854,
2,50.67,25.94,284.81,3560,
3,68.25,25.57,450.8,3542,
4,86.15,25.2,667.91,2784,
5,104.38,24.83,937.28,3497,
6,122.92,24.46,1259.8,3481,
7,141.79,24.09,1636.18,2720,
8,161.01,23.72,2066.94,3442,
9,180.58,23.35,2552.21,3427,
10.02,200.91,22.97,3102.69,2660,
11.02,221.17,22.6,3695.09,3391,
12.02,241.75,22.23,4337.96,3377,
13.02,262.72,21.86,5032.43,2600,
14.02,284.23,21.49,5785.1,3341,
15.04,306.78,21.11,6619.69,2555,
16.06,329.54,20.73,7509.65,2537,
17.08,352.27,20.35,8441.18,3288,
18.08,374.65,19.98,9389.87,2487,
19.1,397.96,19.6,10410.95,3245,
20.1,422.09,19.23,11511.86,3227,
21.1,447.71,18.86,12731.04,2410,
22.1,474.87,18.49,14081.27,3176,
23.1,503.69,18.12,15580.83,3154,
24.1,534.33,17.75,17251.77,2321,
25.1,566.85,17.38,19116.97,3095,
26.1,600.97,17.01,21182.81,3068,
27.1,635.94,16.64,23432.6,2217,
28.1,671.71,16.26,25879.03,2997,
29.1,708.46,15.89,28546.2,2966,
30.1,746.36,15.52,31462.38,2097,
31.1,785.64,15.15,34663.86,2880,
32.12,827.28,14.77,38262.83,2843,
33.12,869.73,14.4,42160.45,1956,
34.14,914.77,14.02,46560.35,2740,
35.14,960.59,13.65,51333.69,2695,
36.16,1009.04,13.28,56728.43,1794,
37.16,1058.36,12.9,62607.59,2575,
38.18,1110.73,12.53,69306.36,1665,
39.18,1164.36,12.15,76685.28,1608,
40.18,1220.53,11.78,85017.89,2386,
41.2,1280.63,11.4,94676.57,1463,
42.22,1289.58,11.32,97235.94,3034,
43.22,1298.5,11.24,99804.12,3865,
44.22,1308.56,11.16,102583.27,2994,
45.22,1319.48,11.08,105544.89,2976,
46.24,1331.27,11,108725.67,3807,
47.24,1343.51,10.92,111991.75,2933,
48.24,1356.49,10.84,115388.24,2914,
49.24,1370.07,10.77,118895.82,3744,
50.24,1383.8,10.69,122451.99,2868,
51.24,1397.75,10.61,126074.36,2849,
52.26,1412.33,10.53,129885.78,3679,
53.26,1427.06,10.45,133781.64,2801,
54.28,1442.54,10.37,137948.04,3630,
55.3,1458.45,10.29,142323.9,3610,
56.3,1474.41,10.21,146823.38,2732,
57.3,1490.69,10.13,151533.4,3560"""

lines = raw.splitlines()
for i, line in enumerate(lines):
    if i == 0:
        continue
    parts = line.rstrip(',').split(",")
    if len(parts) >= 4:
        t, vk, mk, ak = parts[:4]
        time_ksp.append(float(t))
        v_ksp.append(float(vk))
        m_ksp.append(float(mk) * 1000)
        apo_ksp.append(float(ak))

time, v_m, m_m, apo_m = [], [], [], []

t = 0
max_time = 45

while t <= max_time:
    g = mu / r ** 2

    a_cent = v ** 2 / r if r > 0 else 0

    dv = (T / m - g + a_cent) * dt

    v += dv
    r += v * dt
    m -= mdot * dt

    eps = v ** 2 / 2 - mu / r

    if eps < 0:
        h = r * v * angle
        e = math.sqrt(1 + 2 * eps * h ** 2 / mu ** 2)
        a = -mu / (2 * eps)
        ra = a * (1 + e)
        apo = ra - R
    else:
        apo = float("nan")

    time.append(t)
    v_m.append(v)
    m_m.append(m)
    apo_m.append(apo)

    t += dt

plt.figure(figsize=(14, 10))

plt.subplot(3, 1, 1)
plt.plot(time, v_m, "b-", label="Model", linewidth=2, alpha=0.8)
plt.plot(time_ksp, v_ksp, "r-", label="KSP", linewidth=1.5, alpha=0.8, marker='o', markersize=3)
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Surface Speed (m/s)", fontsize=12)
plt.title("Скорость: модель vs KSP (1 этап)", fontsize=14, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, alpha=0.3, linestyle='--')
plt.xlim(0, max_time)

plt.subplot(3, 1, 2)
plt.plot(time, m_m, "g-", label="Model", linewidth=2, alpha=0.8)
plt.plot(time_ksp, m_ksp, "m-", label="KSP", linewidth=1.5, alpha=0.8, marker='s', markersize=3)
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Mass (kg)", fontsize=12)
plt.title("Масса: модель vs KSP (1 этап)", fontsize=14, fontweight='bold')
plt.legend(fontsize=11, loc='upper right')
plt.grid(True, alpha=0.3, linestyle='--')
plt.xlim(0, max_time)

plt.subplot(3, 1, 3)
apo_m_filtered = [val if not math.isnan(val) else 0 for val in apo_m]
plt.plot(time, apo_m_filtered, "c-", label="Model", linewidth=2, alpha=0.8)
plt.plot(time_ksp, apo_ksp, "y-", label="KSP", linewidth=1.5, alpha=0.8, marker='^', markersize=3)
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Apoapsis (m)", fontsize=12)
plt.title("Апоцентр: модель vs KSP (1 этап)", fontsize=14, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, alpha=0.3, linestyle='--')
plt.xlim(0, max_time)
plt.yscale('log')

plt.tight_layout()
plt.show()
