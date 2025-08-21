import math
import time
import cardputerlib as card
from gamepad import SeesawGamepad
import random
from micropython import const

BUTTON_PINS = [0, 1, 2, 5, 6, 16]
gamepad = SeesawGamepad(button_pins=BUTTON_PINS)
gaming = gamepad.setup() if gamepad else False

card.setrotation(1)
card.initbuff()

G = const(1.0)
show_map = False
zoom_mode = False
zoom_scale = 0.2
last_toggle = False
thrusting = False  # reset each frame
landed = False



def generate_solar_system():
    sun = {
        'pos': [0.0, 3000.0],
        'vel': [0.0, 0.0],
        'mass': 3000000.0,
        'r': 500,
        'color': [255, 255, 0]
    }
    

    new_planets = [sun]
    orbits = []
    min_orbit = 500
    max_orbit = 12000
    orbit_spacing = 1000

    num_planets = 4 + random.randint(0, 2)

    for i in range(num_planets):
        if i == 0:
            orbit_radius = random.uniform(min_orbit, int(max_orbit / 4))
        else:
            last = orbits[-1]
            orbit_radius = last + orbit_spacing + random.uniform(0, 500)
            if orbit_radius > max_orbit:
                break
        orbits.append(orbit_radius)

        angle = random.uniform(0, 2 * math.pi)
        dx = math.cos(angle)
        dy = math.sin(angle)
        x = sun['pos'][0] + dx * orbit_radius
        y = sun['pos'][1] + dy * orbit_radius

        mass = random.uniform(500, 45000)
        radius = int((mass / 90) + random.uniform(0, 5))

        speed = math.sqrt(G * (sun['mass'] + mass) / orbit_radius)
        perp_x = -dy
        perp_y = dx
        vx = sun['vel'][0] + speed * perp_x
        vy = sun['vel'][1] + speed * perp_y

        color = [random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)]

        planet = {
            'pos': [x, y],
            'vel': [vx, vy],
            'mass': mass,
            'r': radius,
            'color': color
        }

        new_planets.append(planet)

        #  Add moon if massive enough
        if mass > 25000 and random.random() < 0.50:
            moon_mass = random.uniform(10, 100)
            moon_radius = max(7, int(moon_mass / 10) + random.randint(0, 5))
            moon_distance = random.uniform(radius + 200 + moon_radius, radius + 300 + moon_radius)
            moon_angle = random.uniform(0, 2 * math.pi)
            mx = x + moon_distance * math.cos(moon_angle)
            my = y + moon_distance * math.sin(moon_angle)

            moon_speed = math.sqrt(G * (mass + moon_mass) / moon_distance)
            perp_mx = -math.sin(moon_angle)
            perp_my = math.cos(moon_angle)
            mvx = vx + moon_speed * perp_mx
            mvy = vy + moon_speed * perp_my

            moon = {
                'pos': [mx, my],
                'vel': [mvx, mvy],
                'mass': moon_mass,
                'r': moon_radius,
                'color': [200, 200, 255]
            }

            new_planets.append(moon)
    if random.random() < 0.1:
        blackhole = {
                'pos': [random.uniform(-5000, 5000), random.uniform(8000, 12000)],
                'vel': [0, 0],
                'mass': 50000000.0,
                'r': 80,
                'color': [10, 10, 10]
            }
        new_planets.append(blackhole)

    return new_planets

