import matplotlib.pyplot as plt

dt = 1.0
g0 = 9.81

T = 205161
Isp = 265
mdot = T / (Isp * g0)

m = 6.96 * 1000
v = 757.89
dv = 0.0

time_ksp, v_ksp, m_ksp, dv_ksp = [], [], [], []

raw = """Time, Surface Speed (m/s), Mass (t), Apoapsis (m), Vessel DeltaV (m/s)
1,757.89,6.96,151738.82,1989,
3,790.4,6.88,151739.03,1953,
3,823.56,6.8,151744.08,1917,
4,857.28,6.72,151746.11,1881,
5,891.56,6.64,151744.2,1844,
6,926.44,6.56,151744,1807,
7,961.91,6.48,151747.51,1776,
8,997.94,6.41,151750.51,1738,
9,1034.53,6.33,151750.62,1699,
10,1071.7,6.25,151750.64,1660,
11,1109.45,6.17,151752.8,1620,
12,1147.77,6.09,151755.31,1580,
13,1186.66,6.01,151756.18,1539,
14,1226.15,5.93,151756.36,1507,
15,1267.06,5.85,151757.19,1464,
16,1307.76,5.77,151758.06,1422,
17,1349.06,5.69,151758.32,1379,
18,1391.01,5.61,151758.29,1336,
19,1433.6,5.53,151757.85,1291,
20,1476.83,5.46,151756.52,1246,
21,1520.71,5.38,151755.17,1200,
22,1565.29,5.3,151754.58,1164,
23,1610.58,5.22,151753.19,1117,
24,1656.57,5.14,151749.64,1069,
25,1703.27,5.06,151746.4,1021,
26,1750.75,4.98,151745.89,972,
27,1799.02,4.9,151745.28,922,
28,1848.06,4.82,151741.49,871,
29,1897.91,4.74,151739.72,830,
30,1948.63,4.66,151747.74,778,
31,1989.65,4.6,151760.42,733,
32,2026.18,4.55,151774.15,695,
33,2063.13,4.49,151807.5,657,
34,2100.57,4.44,151914.58,618,
35,2138.5,4.38,152409.98,579,
36,2161.46,4.35,157583.34,559,
37,2161.5,4.35,157592.31,556"""

lines = raw.splitlines()
for i, line in enumerate(lines):
    if i == 0:
        continue
    parts = line.rstrip(',').split(",")
    if len(parts) >= 5:
        t, vk, mk, _, dvk = parts
        time_ksp.append(float(t))
        v_ksp.append(float(vk))
        m_ksp.append(float(mk) * 1000)
        dv_ksp.append(float(dvk))

time, v_m, m_m, dv_m = [], [], [], []

t = 0
max_time = 37

while t <= max_time:
    a = T / m
    v += a * dt
    dv += a * dt
    m -= mdot * dt

    time.append(t)
    v_m.append(v)
    m_m.append(m)
    dv_m.append(1989-dv)

    t += dt

plt.figure(figsize=(12, 10))

plt.subplot(3, 1, 1)
plt.plot(time, v_m, "b-", label="Model", linewidth=2, alpha=0.8)
plt.plot(time_ksp, v_ksp, "r-", label="KSP", linewidth=2, alpha=0.8, marker='o', markersize=4)
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Speed (m/s)", fontsize=12)
plt.title("Сравнение скорости: модель vs KSP", fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')
plt.xlim(0, max_time)

plt.subplot(3, 1, 2)
plt.plot(time, m_m, "g-", label="Model", linewidth=2, alpha=0.8)
plt.plot(time_ksp, m_ksp, "m-", label="KSP", linewidth=2, alpha=0.8, marker='s', markersize=4)
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Mass (kg)", fontsize=12)
plt.title("Сравнение массы: модель vs KSP", fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')
plt.xlim(0, max_time)

plt.subplot(3, 1, 3)
plt.plot(time, dv_m, "c-", label="Model", linewidth=2, alpha=0.8)
plt.plot(time_ksp, dv_ksp, "y-", label="KSP", linewidth=2, alpha=0.8, marker='^', markersize=4)
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Delta-V (m/s)", fontsize=12)
plt.title("Сравнение Delta-V: модель vs KSP", fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, linestyle='--')
plt.xlim(0, max_time)
plt.ylim()  
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 8))

plt.subplot(1, 3, 1)
plt.plot(time, v_m, "b-", linewidth=2, label="Model")
plt.plot(time_ksp, v_ksp, "r--", linewidth=2, label="KSP")
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
plt.title("Speed Comparison")
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 2)
plt.plot(time, m_m, "g-", linewidth=2, label="Model")
plt.plot(time_ksp, m_ksp, "m--", linewidth=2, label="KSP")
plt.xlabel("Time (s)")
plt.ylabel("Mass (kg)")
plt.title("Mass Comparison")
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 3)
plt.plot(time, dv_m, "c-", linewidth=2, label="Model")
plt.plot(time_ksp, dv_ksp, "y--", linewidth=2, label="KSP")
plt.xlabel("Time (s)")
plt.ylabel("Delta-V (m/s)")
plt.title("Delta-V Comparison")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
