import math

def calculate_orbital_velocity(pos_a, mass_a, pos_b, mass_b, vel_a, G=1):
    """
    pos_a: [x, y] of massive planet (A)
    mass_a: mass of planet A
    pos_b: [x, y] of orbiting planet (B)
    mass_b: mass of planet B
    vel_a: [vx, vy] of planet A
    G: gravity constant

    Returns: [vx, vy] velocity of planet B for circular orbit around barycenter
    """

    dx = pos_b[0] - pos_a[0]
    dy = pos_b[1] - pos_a[1]
    dist = math.sqrt(dx**2 + dy**2)

    # Orbital speed using reduced mass (mu = G * (m1 + m2))
    speed = math.sqrt(G * (mass_a + mass_b) / dist)

    # Perpendicular direction (normalized)
    perp_x = -dy / dist
    perp_y = dx / dist

    # Add planet A's velocity to get final absolute velocity
    vel_bx = vel_a[0] + speed * perp_x
    vel_by = vel_a[1] + speed * perp_y

    return [vel_bx, vel_by]

pos_a = list(map(float, input("pos_a (x y): ").split()))
mass_a = float(input("mass_a: "))
pos_b = list(map(float, input("pos_b (x y): ").split()))
mass_b = float(input("mass_b: "))
vel_a = list(map(float, input("vel_a (vx vy): ").split()))

print("Required velocity for planet B:")
print(calculate_orbital_velocity(pos_a, mass_a, pos_b, mass_b, vel_a))