planets = generate_solar_system()
'''[
    {'pos': [0.0, -2370.0], 'vel': [2.779845, 0], 'mass': 30.0, 'r': 10, 'color': [255, 100, 100]},
    {'pos': [0.0, -2500.0], 'vel': [16.65151, 0], 'mass': 50000.0, 'r': 60, 'color': [255, 255, 255]},
    {'pos': [0.0, 3000.0], 'vel': [0, 0], 'mass': 3000000.0, 'r': 500, 'color': [255, 255, 0]},
    {'pos': [-3000.0, 3000.0], 'vel': [17.03, 9.73], 'mass': 10000.0, 'r': 150, 'color': [10, 1, 50]}
]'''
indexx = random.randint(1,len(planets)-1)
player = {
    'pos': [planets[indexx]['pos'][0], planets[indexx]['pos'][1]-planets[indexx]['r']+1],
    'vel': [planets[indexx]['vel'][0], planets[indexx]['vel'][1]],
    'angle': 0.0,
    'mass': 5.0
}
del indexx
def apply_gravity(a, b):
    dx = b['pos'][0] - a['pos'][0]
    dy = b['pos'][1] - a['pos'][1]
    dist_sq = dx*dx + dy*dy
    if dist_sq == 0 or dist_sq < b['r'] * b['r']:
        return
    dist = math.sqrt(dist_sq)
    force = G * a['mass'] * b['mass'] / dist_sq
    inv_mass = 1 / a['mass']
    fx = force * dx / dist
    fy = force * dy / dist
    a['vel'][0] += fx * inv_mass
    a['vel'][1] += fy * inv_mass

def keep_out_of_planets():
    global landed
    landed = False
    for p in planets:
        dx = player['pos'][0] - p['pos'][0]
        dy = player['pos'][1] - p['pos'][1]
        dist_sq = dx * dx + dy * dy
        if dist_sq < p['r'] * p['r']:
            dist = math.sqrt(dist_sq) if dist_sq > 0 else 1.0
            nx = dx / dist
            ny = dy / dist
            player['pos'][0] = p['pos'][0] + nx * p['r']
            player['pos'][1] = p['pos'][1] + ny * p['r']
            player['vel'][0] = p['vel'][0]
            player['vel'][1] = p['vel'][1]
            landed = True

def resolve_collision(a, b):
    m1, m2 = a['mass'], b['mass']
    u1x, u1y = a['vel']
    u2x, u2y = b['vel']

    a['vel'][0] = (u1x * (m1 - m2) + 2 * m2 * u2x) / (m1 + m2)
    a['vel'][1] = (u1y * (m1 - m2) + 2 * m2 * u2y) / (m1 + m2)
    b['vel'][0] = (u2x * (m2 - m1) + 2 * m1 * u1x) / (m1 + m2)
    b['vel'][1] = (u2y * (m2 - m1) + 2 * m1 * u1y) / (m1 + m2)

def separate_planets():
    for i, a in enumerate(planets):
        for j in range(i + 1, len(planets)):
            b = planets[j]
            dx = b['pos'][0] - a['pos'][0]
            dy = b['pos'][1] - a['pos'][1]
            dist_sq = dx * dx + dy * dy
            min_dist = a['r'] + b['r']
            if dist_sq < min_dist * min_dist and dist_sq > 0:
                dist = math.sqrt(dist_sq)
                overlap = min_dist - dist
                nx = dx / dist
                ny = dy / dist
                a['pos'][0] -= nx * overlap / 2
                a['pos'][1] -= ny * overlap / 2
                b['pos'][0] += nx * overlap / 2
                b['pos'][1] += ny * overlap / 2
                resolve_collision(a, b)

def planet_gravity():
    for i, a in enumerate(planets):
        for j in range(i + 1, len(planets)):
            b = planets[j]
            dx = b['pos'][0] - a['pos'][0]
            dy = b['pos'][1] - a['pos'][1]
            dist_sq = dx * dx + dy * dy
            if dist_sq == 0 or dist_sq < (a['r'] + b['r']) ** 2:
                continue
            inv_dist = 1 / math.sqrt(dist_sq)
            f = G * a['mass'] * b['mass'] * inv_dist * inv_dist
            fx = f * dx * inv_dist
            fy = f * dy * inv_dist
            a['vel'][0] += fx / a['mass']
            a['vel'][1] += fy / a['mass']
            b['vel'][0] -= fx / b['mass']
            b['vel'][1] -= fy / b['mass']

def update_player():
    for p in planets:
        apply_gravity(player, p)
    player['pos'][0] += player['vel'][0]
    player['pos'][1] += player['vel'][1]
    keep_out_of_planets()

