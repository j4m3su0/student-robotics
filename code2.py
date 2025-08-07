(No subject)

James Onyegbosi
​
Nathanael Bekele​
# Allows us to interact with the robot's hardware (motors, servos, camera):
from sr.robot3 import *
import time
robot = Robot()

#===========================================================================

# Subroutines for performing basic actions:

def move_forward(): # Moves robot forward
  left_motor.power = 0.5
  right_motor.power = 0.5
  return move_forward

def move_backward(): # Moves robot backwards
  left_motor.power = -0.5
  right_motor.power = -0.5
  return move_backward

def rotate_left(): # Makes robot rotate to the left
  left_motor.power = -0.1
  right_motor.power = 0.1
  return rotate_left

def rotate_right(): # Makes robot rotate to the right
  left_motor.power = 0.1
  right_motor.power = -0.1
  return rotate_right

def stop_robot(): # Stops robot
  left_motor.power = 0
  right_motor.power = 0
  return stop_robot

def close_clamps(): # Closes clamps
  left_clamp.position = 1
  right_clamp.position = 1
  return close_clamps

def open_clamps(): # Opens clamps
  left_clamp.position = -1
  right_clamp.position = -1
  return open_clamps

def raise_clamps(): # Raises clamps
  lift.position = 1
  return raise_clamps

def lower_clamps(): # Lowers clamps (to rest position)
  lift.position = -1
  return lower_clamps

def identify_zone(): # Done
  zone_number = robot.zone
  if zone_number == 0:
    arena_boundary_marker_numbers = [0,1,2,3,4,5,6]
  elif zone_number == 1:
    arena_boundary_marker_numbers = [7,8,9,10,11,12,13]
  elif zone_number == 2:
    arena_boundary_marker_numbers = [14,15,16,17,18,19,20]
  else:
    arena_boundary_marker_numbers = [21,22,23,24,25,26,27]
  print(f"Zone number: {zone_number}")
  print(f"Arena boundary marker numbers: {arena_boundary_marker_numbers}")
  return arena_boundary_marker_numbers

def deposit_asteroid_into_spaceship(): # Done
  raise_clamps()
  robot.sleep(3)
  move_forward()
  robot.sleep(0.3)
  stop_robot()
  robot.sleep(0.1)
  open_clamps()
  robot.sleep(0.5)
  move_backward()
  robot.sleep(2.5)
  stop_robot()
  return deposit_asteroid_into_spaceship

def capture_spaceship(): # Done
  raise_clamps()
  robot.sleep(3)
  move_forward()
  robot.sleep(0.3)
  stop_robot()
  robot.sleep(0.1)
  open_clamps()
  robot.sleep(0.5)
  lift.position = 0.1
  robot.sleep(3)
  move_backward()
  robot.sleep(1)
  stop_robot()
  return capture_spaceship

def update_points(points, list): # Done
  if list == asteroids_in_spaceship_marker_numbers:
    asteroids_in_spaceship_marker_numbers.append(closest_asteroid_marker_number)
    points += 40
  elif list == asteroids_in_home_planet_marker_numbers:
    asteroids_in_home_planet_marker_numbers.append(closest_asteroid_marker_number)
    points += 12
  elif list is None:
    points += 8
  print(f"Asteroid in spaceship marker numbers: \
  {asteroids_in_spaceship_marker_numbers}")
  print(f"Asteroid in home planet marker numbers: \
  {asteroids_in_home_planet_marker_numbers}")
  print(f"Current points: {points}")
  return points

def record_time(emd_time): # Done
  end_time = time.time()
  timer = (end_time - start_time)
  print(f"Timer: {timer}")
  return timer

# Subroutines for asteroids:

def face_closest_asteroid(points): # Done
  # Turns until at least one asteroid is in view:
  print("Robot is turning left")
  rotate_left()
  marker_in_view = False
  while True:
    while marker_in_view is False:
      robot.sleep(0.1)
      view = robot.camera.see()
      if len(view) > 0:
        for marker in view:
          if (marker.id in asteroid_marker_numbers
          and marker.id not in asteroids_in_spaceship_marker_numbers
          and marker.id not in asteroids_in_home_planet_marker_numbers):
            marker_in_view = True
    break
  if first_asteroid_collected == True:
    robot.sleep(0.7)
  stop_robot()
  print("An asteroid is in view")
  # Finds the asteroid in view with the closest distance:
  angle = None
  distance = None
  marker_number = None
  distances = []
  while True:
    robot.sleep(0.1)
    view = robot.camera.see()
    for marker in view:
      if (marker.id in asteroid_marker_numbers
      and marker.id not in asteroids_in_spaceship_marker_numbers
      and marker.id not in asteroids_in_home_planet_marker_numbers):
        distance = marker.position.distance
        distances.append(distance)
      if marker.id in asteroids_in_spaceship_marker_numbers: # Removes accidental...
        # ...asteroid marker numbers from list and subsequent points
        asteroids_in_spaceship_marker_numbers.remove(marker.id)
        points -= (40 + 8)
      if marker.id in asteroids_in_home_planet_marker_numbers: # Removes accidental...
        # ...asteroid marker numbers from list and subsequent points
        asteroids_in_home_planet_marker_numbers.remove(marker.id)
        points -= (12 + 8)
    distances.sort()
    closest_distance = distances[0]
    for marker in view:
      if (marker.position.distance == closest_distance
      and marker.id in asteroid_marker_numbers
      and marker.id not in asteroids_in_spaceship_marker_numbers):
        angle = marker.position.horizontal_angle
        marker_number = marker.id
    break
  # Turns to face closest asteroid:
  facing_object = False
  if angle > 0.1: # Asteroid is on the right
    print("Robot is turning right")
    rotate_right()
    while True:
      while facing_object is False:
        while angle > 0.1:
          robot.sleep(0.1)
          view = robot.camera.see()
          for marker in view:
            if marker.id == marker_number:
              angle = marker.position.horizontal_angle
        stop_robot()
        facing_object = True
      break
  elif angle < -0.1: # Asteroid is on the left
    print("Robot is turning left")
    rotate_left()
    while True:
      while facing_object is False:
        while angle < -0.1:
          robot.sleep(0.1)
          view = robot.camera.see()
          for marker in view:
            if marker.id == marker_number:
              angle = marker.position.horizontal_angle
        stop_robot()
        facing_object = True
      break
  print("Robot is facing closest asteroid")
  print(f"Closest asteroid marker number: {marker_number}")
  print(f"Closest asteroid angle: {angle}")
  print(f"Closest asteroid distance: {closest_distance}")
  return marker_number, points

def travel_to_closest_asteroid(marker_number): # Done
  move_forward()
  angle = None
  at_marker = False
  while True:
    while at_marker is False:
      marker_numbers = []
      robot.sleep(0.1)
      view = robot.camera.see()
      # Corrects orientation to face asteroid while moving:
      for marker in view:
        if marker.id == marker_number:
          angle = marker.position.horizontal_angle
          facing_object = False
          if angle > 0.1: # Asteroid is on the right
            rotate_right()
            while True:
              while facing_object is False:
                while angle > 0.1:
                  robot.sleep(0.1)
                  view = robot.camera.see()
                  for marker in view:
                    if marker.id == marker_number:
                      angle = marker.position.horizontal_angle
                facing_object = True
              break
          elif angle < -0.1: # Asteroid is on the left
            rotate_left()
            while True:
              while facing_object is False:
                while angle < -0.1:
                  robot.sleep(0.1)
                  view = robot.camera.see()
                  for marker in view:
                    if marker.id == marker_number:
                      angle = marker.position.horizontal_angle
                facing_object = True
              break
          move_forward()
      # Appends to a list of asteroid marker numbers...
      # ...to know when the asteroid is not in view:
      for marker in view:
        if (marker.id in asteroid_marker_numbers
        and marker.id not in asteroids_in_spaceship_marker_numbers
        and marker.id not in asteroids_in_home_planet_marker_numbers):
          marker_numbers.append(marker.id)
      if marker_number not in marker_numbers:
        stop_robot()
        at_marker = True
    break
  print ("Robot is at closest asteroid")
  return travel_to_closest_asteroid

