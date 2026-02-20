import math
import matplotlib.pyplot as plt

thrust_main_asl = 205161
thrust_main_vac = 240000
isp_main_asl = 265
isp_main_vac = 310

thrust_srb_single_asl = 250000
thrust_srb_single_vac = 300000
isp_srb_asl = 175
isp_srb_vac = 210
count_srb = 2
mass_srb_wet = 7650
mass_srb_dry = 1500

R = 600_000
mu = 3.5316e12
m_start = 26.976 * 1000
g0 = 9.80665

d = 1.25
Cd = 0.70
angle_deg = 60
angle_rad = math.radians(angle_deg)
P0 = 1.225
H_atm = 5000
S = (math.pi * d**2 / 4) * 3

def get_mass_flow(thrust, isp):
    return thrust / (isp * g0)

def get_drag_force(density, velocity, cd, S):
    return 0.5 * density * (velocity ** 2) * cd * S

def get_gravity(altitude):
    return mu / ((R + altitude) ** 2)

def get_density(altitude):
    if altitude > 70000:
        return 0.0
    return P0 * math.exp(-altitude / H_atm)

def get_Isp(Isp_asl, Isp_vac, P_h, P0):
    return Isp_vac - (Isp_vac - Isp_asl) * (P_h / P0)

def get_thrust(thrust_vac, Isp_vac, current_Isp):
    return thrust_vac * (current_Isp / Isp_vac)

fuel_srb_single = mass_srb_wet - mass_srb_dry
mdot_srb_single = get_mass_flow(thrust_srb_single_asl, isp_srb_asl)
burn_time_srb = fuel_srb_single / mdot_srb_single
mdot_main = get_mass_flow(thrust_main_asl, isp_main_asl)

time_ksp, v_ksp, m_ksp, h_ksp = [], [], [], []
raw = """Time,Surface Speed (m/s),Mass (t),Altitude from the Sea (m),Vessel DeltaV (m/s)
0,0,26.976,83,3777,
1,16.81,26.68,92.05,3577,
2,33.72,26.31,117.45,2420,
3,50.96,25.94,159.91,3525,
4.02,68.9,25.56,221.09,3506,
5.04,87.19,25.18,300.58,2348,
6.04,105.45,24.81,396.52,3462,
7.04,124.03,24.44,510.47,2300,
8.04,142.93,24.07,642.55,2281,
9.04,162.19,23.7,792.88,3406,
10.04,181.81,23.33,961.53,2235,
11.04,201.79,22.96,1148.54,2216,
12.04,222.1,22.59,1353.85,3355,
13.04,242.74,22.22,1577.35,2170,
14.04,263.77,21.85,1818.89,2150,
15.06,285.77,21.47,2083.88,3305,
16.08,308.39,21.09,2367.92,2101,
17.08,330.8,20.72,2665.03,2080,
18.08,353.21,20.35,2980.28,3251,
19.1,376.18,19.97,3319.97,2026,
20.1,399.19,19.6,3670.48,2003,
21.12,423.97,19.22,4046.42,3189,
22.12,449.74,18.85,4434.34,1942,
23.14,477.6,18.47,4851.12,3137,
24.16,507.18,18.09,5290.68,3116,
25.18,538.64,17.72,5754.64,1845,
26.2,572.06,17.34,6244.71,3055,
27.22,607.04,16.96,6762.55,1767,
28.24,642.89,16.58,7309.23,1734,
29.24,678.87,16.21,7874,2956,
30.26,716.61,15.83,8480.36,1645,
31.28,755.58,15.45,9118.4,2875,
32.3,796.03,15.08,9789.34,2839,
33.3,837.23,14.71,10480.4,1505,
34.32,880.94,14.33,11220.7,2741,
35.34,926.39,13.95,11998.31,1392,
36.36,973.54,13.57,12814.81,1344,
37.36,1021.47,13.2,13654.56,2583,
38.38,1072.26,12.82,14552.83,1216,
39.38,1124.14,12.45,15476.16,1161,
40.4,1179.45,12.07,16463.56,2400,
41.4,1236.3,11.7,17478.56,1019,
42.4,1284.57,11.39,18541.32,2546,
43.4,1293.48,11.31,19623.46,3839,
44.42,1302.94,11.23,20733.96,2506,
45.44,1313.4,11.15,21851.89,3799,
46.44,1324.48,11.07,22955.97,3783,
47.44,1336.2,10.99,24068.67,2446,
48.44,1348.56,10.91,25190.47,3739,
49.44,1361.65,10.84,26321.68,3721,
50.44,1375.31,10.76,27462.5,2381,
51.44,1389.15,10.68,28612.87,3675,
52.44,1403.18,10.6,29772.6,3656,
53.44,1417.54,10.52,30941.68,2315,
54.44,1432.31,10.44,32120.29,3608,
55.44,1447.5,10.36,33308.82,3589,
56.44,1463.1,10.28,34507.73,2246,
57.44,1479.06,10.2,35717.51,3539,
58.44,1485.41,10.16,36936.84,3525,
59.44,1478.18,10.16,38151.64,2207,
60.44,1471,10.16,39358.82,3525,
61.44,1463.87,10.16,40558.43,3525,
62.48,1455.61,10.16,41766.7,2206,
63.48,1448.57,10.16,42950.2,3566,
64.48,1441.59,10.16,44126.24,2206,
65.48,1434.65,10.16,45294.84,2206,
66.48,1427.76,10.16,46456.04,3566,
67.48,1420.91,10.16,47609.87,2206,
68.48,1414.1,10.16,48756.37,2206,
69.58,1406.46,10.16,50044.28,3566,
70.59,1399.63,10.16,51193.43,2206,
71.61,1392.82,10.16,52339.24,2206,
72.63,1386.05,10.16,53477.53,2206,
73.67,1379.09,10.16,54647.02,3566,
74.7,1372.29,10.16,55787.23,3566,
75.74,1365.51,10.16,56924.48,3566,
76.78,1358.77,10.16,58054.04,2206,
77.82,1352.06,10.16,59175.91,2206,
78.86,1345.39,10.16,60290.14,2206,
79.9,1338.76,10.16,61396.74,3566,
80.94,1332.16,10.16,62495.74,3566,
81.98,1325.6,10.16,63587.17,3566,
83.02,1319.07,10.16,64671.04,2206,
84.06,1312.59,10.16,65747.38,2206,
85.1,1306.13,10.16,66816.22,2206,
86.14,1299.71,10.16,67877.57,3566,
87.18,1293.33,10.16,68931.46,3566,
88.22,1286.97,10.16,69977.91,3566,
89.26,1280.66,10.16,71017.22,2206,
90.3,1274.37,10.16,72049.04,2206,
91.34,1268.12,10.16,73073.63,2206,
92.38,1261.91,10.16,74090.86,3566,
93.42,1255.72,10.16,75100.76,3566,
94.46,1249.57,10.16,76103.35,3566,
95.5,1243.46,10.16,77098.65,2206,
96.54,1237.37,10.16,78086.67,2206,
97.58,1231.32,10.16,79067.44,2206,
98.62,1225.3,10.16,80040.97,3566,
99.66,1219.31,10.16,81007.29,3566,
100.7,1213.41,7.05,81966.43,2014,
101.74,1207.49,7.05,82918.41,2014,
102.78,1201.6,7.05,83863.25,2014,
103.79,1195.87,7.05,84765.39,,2014,
104.79,1190.3,7.05,85616.27,2014,
105.79,1184.73,7.05,86504.29,2014,
106.79,1179.19,7.05,87385.27,2015,
107.79,1173.69,7.05,88259.71,2015,
108.79,1168.25,7.05,89127.7,2015,
109.79,1162.86,7.05,89989.47,2015,
110.79,1157.5,7.05,90845.02,2016,
111.79,1152.17,7.05,91694.34,2016,
112.79,1146.82,7.05,92537.35,2016,
113.79,1141.28,7.05,93409.25,2016,
114.84,1135.37,7.05,94332.45,2016,
115.87,1129.8,7.05,95201.57,2016,
116.87,1124.43,7.05,96036.6,2016,
118.04,1118.17,7.05,97007.02,2016,
119.19,1112.14,7.05,97940.39,2016,
120.19,1106.99,7.05,98734.85,2016,
121.19,1101.88,7.05,99522.97,2016"""