def update_planets():
    planet_gravity()
    for p in planets:
        p['pos'][0] += p['vel'][0]
        p['pos'][1] += p['vel'][1]
    separate_planets()

def get_SOI_body_index():
    """Return index of the planet whose gravity dominates (Sphere of Influence)."""
    closest_index = None
    closest_force = 0.0
    px, py = player['pos']
    for i, p in enumerate(planets):
        if p['mass'] > 1_000_000:
            continue
        dx = px - p['pos'][0]
        dy = py - p['pos'][1]
        dist_sq = dx * dx + dy * dy
        if dist_sq == 0:
            continue
        force = G * p['mass'] / dist_sq
        if force > closest_force:
            closest_index = i
            closest_force = force
    if closest_force < 0.019:
        return 0
    return closest_index

def simulate_trajectory(index, steps=25, dt=10.0):
    sim_pos = player['pos'][:]
    sim_vel = player['vel'][:]
    sim_mass = player['mass']

    sim_planets = []
    for p in planets:
        sim_planets.append({
            'pos': p['pos'][:],
            'vel': p['vel'][:],
            'mass': p['mass']
        })
    ref_planet = sim_planets[index]

    points = [(sim_pos[0] - ref_planet['pos'][0], sim_pos[1] - ref_planet['pos'][1])]
    planet_forces = [[0.0, 0.0] for _ in sim_planets]

    for _ in range(steps):
        fx = fy = 0.0
        for forces in planet_forces:
            forces[0] = 0.0
            forces[1] = 0.0

        # Gravity on player from all planets
        for p in sim_planets:
            dx = p['pos'][0] - sim_pos[0]
            dy = p['pos'][1] - sim_pos[1]
            dist_sq = dx*dx + dy*dy
            if dist_sq < 1e-10:
                continue
            inv_dist = 1.0 / (dist_sq ** 0.5)  # one sqrt per planet-player pair per step
            inv_dist_cubed = inv_dist / dist_sq  # (1/d)^3 = (1/d) / d^2
            f = G * sim_mass * p['mass'] * inv_dist_cubed
            fx += f * dx
            fy += f * dy

        sim_vel[0] += (fx / sim_mass) * dt
        sim_vel[1] += (fy / sim_mass) * dt
        sim_pos[0] += sim_vel[0] * dt
        sim_pos[1] += sim_vel[1] * dt

        # Planet-planet gravity
        num_planets = len(sim_planets)
        for i in range(num_planets):
            for j in range(i + 1, num_planets):
                a = sim_planets[i]
                b = sim_planets[j]
                dx = b['pos'][0] - a['pos'][0]
                dy = b['pos'][1] - a['pos'][1]
                dist_sq = dx*dx + dy*dy
                if dist_sq < 1e-10:
                    continue
                inv_dist = 1.0 / (dist_sq ** 0.5)
                inv_dist_cubed = inv_dist / dist_sq
                f = G * a['mass'] * b['mass'] * inv_dist_cubed
                force_x = f * dx
                force_y = f * dy
                planet_forces[i][0] += force_x
                planet_forces[i][1] += force_y
                planet_forces[j][0] -= force_x
                planet_forces[j][1] -= force_y

        # Update planet velocities and positions
        for i, planet in enumerate(sim_planets):
            planet['vel'][0] += (planet_forces[i][0] / planet['mass']) * dt
            planet['vel'][1] += (planet_forces[i][1] / planet['mass']) * dt
            planet['pos'][0] += planet['vel'][0] * dt
            planet['pos'][1] += planet['vel'][1] * dt

        # Relative position to ref planet
        target = sim_planets[index]
        rel_x = sim_pos[0] - target['pos'][0]
        rel_y = sim_pos[1] - target['pos'][1]
        points.append((rel_x, rel_y))

    return points

def world_to_screen(x, y):
    cx, cy = player['pos']
    return int(x - cx + 120), int(y - cy + 67)

