# Allows us to interact with robot hardware (motors, servos, camera):
from sr.robot3 import * 
robot = Robot()

#=======================================================================================

# Contents:

#   - SUBROUTINES FOR BASIC MOVEMENTS (Done)
#   - SUBROUTINES FOR A SPECIFIC COMBINATION OF MOVEMENTS (TEST)
#   - SUBROUTINES FOR RECORDING OR EDITING DATA (Done)
#   - SUBROUTINES FOR ASTEROIDS (Done)
#   - SUBROUTINES FOR HOME PLANET (Done) 
#   - SUBROUTINES FOR SPACESHIP (WIP)
#   - SUBROUTINES FOR EGG (WIP)
#   - ASSIGNING ROBOT HARDWARE (Done)
#   - INITIALIZING VARIABLES (Done)
#   - MAIN PROGRAM (WIP)


#=======================================================================================

# SUBROUTINES FOR BASIC MOVEMENTS (Done)

def move_robot():
    left_motor.power = 0.5
    right_motor.power = 0.5

def reverse_robot():
    left_motor.power = -0.5
    right_motor.power = -0.5

def stop_robot():
    left_motor.power = 0
    right_motor.power = 0

def rotate_left(motor_power):
    left_motor.power = -(motor_power)
    right_motor.power = motor_power

def rotate_right(motor_power):
    left_motor.power = motor_power
    right_motor.power = -(motor_power)

def close_clamps():
    left_clamp.position = 1
    right_clamp.position = 1

def open_clamps():
    left_clamp.position = -1
    right_clamp.position = -1

def raise_clamps(lift_position): 
    lift.position = lift_position

def lower_clamps(): # To rest position
    lift.position = -1

# SUBROUTINES FOR A SPECIFIC COMBINATION OF MOVEMENTS (Done)

def deposit_asteroid_into_spaceship(): # Done
    raise_clamps(1)
    robot.sleep(3)
    move_robot()
    robot.sleep(0.25)
    stop_robot()
    robot.sleep(0.1)
    open_clamps()
    robot.sleep(0.5)
    reverse_robot()
    lower_clamps()
    robot.sleep(1)
    stop_robot()

def deposit_object_into_planet(): # Done
    open_clamps()
    reverse_robot()
    robot.sleep(1)
    stop_robot()

def clamp_onto_team_spaceship(): # TEST
    raise_clamps(1) 
    robot.sleep(3)
    move_robot()
    robot.sleep(0.2)
    stop_robot()
    robot.sleep(0.1)
    open_clamps()
    robot.sleep(0.5)
    raise_clamps(0.1)
    robot.sleep(3)
    reverse_robot()
    robot.sleep(1)
    stop_robot()

def deposit_team_spaceship(): # TEST
    rotate_left(0.2)
    robot.sleep(0.2)
    stop_robot()
    raise_clamps(1)
    reverse_robot()
    robot.sleep(1)
    stop_robot()

# SUBROUTINES FOR RECORDING OR EDITING DATA (Done)

def record_time(start_time): # Done
    end_time = robot.time()
    elapsed_time = (end_time - start_time)
    return elapsed_time

def take_photo(): # Done
    robot.sleep(0.1)
    while True:
        view = robot.camera.see()
        break
    return view

def identify_zone(): # Done
    arena_boundary_marker_numbers = []
    zone_number = robot.zone
    if zone_number == 0:
        arena_boundary_marker_numbers = [0,1,2,3,4,5,6]
    elif zone_number == 1:
        arena_boundary_marker_numbers = [7,8,9,10,11,12,13]
    elif zone_number == 2:
        arena_boundary_marker_numbers = [14,15,16,17,18,19,20]
    elif zone_number == 3:
        arena_boundary_marker_numbers = [21,22,23,24,25,26,27]
    return arena_boundary_marker_numbers

def update_points(asteroid_marker_number, points, point_change): # Done
    points += point_change
    if point_change == 40:
        asteroids_in_spaceship_marker_numbers.append(asteroid_marker_number)
    elif point_change == -40:
        asteroids_in_spaceship_marker_numbers.remove(asteroid_marker_number)
    elif point_change == 12:
        asteroids_in_home_planet_marker_numbers.append(asteroid_marker_number)
    elif point_change == -12:
        asteroids_in_home_planet_marker_numbers.remove(asteroid_marker_number)
    print(f"Asteroid in spaceship marker numbers: \
  {asteroids_in_spaceship_marker_numbers}")
    print(f"Asteroid in home planet marker numbers: \
  {asteroids_in_home_planet_marker_numbers}")
    print(f"Current points: {points}")
    return points

