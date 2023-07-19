import sys
import math
sys.path.insert(0, '../')
from planet_wars import issue_order

def dist(A, B):
    return math.sqrt(pow(A[0] - B[0], 2) + pow(A[1] - B[1], 2))

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    
def atk_close(state):
    if len(state.my_planets()) == 0:
        return False
    
    wk_planet = min(state.enemy_planet(), key = lambda p: p.num_ships, default = None)
    wk_ships = wk_planet.num_ships
    closest = max(state.my_planets(), key=lambda p: p.num_ships, default = None)
    distance = dist([wk_planet.x, wk_planet.y], [closest.x, closest.y])

    for planet in state.my_planets():
        tDist = state.distance(planet.ID, wk_planet.ID)
        if tDist < distance & planet.num_ships > (wk_ships + 3):
            closest = planet
            distance = tDist

    return issue_order(state, closest.ID, wk_planet.ID, wk_ships + 3)
#adapted and inspired from spread_bot
def spread_atk(state):
    my_planets = iter(sorted(state.my_planets(), key = lambda p: p.num_ships))
    options = [planet for planet in state.not_my_planets() 
                         if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    
    options.sort(key = lambda p: p.num_ships)
    select = iter(options)
    try:
        planet_iter = next(my_planets)
        option_iter = next(select)
        while True:
            tShips = option_iter.num_ships + 1

            if option_iter in state.enemy_planets():
                tShips = option_iter.num_ships + \
                    state.distance(planet_iter.ID, option_iter.ID) * option_iter.growth_rate + 1
                 
            if planet_iter.num_ships > tShips:
                issue_order(state, planet_iter.ID, option_iter.ID, tShips)
                planet_iter = next(my_planets)
                option_iter = next(select)
            else:
                planet_iter = next(my_planets)

    except StopIteration:
        return False

    