lines = raw.splitlines()
for i, line in enumerate(lines):
    if i == 0: continue
    parts = line.rstrip(',').split(",")
    if len(parts) >= 4:
        time_ksp.append(float(parts[0]))
        v_ksp.append(float(parts[1]))
        m_ksp.append(float(parts[2]) * 1000)
        h_ksp.append(float(parts[3]))


time_log, velocity_log, mass_log, altitude_log = [], [], [], []
t = 0
dt = 0.1
max_time = 120.0


velocity = 0.0
altitude = 83.0
current_mass = m_start
srb_dropped = False

while t <= max_time:
    current_thrust = 0.0
    current_mdot = 0.0

    engine_cutoff = True if t > 58.0 else False

    if not engine_cutoff:
        current_thrust += get_thrust(thrust_main_vac, isp_main_vac, current_Isp = get_Isp(isp_main_asl, isp_main_vac, get_density(altitude), P0))
        current_mdot += mdot_main

        if t < burn_time_srb:
            current_thrust += get_thrust(thrust_srb_single_vac, isp_srb_vac, current_Isp = get_Isp(isp_srb_asl, isp_srb_vac, get_density(altitude), P0)) * count_srb
            current_mdot += mdot_srb_single * count_srb

    g = get_gravity(altitude)
    rho = get_density(altitude)
    drag = get_drag_force(rho, velocity, Cd, S)

    gravity_loss = current_mass * g * math.sin(angle_rad)
    f_net = current_thrust - drag - gravity_loss
    acceleration = f_net / current_mass

    velocity += acceleration * dt
    vertical_speed = velocity * math.sin(angle_rad)
    altitude += vertical_speed * dt

    if not engine_cutoff:
        current_mass -= current_mdot * dt

    if not srb_dropped and altitude >= 80000:
        current_mass -= (mass_srb_dry * count_srb)
        srb_dropped = True

    time_log.append(t)
    velocity_log.append(velocity)
    mass_log.append(current_mass)
    altitude_log.append(altitude)

    t += dt

plt.figure(figsize=(16, 10))

plt.subplot(2, 2, 1)
plt.plot(time_log, velocity_log, "b-", label="Model (60°)", linewidth=2)
plt.plot(time_ksp, v_ksp, "r--", label="KSP Data")
plt.ylabel("Speed (m/s)")
plt.title("Скорость")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, max_time)

plt.subplot(2, 2, 2)
plt.plot(time_log, mass_log, "g-", label="Model")
plt.plot(time_ksp, m_ksp, "m--", label="KSP Data")
plt.ylabel("Mass (kg)")
plt.title("Масса")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, max_time)

plt.subplot(2, 2, 3)
plt.plot(time_log, altitude_log, "k-", label="Model")
plt.plot(time_ksp, h_ksp, "c--", label="KSP Data")
plt.ylabel("Altitude (m)")
plt.xlabel("Time (s)")
plt.title("Высота")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, max_time)

plt.tight_layout()
plt.show()