def draw():
    card.fbfill([0, 0, 0])

    # Draw planets
    for p in planets:
        px, py = world_to_screen(*p['pos'])
        card.fbcircle(px, py, p['r'], p['color'])

    # Draw player
    sx, sy = world_to_screen(*player['pos'])
    card.fbcircle(sx, sy, 2, [255, 255, 255])
    dx = math.cos(player['angle']) * 5
    dy = math.sin(player['angle']) * 5
    card.fbline(sx, sy, int(sx + dx), int(sy + dy), [0, 255, 255])

    if thrusting:
        fx = int(sx - math.cos(player['angle']) * 4)
        fy = int(sy - math.sin(player['angle']) * 4)
        card.fbrect(fx, fy, 2, 2, [255, 100, 0], True)

    # Nearest body info
    nearest = None
    nearest_dist = float('inf')
    rel_speed = 0.0

    for p in planets:
        dx = p['pos'][0] - player['pos'][0]
        dy = p['pos'][1] - player['pos'][1]
        dist = math.sqrt(dx * dx + dy * dy) - p['r']
        if dist < nearest_dist:
            nearest = p
            nearest_dist = dist
            rvx = player['vel'][0] - p['vel'][0]
            rvy = player['vel'][1] - p['vel'][1]
            rel_speed = math.sqrt(rvx * rvx + rvy * rvy)

    # Prograde/retrograde marker
    diff_angle = 0
    if rel_speed > 0.1:
        rel_angle = math.atan2(rvy, rvx)
        diff_angle = (rel_angle - player['angle']) % (2 * math.pi)
        if diff_angle > math.pi:
            diff_angle -= 2 * math.pi

        vx_dir = rvx / rel_speed
        vy_dir = rvy / rel_speed
        dot_x = int(sx + vx_dir * rel_speed)
        dot_y = int(sy + vy_dir * rel_speed)
        card.fbcircle(dot_x, dot_y, 1, [255, 0, 0])

    # HUD Text
    card.fbtext(f"VEL: {round(player['vel'][0],1)},{round(player['vel'][1],1)}", [0, 0], [0, 255, 0])
    card.fbtext(f"POS: {round(player['pos'][0],1)},{round(player['pos'][1],1)}", [0, 8], [0, 255, 0])
    if landed:
        card.fbtext("LANDED", [90, 24], [255, 0, 0])
    
    # Bottom HUD
    card.fbtext(f"ALT {int(nearest_dist)}m", [2, 120], [200, 200, 200])
    card.fbtext(f"REL {int(rel_speed)}m/s", [90, 120], [200, 200, 255])
    if abs(diff_angle) < 0.5:
        card.fbtext("PRO", [180, 120], [0, 255, 0])
    elif abs(abs(diff_angle) - math.pi) < 0.5:
        card.fbtext("RETRO", [180, 120], [255, 0, 0])

    card.fbdraw(0, 0)

def draw_map():
    global zoom_scale
    card.fbfill([0, 0, 0])

    if zoom_mode:
        cx, cy = player['pos']
        scale = zoom_scale
    else:
        xs = [p['pos'][0] for p in planets] + [player['pos'][0]]
        ys = [p['pos'][1] for p in planets] + [player['pos'][1]]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        margin = 20
        scale_x = (240 - 2 * margin) / (max_x - min_x + 1)
        scale_y = (135 - 2 * margin) / (max_y - min_y + 1)
        scale = min(scale_x, scale_y)
        cx = (min_x + max_x) / 2
        cy = (min_y + max_y) / 2

    def w2m(px, py):
        return int(120 + (px - cx) * scale), int(67 + (py - cy) * scale)

    for p in planets:
        mx, my = w2m(*p['pos'])
        r = max(1, int(p['r'] * scale))
        card.fbcircle(mx, my, r, p['color'])

    soi_index = get_SOI_body_index()
    ref_planet = planets[soi_index]
    path = simulate_trajectory(soi_index, steps=25, dt=10.0)
    ref_x, ref_y = ref_planet['pos']

    for i in range(len(path) - 1):
        x1 = path[i][0] + ref_x
        y1 = path[i][1] + ref_y
        x2 = path[i + 1][0] + ref_x
        y2 = path[i + 1][1] + ref_y
        mx1, my1 = w2m(x1, y1)
        mx2, my2 = w2m(x2, y2)
        card.fbline(mx1, my1, mx2, my2, [255, 255, 0])

    # Player
    px, py = w2m(*player['pos'])
    card.fbcircle(px, py, 2, [255, 255, 255])
    dx = math.cos(player['angle']) * 8
    dy = math.sin(player['angle']) * 8
    card.fbline(px, py, int(px + dx), int(py + dy), [0, 255, 255])

    # SOI line
    sx, sy = w2m(*ref_planet['pos'])
    card.fbline(px, py, sx, sy, [0, 100, 255])

    card.fbtext(f"MAP MODE {'(Zoom)' if zoom_mode else ''} - m to exit", [5, 5], [0, 255, 0])
    if landed:
        card.fbtext("LANDED", [90, 24], [255, 0, 0])
    card.fbdraw(0, 0)