# Subroutines for home planet:

def face_home_planet(): # Done
  # Turns until the arena boundary marker numbers...
  # ...for the home planet is in view:
  print("Robot is turning right")
  rotate_right()
  angle = None
  distance = None
  closest_distance = None
  marker_number = None
  distances = []
  marker_in_view = False
  while True:
    while marker_in_view is False:
      robot.sleep(0.1)
      view = robot.camera.see()
      for marker in view:
        # Robot is going to deposit asteroid in spaceship
        if ((home_planet_spaceship_location == "in home planet"
            and marker.id in arena_boundary_marker_numbers[2:5])
        # Robot is going to return home planet spaceship to home planet
        or (home_planet_spaceship_location == "not in home planet"
            and marker.id == arena_boundary_marker_numbers[1])):
          angle = marker.position.horizontal_angle
          marker_in_view = True
    break
  stop_robot()
  print("Home planet is in view")
  # Turns to face closest arena boundary marker:
  facing_object = False
  if angle > 0.1: # Arena boundary marker is on the right
    print("Robot is turning right")
    rotate_right()
    while True:
      while facing_object is False:
        while angle > 0.1:
          robot.sleep(0.1)
          view = robot.camera.see()
          for marker in view:
            if marker.id in arena_boundary_marker_numbers[2:5]:
              distance = marker.position.distance
              distances.append(distance)
          distances.sort()
          closest_distance = distances[0]
          for marker in view:
            if (marker.position.distance == closest_distance
            and marker.id in arena_boundary_marker_numbers[2:5]):
              angle = marker.position.horizontal_angle
              marker_number = marker.id
        stop_robot()
        facing_object = True
      break
  elif angle < -0.1: # Arena boundary marker is on the left
    print("Robot is turning left")
    rotate_left()
    while True:
      while facing_object is False:
        while angle < -0.1:
          robot.sleep(0.1)
          view = robot.camera.see()
          for marker in view:
            if marker.id in arena_boundary_marker_numbers[2:5]:
              distance = marker.position.distance
              distances.append(distance)
          distances.sort()
          closest_distance = distances[0]
          for marker in view:
            if (marker.position.distance == closest_distance
            and marker.id in arena_boundary_marker_numbers[2:5]):
              angle = marker.position.horizontal_angle
              marker_number = marker.id
        stop_robot()
        facing_object = True
      break
  print(f"Distance from home planet: {closest_distance}")
  return closest_distance, marker_number

def travel_to_home_planet(distance, marker_number): # Done
  move_forward()
  at_marker = False
  while True:
    while at_marker is False:
      while distance > 600:
        robot.sleep(0.1)
        view = robot.camera.see()
        # Corrects orientation to face arena boundary marker while moving:
        for marker in view:
          if marker.id == marker_number:
            angle = marker.position.horizontal_angle
            facing_object = False
            if angle > 0.1: # Arena boundary marker is on the right
              rotate_right()
              while True:
                while facing_object is False:
                  while angle > 0.1:
                    robot.sleep(0.1)
                    view = robot.camera.see()
                    for marker in view:
                      if marker.id == marker_number:
                        angle = marker.position.horizontal_angle
                  stop_robot()
                  facing_object = True
                break
            elif angle < -0.1: # Arena boundary marker is on the left
              rotate_left()
              while True:
                while facing_object is False:
                  while angle < -0.1:
                    robot.sleep(0.1)
                    view = robot.camera.see()
                    for marker in view:
                      if marker.id == marker_number:
                        angle = marker.position.horizontal_angle
                  stop_robot()
                  facing_object = True
                break
            move_forward()
        # Finds the distance from closest arena boundary marker:
        for marker in view:
          if marker.id == marker_number:
            distance = marker.position.distance
      at_marker = True
    break
  stop_robot()
  print("Robot is at spaceship")
  return travel_to_home_planet