# SUBROUTINES FOR ASTEROIDS (WIP)

def face_closest_asteroid(points): # Done
  # Turns until at least one asteroid is in view:
  rotate_left(0.2)
  asteroid_in_view = None
  while asteroid_in_view is not True:
      view = take_photo()
      for marker in view:
          if (marker.id in asteroid_marker_numbers
          and marker.id not in asteroids_in_spaceship_marker_numbers
          and marker.id not in asteroids_in_home_planet_marker_numbers):
              asteroid_in_view = True
  stop_robot()
  # Finds the asteroid in view with the closest distance:
  view = take_photo()
  distance_from_asteroid = None
  asteroid_marker_number = None
  asteroid_distances = []
  for marker in view:
      if (marker.id in asteroid_marker_numbers
      and marker.id not in asteroids_in_spaceship_marker_numbers
      and marker.id not in asteroids_in_home_planet_marker_numbers):
          distance_from_asteroid = marker.position.distance
          asteroid_distances.append(distance_from_asteroid)
  asteroid_distances.sort()
  closest_asteroid_distance = asteroid_distances[0]
  for marker in view:
      if (marker.position.distance == closest_asteroid_distance
      and marker.id in asteroid_marker_numbers
      and marker.id not in asteroids_in_spaceship_marker_numbers
      and marker.id not in asteroids_in_home_planet_marker_numbers):
          asteroid_marker_number = marker.id 
  print(f"Closest asteroid marker number: {asteroid_marker_number}")
  # Removes added points for asteroids that the robot failed to take:
  view = take_photo()
  for marker in view:
      if marker.id in asteroids_in_spaceship_marker_numbers:
          points = update_points(marker.id, points, -40)
      if marker.id in asteroids_in_home_planet_marker_numbers:
          points = update_points(marker.id, points, -12)
  return asteroid_marker_number, points


def travel_to_closest_asteroid(asteroid_marker_number, asteroid_has_been_stolen): # Done
    move_robot()
    marker_is_in_spaceship = False
    asteroid_has_been_stolen = False
    previous_distance_from_asteroid = float('inf')
    current_distance_from_asteroid = float('inf')
    count = 0
    at_asteroid = None
    while at_asteroid is not True and asteroid_has_been_stolen is False:
        # Records whether the asteroid is in its view:
        view_of_closest_asteroid = []
        view = take_photo()
        for marker in view:
            if (marker.id == asteroid_marker_number
                and marker.id not in asteroids_in_spaceship_marker_numbers
                and marker.id not in asteroids_in_home_planet_marker_numbers):
                view_of_closest_asteroid.append(marker.id)
                if marker.position.distance < 3000 and not marker_is_in_spaceship:
                   if marker.position.vertical_angle > 0.1:
                      marker_is_in_spaceship = True
                      asteroid_has_been_stolen = True
                      asteroids_in_spaceship_marker_numbers.append(marker.id)            
                      break
        # Corrects orientation to face asteroid while moving:
        for marker in view:
            if (marker.id == asteroid_marker_number
                and marker.id not in asteroids_in_spaceship_marker_numbers
                and marker.id not in asteroids_in_home_planet_marker_numbers):
                angle_from_robot = marker.position.horizontal_angle
                if angle_from_robot > 0.1: # Right
                    rotate_right(0.3)
                    robot.sleep(0.1)
                    move_robot()
                elif angle_from_robot < -0.1: # Left
                    rotate_left(0.3)
                    robot.sleep(0.1)
                    move_robot()
                previous_distance_from_asteroid = current_distance_from_asteroid
                current_distance_from_asteroid = marker.position.distance
                break
        # Checks whether robot is stuck:
        if current_distance_from_asteroid == previous_distance_from_asteroid: # WIP
            count += 1
        if count > 3:
            reverse_robot()
            robot.sleep(2)
            stop_robot()
            break
        # Checks whether closest asteroid is no longer in view:
        if asteroid_marker_number not in view_of_closest_asteroid:
            robot.sleep(0.5)
            stop_robot()
            reverse_robot()
            robot.sleep(0.25)
            stop_robot()
            at_asteroid = True
    # Checks if asteroid has been stolen by an enemy while travelling to it:
    if current_distance_from_asteroid > 700 or count > 3 or marker_is_in_spaceship:
        asteroid_has_been_stolen = True
    elif current_distance_from_asteroid < 700:
        asteroid_has_been_stolen = False
    return asteroid_has_been_stolen

