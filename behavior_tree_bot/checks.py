

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())
def furthest_planets(state):
    dist = 0
    src=None
    dest=None
    for srcplanet in state.my_planets():
        for dest_planet in state.not_my_planets():
            if(state.distance(srcplanet.ID,dest_planet.ID) > dist):
                srcplanet = src
                dest_planet = dest
    return(src,dest)