# Subroutines for spaceships:

def face_home_planet_spaceship(home_planet_spaceship_location): # Done
  # Turns until the spaceship is in view:
  print("Robot is turning left")
  rotate_left()
  angle = None
  distance = None
  marker_number = None
  marker_in_view = False
  while True:
    while marker_in_view is False:
      robot.sleep(0.1)
      view = robot.camera.see()
      for marker in view:
        range = marker.position.distance
        if (marker.id in spaceship_marker_numbers
        and range < 3000):
          home_planet_spaceship_location = "in home planet"
          print("Home planet spaceship is in home planet")
          angle = marker.position.horizontal_angle
          marker_number = marker.id
          stop_robot()
          marker_in_view = True
        elif (marker.id == home_planet_spaceship_marker_number
        and range > 3000):
          home_planet_spaceship_location = "not in home planet"
          print("Home planet spaceship is not in home planet")
          angle = marker.position.horizontal_angle
          marker_number = marker.id
          stop_robot()
          marker_in_view = True
    break
  stop_robot()
  print("Spaceship is in view")
  # Turns to face spaceship:
  facing_object = False
  if angle < -0.1:
    print("Robot is turning left")
    rotate_left()
    while True:
      while facing_object is False:
        while angle < -0.1:
          robot.sleep(0.1)
          view = robot.camera.see()
          for marker in view:
            if marker.id == marker_number:
              angle = marker.position.horizontal_angle
              distance = marker.position.distance
        stop_robot()
        facing_object = True
      break
  elif angle > 0.1:
    print("Robot is turning right")
    rotate_left()
    while True:
      while facing_object is False:
        while angle < -0.1:
          robot.sleep(0.1)
          view = robot.camera.see()
          for marker in view:
            if marker.id == marker_number:
              angle = marker.position.horizontal_angle
              distance = marker.position.distance
        stop_robot()
        facing_object = True
      break
  print("Robot is facing spaceship")
  print(f"Distance from spaceship in home planet: {distance}")
  return distance, marker_number, home_planet_spaceship_location

def travel_to_spaceship(distance, marker_number): # Done
  move_forward()
  at_marker = False
  while True:
    while at_marker is False:
      while distance > 500:
        robot.sleep(0.1)
        view = robot.camera.see()
        # Corrects orientation to face spaceship:
        for marker in view:
          if marker.id == marker_number:
            angle = marker.position.horizontal_angle
            facing_object = False
            if angle > 0.1: # Spaceship is on the right
              rotate_right()
              while True:
                while facing_object is False:
                  while angle > 0.1:
                    robot.sleep(0.1)
                    view = robot.camera.see()
                    for marker in view:
                      if marker.id == marker_number:
                        angle = marker.position.horizontal_angle
                  stop_robot()
                  facing_object = True
                break
            elif angle < -0.1: # Spaceship is on the left
              rotate_left()
              while True:
                while facing_object is False:
                  while angle < -0.1:
                    robot.sleep(0.1)
                    view = robot.camera.see()
                    for marker in view:
                      if marker.id == marker_number:
                        angle = marker.position.horizontal_angle
                  stop_robot()
                  facing_object = True
                break
            move_forward()
        # Finds the distance from home planet spaceship:
        for marker in view:
          if marker.id == marker_number:
            distance = marker.position.distance
      at_marker = True
    break
  stop_robot()
  print("Robot is at spaceship")
  return travel_to_spaceship

# Subrotuines for egg:

def face_egg(): # Done
  # Turns until the egg is in view:
  print("Robot is turning left")
  rotate_left()
  angle = None
  distance = None
  marker_number = None
  marker_in_view = False
  while True:
    while marker_in_view is False:
      robot.sleep(0.1)
      view = robot.camera.see()
      if len(view) > 0:
        for marker in view:
          if marker.id == 110:
            angle = marker.position.horizontal_angle
            marker_number = marker.id
            stop_robot()
            marker_in_view = True
    break
  stop_robot()
  print("Egg is in view")
  # Turns to face egg:
  facing_object = False
  if angle < -0.1:
    print("Robot is turning left")
    rotate_left()
    while True:
      while facing_object is False:
        while angle < -0.1:
          robot.sleep(0.1)
          view = robot.camera.see()
          for marker in view:
            if marker.id == marker_number:
              angle = marker.position.horizontal_angle
              distance = marker.position.distance
        stop_robot()
        facing_object = True
      break
  elif angle > 0.1:
    print("Robot is turning right")
    rotate_left()
    while True:
      while facing_object is False:
        while angle < -0.1:
          robot.sleep(0.1)
          view = robot.camera.see()
          for marker in view:
            if marker.id == marker_number:
              angle = marker.position.horizontal_angle
              distance = marker.position.distance
        stop_robot()
        facing_object = True
      break
  print("Robot is facing egg")
  print(f"Distance from egg in home planet: {distance}")
  return face_egg

def travel_to_egg(): # Done
  move_forward()
  angle = None
  marker_number = None
  at_marker = False
  while True:
    while at_marker is False:
      egg = []
      robot.sleep(0.1)
      view = robot.camera.see()
      # Corrects orientation to face egg while moving:
      for marker in view:
        if marker.id == 110:
          angle = marker.position.horizontal_angle
          facing_object = False
          if angle > 0.1: # Egg is on the right
            rotate_right()
            while True:
              while facing_object is False:
                while angle > 0.1:
                  robot.sleep(0.1)
                  view = robot.camera.see()
                  for marker in view:
                    if marker.id == 110:
                      angle = marker.position.horizontal_angle
                facing_object = True
              break
          elif angle < -0.1: # Egg is on the left
            rotate_left()
            while True:
              while facing_object is False:
                while angle < -0.1:
                  robot.sleep(0.1)
                  view = robot.camera.see()
                  for marker in view:
                    if marker.id == 110:
                      angle = marker.position.horizontal_angle
                facing_object = True
              break
          move_forward()
      # Appends to a list of asteroid marker numbers...
      # ...to know when the asteroid is not in view:
      for marker in view:
        if marker.id == 110:
          marker_number = marker.id
          egg.append(marker.id)
      if marker_number not in egg:
        stop_robot()
        at_marker = True
    break
  print ("Robot is at egg")
  return travel_to_egg

#===========================================================================

# Assigns motor (wheels) and servos (clamps) to variables
left_motor = robot.motor_boards['srABC1'].motors[0]
right_motor = robot.motor_boards['srABC1'].motors[1]
left_clamp = robot.servo_board.servos[0]
right_clamp = robot.servo_board.servos[1]
lift = robot.servo_board.servos[2]

#===========================================================================

# Initialise points
points = 0

# Identifies arena boundary depending on zone number
arena_boundary_marker_numbers = identify_zone()

# Assigns all possible spaceship marker numbers into a list
spaceship_marker_numbers = [120,121,122,123,125,126,127,128]
# Initialises spaceship location
home_planet_spaceship_location = "in home planet"
# Initialise home planet spaceship marker number
home_planet_spaceship_marker_number = None

# Creates a list to store all possible asteroid marker numbers...
asteroid_marker_numbers = list(range(150,200))
# Creates a list for asteroids in spaceship
asteroids_in_spaceship_marker_numbers = []
asteroids_in_home_planet_marker_numbers = []