# SUBROUTINES FOR HOME PLANET (Done)

def face_home_planet(): # Done
    # Turns until the arena boundary marker numbers for the home planet is in view:
    rotate_right(0.2)
    arena_boundary_marker_number = None
    home_planet_in_view = None
    while home_planet_in_view is not True:
        view = take_photo()
        for marker in view:
            if marker.id in arena_boundary_marker_numbers[2:5]:
                home_planet_in_view = True
    stop_robot()
    # Finds the arena boundary marker number with the closest distance:
    view = take_photo()
    distance_from_home_planet = None
    arena_boundary_marker_number = None
    arena_boundary_distances = []
    for marker in view:
        if marker.id in arena_boundary_marker_numbers[2:5]:
            distance_from_home_planet = marker.position.distance
            arena_boundary_distances.append(distance_from_home_planet)
    arena_boundary_distances.sort()
    closest_arena_boundary_distance = arena_boundary_distances[0]
    for marker in view:
        if (marker.position.distance == closest_arena_boundary_distance
            and marker.id in arena_boundary_marker_numbers[2:5]):
            arena_boundary_marker_number = marker.id
    print(f"Closest arena boundary marker number: {arena_boundary_marker_number}")
    return arena_boundary_marker_number

def travel_to_planet(arena_boundary_marker_number): # Done
    move_robot()
    distance_from_planet = float("inf")
    at_planet = None
    while at_planet is not True:
        while distance_from_planet > 600:
            view = take_photo()
            # Corrects orientation to face arena boundary marker while moving:
            for marker in view:
                if marker.id == arena_boundary_marker_number:
                    angle_from_robot = marker.position.horizontal_angle
                    if angle_from_robot > 0.1: # Right
                        rotate_right(0.3)
                        robot.sleep(0.1)
                        move_robot()
                    elif angle_from_robot < -0.1: # Left
                        rotate_left(0.3)
                        robot.sleep(0.1)
                        move_robot()
                    distance_from_planet = marker.position.distance
                    break
        stop_robot()
        at_planet = True
        # Checks for asteroid that have accidently been dragged by robot to the home planet:
        for marker in robot.camera.see():
           if not (marker.id in arena_boundary_marker_numbers or marker.id in asteroids_in_home_planet_marker_numbers or marker.id in asteroids_in_spaceship_marker_numbers):
              asteroids_in_home_planet_marker_numbers.append(marker.id)

# SUBROUTINES FOR SPACESHIP (Done)

