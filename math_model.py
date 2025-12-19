import math


def typical_periapsis(burn_altitude):
    periapsis_factor = 0.85

    typical_periapsis_alt = burn_altitude * periapsis_factor
    if typical_periapsis_alt < 0:
        typical_periapsis_alt = 0

    return typical_periapsis_alt


R = 600_000
mu = 3.5316e12
g0 = 9.81

target_altitude = 150_000
r_a = R + target_altitude


m_wet = 26_976
m_dry = 3_676
sum_thrust = (250 * 2 + 205.161) * 1000

Isp_boosters = 175
Isp_sustainer = 265
Isp_avg = (175 * (250*1000*2) + 265 * 205161) / sum_thrust

print("=" * 50)
print(f"Удельный импульс средний: {Isp_avg:.1f} с")

delta_v_total = Isp_avg * g0 * math.log(m_wet / m_dry)
print(f"ΔV ракеты: {delta_v_total:.1f} м/с")

periapsis_alt = typical_periapsis(70_000)
r_p = R + periapsis_alt

a_initial = (r_p + r_a) / 2

v_initial = math.sqrt(mu * (2/r_a - 1/a_initial))

v_circular = math.sqrt(mu / r_a)

print(f"\n1. Начальная орбита:")
print(f"   Перицентр: {periapsis_alt/1000:.0f} км")
print(f"   Апоцентр: {target_altitude/1000:.0f} км")
print(f"   Скорость в апоцентре: {v_initial:.1f} м/с")

energy_min = mu * (1/R - 1/r_a)

v_vertical_min = math.sqrt(2 * energy_min)

alpha = 60  # градусов
alpha_rad = math.radians(alpha)

v_needed_initial = v_vertical_min / math.sin(alpha_rad)

print(f"\n2. Требования к первому этапу:")
print(f"   Минимальная вертикальная скорость: {v_vertical_min:.1f} м/с")
print(f"   При угле {alpha}° нужна скорость: {v_needed_initial:.1f} м/с")

avg_mass = (m_wet + m_dry) / 2
acceleration = sum_thrust / avg_mass - g0

t_burn = v_needed_initial / acceleration

gravity_losses = g0 * math.sin(alpha_rad) * t_burn

print(f"   Среднее ускорение: {acceleration:.1f} м/с²")
print(f"   Время работы: {t_burn:.1f} с")
print(f"   Гравитационные потери: {gravity_losses:.1f} м/с")

delta_v_first = v_needed_initial + gravity_losses


def calculate_periapsis(dv1, theta_deg, launch_altitude=0.0):
    """
    Расчёт перицентра после первого этапа.
    dv1 - Δv первого этапа (м/с)
    theta_deg - угол к горизонту (градусы)
    launch_altitude - высота, на которой приложен импульс (м)

    возвращает высоту перицентра после первого этапа
    """
    theta = math.radians(theta_deg)

    r_start = R + launch_altitude

    vx = dv1 * math.cos(theta)
    v_total = dv1

    h = r_start * vx

    epsilon = 0.5 * v_total ** 2 - mu / r_start

    h_squared = h ** 2
    e = math.sqrt(1 + (2 * epsilon * h_squared) / (mu ** 2))

    p = h_squared / mu

    periapsis = p / (1 + e)
    return periapsis


r_a = 150000 + R
r_p = calculate_periapsis(delta_v_first, alpha, 0)
a = (r_a + r_p) / 2
v_a = (mu * (2 / r_a - 1 / a)) ** 0.5
v_circ = (mu / r_a) ** 0.5
delta_v_second = v_circ - v_a

print(f"Требуемая дельта в для второго этапа: {delta_v_second} м/с")

delta_v_required = delta_v_first + delta_v_second
print(f"\n4. Суммарная требуемая ΔV: {delta_v_required:.1f} м/с")

Z = delta_v_total - delta_v_required
print(f"\n5. Проверка:")
print(f"Доступно ΔV: {delta_v_total:.1f} м/с")
print(f"Требуется ΔV: {delta_v_required:.1f} м/с")

if Z >= 0:
    print(f"ЗАПАС: {Z:.1f} м/с")
    print("Ракета способна выполнить миссию")
else:
    print(f"НЕДОСТАТОК: {-Z:.1f} м/с")
    print("Ракета НЕ способна выполнить миссию")

print("\n" + "=" * 50)