# Starts a timer that record how long the robot takes
start_time = time.time()
end_time = None
timer = 0
x = 125

#===========================================================================

# 1. Collects two asteroids one after another...
#    ...and deposits them into the spaceship in its home planet
first_asteroid_collected = False
for i in range(0,2):
  if timer < x:
    # A. Identifies closest asteroid and travels to it
    robot.sleep(0.5)
    closest_asteroid_marker_number, points = face_closest_asteroid(points)
    travel_to_closest_asteroid(closest_asteroid_marker_number)
    # B. Collects asteroid
    robot.sleep(0.5)
    close_clamps()
    points = update_points(points, None)
    # C. Faces home planet and travels to it
    robot.sleep(0.5)
    distance_from_closest_arena_boundary_marker, \
    closest_arena_boundary_marker_number = face_home_planet()
    robot.sleep(0.5)
    travel_to_home_planet(distance_from_closest_arena_boundary_marker,
                          closest_arena_boundary_marker_number)
    # D. Faces home planet spaceship and travels to it
    robot.sleep(0.5)
    distance_from_home_planet_spaceship, \
    home_planet_spaceship_marker_number, \
    home_planet_spaceship_location \
    = face_home_planet_spaceship(home_planet_spaceship_location)
    robot.sleep(0.5)
    travel_to_spaceship(distance_from_home_planet_spaceship,
                        home_planet_spaceship_marker_number)
    # E. Deposits asteroid into spaceship and stores its marker number
    robot.sleep(0.5)
    deposit_asteroid_into_spaceship()
    points = update_points(points, asteroids_in_spaceship_marker_numbers)
    # F. Resets clamp position
    robot.sleep(0.5)
    lower_clamps()
    robot.sleep(3)
    # G. Records the time taken since the start of the program
    end_time = time.time()
    timer = record_time(end_time)
    # H. Records if this the first asteroid has been taken
    if i == 0:
      first_asteroid_collected = True


# 2. Collects three asteroids one after another...
#    ...and places them in the home planet
for i in range(0,3):
  if timer < x:
    # A. Identifies closest asteroid and travels to it
    robot.sleep(0.5)
    closest_asteroid_marker_number, points = face_closest_asteroid(points)
    travel_to_closest_asteroid(closest_asteroid_marker_number)
    # B. Collects asteroid
    robot.sleep(0.5)
    close_clamps()
    points = update_points(points, None)
    # C. Faces home planet and travels to it
    robot.sleep(0.5)
    distance_from_closest_arena_boundary_marker, \
    closest_arena_boundary_marker_number = face_home_planet()
    robot.sleep(0.5)
    travel_to_home_planet(distance_from_closest_arena_boundary_marker,
                          closest_arena_boundary_marker_number)
    # D. Puts asteroid in home planet
    robot.sleep(0.5)
    open_clamps()
    move_backward()
    robot.sleep(1)
    stop_robot()
    points = update_points(points, asteroids_in_home_planet_marker_numbers)
    # E. Records the time taken since the start of the program
    end_time = time.time()
    timer = record_time(end_time)

# 3. Checks for home planet spaceship location...
#    ...and reclaims it if it has been stolen
if timer < x:
  # A. Faces home planet spaceship
  robot.sleep(0.5)
  distance_from_home_planet_spaceship, \
  home_planet_spaceship_marker_number, \
  home_planet_spaceship_location \
  = face_home_planet_spaceship(home_planet_spaceship_location)
  if home_planet_spaceship_location == "not in home planet":
    # B. Capture spaceship
    capture_spaceship()
    # C. Travels to spaceship
    robot.sleep(0.5)
    travel_to_home_planet(distance_from_closest_arena_boundary_marker,
                          closest_arena_boundary_marker_number) # This is not unbound
    home_planet_spaceship_location = "in home planet"
  # D. Records the time taken since the start of the program
  end_time = time.time()
  timer = record_time(end_time)