def face_team_spaceship(team_spaceship_marker_number, team_spaceship_in_home_planet, closest_arena_boundary_marker_number, team_spaceship_has_been_stolen): # Done
    # Turns until the spaceship is in view:
    rotate_left(0.2)
    number_of_times_arena_boundary_has_been_seen = 0
    arena_boundary_was_out_of_view = False
    team_spaceship_in_view = None
    # Checks whether team spaceship is in home planet:
    if team_spaceship_in_home_planet is True:
        while team_spaceship_in_view is not True:
            view = take_photo()
            for marker in view:
                range = marker.position.distance
                if ((team_spaceship_marker_number is None 
                    and marker.id in spaceship_marker_numbers 
                    and range < 1700) 
                    or (marker.id == team_spaceship_marker_number
                    and range < 1700)):
                    team_spaceship_in_home_planet = True
                    print("Team spaceship is in home planet")
                    print(f"Team spaceship marker number: {team_spaceship_marker_number}")
                    team_spaceship_marker_number = marker.id
                    stop_robot()
                    team_spaceship_in_view = True
                    break
                elif (marker.id == team_spaceship_marker_number
                        and range > 1700):
                    team_spaceship_in_home_planet = False
                    print("Team spaceship is not in home planet")
                    stop_robot()
                    team_spaceship_in_view = True
                    break
            if team_spaceship_in_view is False:
                view_of_arena_boundary_marker_number = []
                for marker in view:
                    if marker.id == closest_arena_boundary_marker_number:
                        view_of_arena_boundary_marker_number.append(marker.id)
                        if number_of_times_arena_boundary_has_been_seen == 0 and arena_boundary_was_out_of_view is True:
                            number_of_times_arena_boundary_has_been_seen += 1
                if number_of_times_arena_boundary_has_been_seen == 1 and closest_arena_boundary_marker_number not in view_of_arena_boundary_marker_number:
                    arena_boundary_was_out_of_view = True
                if number_of_times_arena_boundary_has_been_seen > 1: # If the arena boundary has appeared more than once without the robot seeing the team spacehsip, it has probably been taken
                    team_spaceship_in_home_planet = False
                    print("Team spaceship is not in home planet")
                    stop_robot()
                    team_spaceship_in_view = True
    elif team_spaceship_in_home_planet is False:
        while team_spaceship_in_view is not True:
            # Looks for team spaceship to retrieve it
            view = take_photo()
            for marker in view:
                if marker.id == team_spaceship_marker_number:
                    stop_robot()
                    team_spaceship_in_view = True   
    if team_spaceship_in_home_planet is False:
        team_spaceship_has_been_stolen = True
    return team_spaceship_marker_number, team_spaceship_in_home_planet, team_spaceship_has_been_stolen

def travel_to_spaceship(spaceship_marker_number, team_spaceship_in_home_planet): # Done
    move_robot()
    distance_from_spaceship = float("inf")
    range_from_robot = 0
    # Checks whether or not its going to retrieve the team spaceship and adjusts the range accordingly:
    if team_spaceship_in_home_planet is True:
        range_from_robot = 500
    elif team_spaceship_in_home_planet is False:
        range_from_robot = 1000
    at_spaceship = None
    while at_spaceship is not True:
        while distance_from_spaceship > range_from_robot:
            view = take_photo()
            # Corrects orientation to face spaceship:
            for marker in view:
                if marker.id == spaceship_marker_number:
                    angle_from_robot = marker.position.horizontal_angle
                    if angle_from_robot > 0.1: # Right
                        rotate_right(0.3)
                        robot.sleep(0.1)
                        stop_robot()
                    elif angle_from_robot < -0.1: # Left
                        rotate_left(0.3)
                        robot.sleep(0.1)
                        stop_robot()
                    move_robot()
                    distance_from_spaceship = marker.position.distance
        stop_robot()
        at_spaceship = True

# SUBROUTINES FOR EGG (WIP)

def face_egg(): # Done
    # Turn until egg is in view:
    rotate_left(0.2)
    egg_in_view = None
    while egg_in_view is not True:
        view = take_photo()
        for marker in view:
            if marker.id == 110:
                stop_robot()
                egg_in_view = True

def travel_to_egg(): # Done
    move_robot()

    marker_number = 110
    at_egg = False

    move_robot()
    raise_clamps(-0.75)

    distanceAfter = 1
    distanceBefore = None

    while not at_egg:
        robot.sleep(0.1)
        marker_in_view = False
        count = 0

        if count >= 5:
            # The distance of the egg has not changed for a while, but it is moving towards the egg, so the robot must be stuck
            stop_robot()
            close_clamps()
            robot.sleep(1)
            reverse_robot()
            robot.sleep(1)
            stop_robot()
            open_clamps()
            reverse_robot()
            robot.sleep(1)
            stop_robot()
            move_robot()

            count = 0
            distanceAfter = 1
            distanceBefore = None

        for marker in robot.camera.see():
            if marker.id == marker_number:
                marker_in_view = True

                if distanceAfter == distanceBefore:
                    count += 1
                else:
                    distanceBefore = distanceAfter

                distanceAfter = marker.position.distance

                if marker.position.distance <= 300:
                    at_egg = True
                    stop_robot()
                    print("Stopped robot at egg")
                    break
                elif marker.position.horizontal_angle > 0.1:
                    rotate_right(0.1)
                    robot.sleep(0.1)
                    move_robot()
                elif marker.position.horizontal_angle < -0.1:
                    rotate_left(0.1)
                    robot.sleep(0.1)
                    move_robot()

        if not marker_in_view:
            at_egg = True
            stop_robot()
            print("Stopped robot at egg")
            break

    close_clamps()
    robot.sleep(1)
    reverse_robot()
    robot.sleep(1)
    stop_robot()

