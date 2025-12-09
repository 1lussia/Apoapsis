import krpc
import time
def connect_to_krpc():
    try:
        conn = krpc.connect(name='Polar Orbit Mission')
        print("Подключение установлено")
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None
def initialize_mission(conn):
    vessel = conn.space_center.active_vessel
    control = vessel.control
    auto_pilot = vessel.auto_pilot

    return vessel, control, auto_pilot
def enable_rcs(control):
    control.rcs = True
    print('РСУ включен.')
    return True
def launch_and_gravity_turn(vessel, control):
    print("Наклонение на север")

    control.sas = False
    vessel.control.throttle = 1.0
    vessel.control.activate_next_stage()

    while vessel.flight().mean_altitude < 50:
        pass

    auto_pilot = vessel.auto_pilot
    auto_pilot.engage()
    auto_pilot.target_pitch_and_heading(0, 0)
    time.sleep(30)
    return True
def achieve_target_apoapsis(vessel, control, auto_pilot):
    auto_pilot.disengage()
    print("НАБОР ВЫСОТЫ ДО 150км")

    target_apoapsis = 150000

    vessel.control.throttle = 1.0

    while True:
        orbit = vessel.orbit
        apoapsis = orbit.apoapsis - 600000

        if apoapsis >= target_apoapsis + 500 and target_apoapsis < 160000:
            print(f"Достигнут целевой апоцентр: {apoapsis:.0f} м")
            control.throttle = 0.0
            break

        time.sleep(0.5)

    return True
def activate_second_stage(vessel, control):
    while vessel.flight().mean_altitude < 80000:
        time.sleep(1)

    print("Отделение ТТУ")
    control.activate_next_stage()
    return True

def polar_orbit_maneuver(vessel, conn, control, auto_pilot):
    print("Создание маневра")

    space_center = conn.space_center
    orbit = vessel.orbit

    maneuver_ut = space_center.ut + orbit.time_to_apoapsis
    node = control.add_node(maneuver_ut)

    mu = vessel.orbit.body.gravitational_parameter
    r_a = vessel.orbit.apoapsis
    r_p = vessel.orbit.periapsis
    a = (r_a + r_p) / 2
    v_a = (mu * (2 / r_a - 1 / a)) ** 0.5
    v_circ = (mu / r_a) ** 0.5

    delta_v = v_circ - v_a
    print("Δv для круговой орбиты:", delta_v, "м/с")
    node.prograde = delta_v

    auto_pilot.disengage()
    control.sas = True
    time.sleep(1)

    control.sas_mode = conn.space_center.SASMode.maneuver

    time.sleep(5)

    time_to_node = node.time_to
    while time_to_node > 20:
        time_to_node = node.time_to
        print(f"Время до маневра: {time_to_node:.1f} с")
        time.sleep(0.1)

    print("Выполнение маневра...")
    control.throttle = 1.0
    while node.remaining_delta_v > 2:
        if node.remaining_delta_v > 100 and node.remaining_delta_v < 200:
            control.throttle = 0.7
        elif node.remaining_delta_v > 10 and node.remaining_delta_v < 20:
            control.throttle = 0.2
        remaining_dv = node.remaining_delta_v
        print(f"Осталось ΔV: {remaining_dv:.1f} м/с")

        control.sas = True
        control.sas_mode = conn.space_center.SASMode.maneuver
        time.sleep(0.1)

    control.throttle = 0.0
    node.remove()
    time.sleep(2)
    final_orbit = vessel.orbit
    print(f"Финальная орбита: Перицентр={final_orbit.periapsis:.0f} м, Апоцентр={final_orbit.apoapsis:.0f} м")

    return True, print("Маневр выполнен")
def time_warp(vessel, conn):
    orbit = vessel.orbit
    warp_time = orbit.period - 200
    conn.space_center.warp_to(conn.space_center.ut + warp_time)
    return True
def landing(conn, control):
    control.sas_mode = conn.space_center.SASMode.retrograde
    time.sleep(20)
    control.throttle = 1.0
    time.sleep(40)
    control.throttle = 0.0
    time.sleep(2)
    return True
def final_stage(vessel, conn, control):
    control.activate_next_stage()
    time.sleep(5)

    print("Разворот против движения")
    control.sas = True
    control.sas_mode = conn.space_center.SASMode.retrograde

    time.sleep(5)

    return True
def main():
    print("Polar Orbit Mission")

    conn = connect_to_krpc()
    if not conn:
        return

    try:
        vessel, control, auto_pilot = initialize_mission(conn)

        mission_phases = [
            lambda: enable_rcs(control),
            lambda: launch_and_gravity_turn(vessel, control),
            lambda: achieve_target_apoapsis(vessel, control, auto_pilot),
            lambda: activate_second_stage(vessel, control),
            lambda: polar_orbit_maneuver(vessel, conn, control, auto_pilot),
            lambda: time_warp(vessel, conn),
            lambda: landing(conn, control),
            lambda: final_stage(vessel, conn, control)
        ]

        for phase in mission_phases:
            if not phase():
                break
        else:
            print("МИССИЯ ВЫПОЛНЕНА УСПЕШНО!")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