def handle_input():
    global show_map, zoom_mode, zoom_scale, last_toggle, thrusting
    thrusting = False
    keys = card.pressed()
    joy_x, joy_y = 500, 500
    btns = []
    if gaming:
        joy_x, joy_y = gamepad.read_joystick()
        btns = gamepad.read_buttons()

    # Toggle map
    toggle = ('m' in keys) or (16 in btns)
    if toggle and not last_toggle:
        show_map = not show_map
    last_toggle = toggle

    # Zoom toggle
    if show_map and ('i' in keys or 6 in btns):
        zoom_mode = not zoom_mode
    if zoom_mode:
        if '=' in keys or '+' in keys or 5 in btns:
            zoom_scale *= 1.2
        if '-' in keys or '_' in keys or 1 in btns:
            zoom_scale /= 1.2

    # Rotation
    if joy_x >= 716 or 'a' in keys:
        player['angle'] -= 0.4
    if joy_x <= 292 or 'd' in keys:
        player['angle'] += 0.4

    # Thrust
    if 2 in btns or 'e' in keys:
        thrust = 1.4
        player['vel'][0] += thrust * math.cos(player['angle'])
        player['vel'][1] += thrust * math.sin(player['angle'])
        thrusting = True
    if card.pressing(['0']):
        thrust = 6
        player['vel'][0] += thrust * math.cos(player['angle'])
        player['vel'][1] += thrust * math.sin(player['angle'])
        thrusting = True

    # Match orbit
    if card.pressing(['o']):
        nearest = None
        nearest_dist = float('inf')
        for p in planets:
            dx = player['pos'][0] - p['pos'][0]
            dy = player['pos'][1] - p['pos'][1]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < nearest_dist:
                nearest = p
                nearest_dist = dist
        if nearest and nearest_dist > 1:
            dx = nearest['pos'][0] - player['pos'][0]
            dy = nearest['pos'][1] - player['pos'][1]
            dist = math.sqrt(dx * dx + dy * dy)
            speed = math.sqrt(G * nearest['mass'] / dist)
            tx = -dy / dist
            ty = dx / dist
            player['vel'][0] = nearest['vel'][0] + tx * speed
            player['vel'][1] = nearest['vel'][1] + ty * speed

    if 'BSPC' in keys:
        reset_game()
    if 0 in btns or 'q' in keys:
        return False
    return True

def reset_game():
    global planets
    planets = generate_solar_system()
    indexx = random.randint(1,len(planets)-1)
    player['pos'] = [planets[indexx]['pos'][0], planets[indexx]['pos'][1]-planets[indexx]['r']+1]
    player['vel'] = [planets[indexx]['vel'][0], planets[indexx]['vel'][1]]
    player['angle'] = 0.0
    del indexx

def main():
    while True:
        if not handle_input():
            break
        update_planets()
        update_player()
        if show_map:
            draw_map()
        else:
            draw()
        time.sleep(0.01)

main()