# SUBROUTINES FOR ENEMY PLANET

def face_enemy_planet():
    # Turns until the arena boundary marker numbers...
    # ...for the enemy planet is in view:
  
    rotate_right(0.2)
    angle = None
    distance = None
    closest_distance = None
    marker_number = None
    distances = []
    marker_in_view = False
  
    while True:
        while marker_in_view is False:
            robot.sleep(0.1)
            for marker in robot.camera.see():
                for i in arena_boundary_marker_numbers[2:5]:
                    if i > 20:
                        if marker.id == i - 14:
                            angle = marker.position.horizontal_angle
                            marker_in_view = True
                            marker_number = marker.id
                            stop_robot()
                            break
                    else:
                        if marker.id == i + 14:
                            angle = marker.position.horizontal_angle
                            marker_in_view = True
                            marker_number = marker.id
                            stop_robot()
                            break
        break
  
    for marker in robot.camera.see():
        if marker.id == marker_number:
            if marker.position.horizontal_angle > 0:
                rotate_right(0.2)
  
                for marker in robot.camera.see():
                    if marker.id == marker_number:
                        if marker.position.horizontal_angle < 0.1 and marker.position.horizontal_angle > -0.1:
                            stop_robot()
            else:
                rotate_left(0.2)
  
                for marker in robot.camera.see():
                    if marker.id == marker_number:
                        if marker.position.horizontal_angle < 0.1 and marker.position.horizontal_angle > -0.1:
                            stop_robot()

    return marker_number

def travel_to_enemy_planet(marker_number):
    at_planet = False
    move_robot()
  
    count = 0
    while not at_planet:
        robot.sleep(0.1)
        marker_in_view = False
  
        distanceAfter = 1
        distanceBefore = None
  
        if count >= 10:
            # The distance of the egg has not changed for a while, but it is moving towards the egg, so the robot must be stuck
            stop_robot()
            close_clamps()
            robot.sleep(1)
            reverse_robot()
            robot.sleep(1)
            stop_robot()
            open_clamps()
            reverse_robot()
            robot.sleep(1)
            stop_robot()
            move_robot()
  
            count = 0
            distanceAfter = 1
            distanceBefore = None
  
        for marker in robot.camera.see():
            if marker.id == marker_number:
                marker_in_view = True
  
                if distanceAfter == distanceBefore:
                    count += 1
                else:
                    distanceBefore = distanceAfter
  
                distanceAfter = marker.position.distance
  
                if marker.position.distance <= 750:
                    at_planet = True
  
                    stop_robot()
                    print("Stopped robot at enemy planet")
  
                    break
                elif marker.position.horizontal_angle > 0.1:
                    rotate_right(0.1)
                    robot.sleep(0.1)
                    move_robot()
                elif marker.position.horizontal_angle < -0.1:
                    rotate_left(0.1)
                    robot.sleep(0.1)
                    move_robot()
  
        if not marker_in_view:
            reverse_robot()
            robot.sleep(0.5)
            face_enemy_planet()

#=======================================================================================

# ASSIGNING ROBOT HARDWARE (Done)

# Assigns motor (wheels) and servos (clamps) to variables
left_motor = robot.motor_boards['srABC1'].motors[0]
right_motor = robot.motor_boards['srABC1'].motors[1]
left_clamp = robot.servo_board.servos[0]
right_clamp = robot.servo_board.servos[1]
lift = robot.servo_board.servos[2]

#=======================================================================================

# INITIALIZING VARIABLES (Done)

# Initialises the time in which a match starts
start_of_match = robot.time()
duration_of_match = 0
# Initialise points
points = 0
# Identifies arena boundary depending on zone number
arena_boundary_marker_numbers = identify_zone()
# Creates a list to store all possible asteroid marker numbers
asteroid_marker_numbers = list(range(150,200))
# Creates a list for asteroids in spaceship
asteroids_in_spaceship_marker_numbers = []
# Creates a list for asteroids in home planet
asteroids_in_home_planet_marker_numbers = []
# Initialises astroid state while travelling to it
asteroid_has_been_stolen = None
# Assigns all possible spaceship marker numbers into a list
spaceship_marker_numbers = [120,121,122,123,125,126,127,128]
# Identifies team spaceship marker number
team_spaceship_marker_number = None
# Initialises team spaceship location
team_spaceship_in_home_planet = True
team_spaceship_has_been_stolen = False
# Initalises egg location
egg_in_home_planet = False
egg_in_team_spaceship = False

#=======================================================================================

# MAIN PROGRAM (WIP)

# 1. Collects three asteroids, one after another, and deposits them into the team spaceship
while len(asteroids_in_spaceship_marker_numbers) < 3 and team_spaceship_has_been_stolen is False:
    # Identifies closest asteroid and travels to it
    closest_asteroid_marker_number, points = face_closest_asteroid(points)
    asteroid_has_been_stolen = travel_to_closest_asteroid(closest_asteroid_marker_number, asteroid_has_been_stolen)
    if asteroid_has_been_stolen is False: # If an asteroid has been stolen while travelling to it, it will find another asteroid
        # Collects asteroid
        close_clamps()
        robot.sleep(0.3)
        # Faces home planet
        closest_arena_boundary_marker_number = face_home_planet()
        # Travels to home planet
        travel_to_planet(closest_arena_boundary_marker_number)
        # Faces team spaceship
        team_spaceship_marker_number, team_spaceship_in_home_planet, team_spaceship_has_been_stolen = face_team_spaceship(team_spaceship_marker_number, team_spaceship_in_home_planet, closest_arena_boundary_marker_number, team_spaceship_has_been_stolen)
        if team_spaceship_in_home_planet is True:
            # Travels to team spaceship
            travel_to_spaceship(team_spaceship_marker_number, team_spaceship_in_home_planet)
            # Deposits asteroid into spaceship
            deposit_asteroid_into_spaceship()
            # Records the subsequent points
            points = update_points(closest_asteroid_marker_number, points, 40)
        elif team_spaceship_in_home_planet is False:
            # Faces home planet
            closest_arena_boundary_marker_number = face_home_planet()
            # Deposits asteroid in home planet
            deposit_object_into_planet()
            # Records the subsequent points
            points = update_points(closest_asteroid_marker_number, points, 12)
            # Faces team spaceship to retrieve it
            team_spaceship_marker_number, team_spaceship_in_home_planet, team_spaceship_has_been_stolen = face_team_spaceship(team_spaceship_marker_number, team_spaceship_in_home_planet, closest_arena_boundary_marker_number, team_spaceship_has_been_stolen)
            # Travels to team spaceship
            travel_to_spaceship(team_spaceship_marker_number, team_spaceship_in_home_planet)
            # Clamps onto team spaceship
            clamp_onto_team_spaceship() # WIP
            # Faces home planet
            closest_arena_boundary_marker_number = face_home_planet()
            # Travels to home planet
            travel_to_planet(closest_arena_boundary_marker_number)

# 2. Collects asteroids one after another and places them in the home planet:
while duration_of_match < 125:
    # Identifies closest asteroid and travels to it
    closest_asteroid_marker_number, points = face_closest_asteroid(points)
    asteroid_has_been_stolen = travel_to_closest_asteroid(closest_asteroid_marker_number, asteroid_has_been_stolen)
    if asteroid_has_been_stolen is False:
        # Collects asteroid
        close_clamps()
        robot.sleep(0.3)
        # Faces home planet
        closest_arena_boundary_marker_number = face_home_planet()
        # Travels to home planet
        travel_to_planet(closest_arena_boundary_marker_number)
        # Deposits asteroid in home planet and records the subsequent points
        deposit_object_into_planet()
        points = update_points(closest_asteroid_marker_number, points, 12)
    # Records the duration of the match at that point
    duration_of_match = record_time(start_of_match)
    print(f'Duration of match: {duration_of_match}')

# 3. Finds egg and deposits it into another team's planet
# Faces egg and travels to it
face_egg()
travel_to_egg()
x = face_enemy_planet()
travel_to_enemy_planet(x)
open_clamps()
# Records the duration of the match at that point
duration_of_match = record_time(start_of_match)
print(f'Duration of match: {duration_of_match}')
