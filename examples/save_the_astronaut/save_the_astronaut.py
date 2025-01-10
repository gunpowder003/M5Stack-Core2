from m5stack import *
from m5ui import *
from uiflow import *
import imu
import random
import time

# Initialize screen and IMU
setScreenColor(0x000000)
imu0 = imu.IMU()

# Constants
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
ASTRONAUT_SIZE = 7
GRAVITY_WELL_RADIUS = 10
GRAVITY_COVERAGE = 2 #multiplication of well radius
GRAVITY_STRENGTH = 2 #must be int. how strong gravity is acting on the astronaut once it is in coverage
LASER_WIDTH = 5
GOAL_SIZE = 15
FRICTION = 0.98  # Slow down astronaut gradually
MAX_SPEED = 5  # Prevent excessive drift
LASER_MAX_QTY = 5 #max qty laser per level
WELL_MAX_QTY = 5 #max qty laser per level
SCALING_FACTOR = 2.7 #adjust how responsive astronaut. too much will cause instability
# Game objects
astronaut_x = random.randint(0,320)
astronaut_y = random.randint(0,240)
velocity_x = 0
velocity_y = 0
prev_astronaut_x = astronaut_x
prev_astronaut_y = astronaut_y


goal_x = random.randint(20, SCREEN_WIDTH - 20)
goal_y = random.randint(20, SCREEN_HEIGHT - 20)
gravity_wells = [(random.randint(40, 280), random.randint(40, 200)) for _ in range(WELL_MAX_QTY)] #gravity well posx, posy
lasers = [(random.randint(50, 270), random.choice([50, 190]), random.randint(50, 150), random.choice(["H", "V"])) for _ in range(LASER_MAX_QTY)] # laser posx, posy, laser_length, horizontal or vertical line

def draw_static_elements():
    lcd.clear(0x000000)
    # Draw gravity wells
    for gx, gy in gravity_wells:
        lcd.circle(int(gx), int(gy), GRAVITY_WELL_RADIUS, 0x0000FF)
    # Draw lasers
    for lx, ly, laser_length, direction in lasers:
        if direction == "H": #if line is horizontal
            lcd.rect(int(lx), int(ly), laser_length, LASER_WIDTH, 0xFF0000, fillcolor=0xFF0000)
        else:
            lcd.rect(int(lx), int(ly), LASER_WIDTH, laser_length, 0xFF0000, fillcolor=0xFF0000)
    # Draw goal hatch
    lcd.rect(int(goal_x), int(goal_y), GOAL_SIZE, GOAL_SIZE, 0x00FF00, fillcolor=0x00FF00)

def erase_previous_astronaut():
    lcd.circle(int(prev_astronaut_x), int(prev_astronaut_y), ASTRONAUT_SIZE, 0x000000, fillcolor=0x000000)
    
    # Redraw static elements only if they were overlapped
    for gx, gy in gravity_wells:
        if ((prev_astronaut_x - gx) ** 2 + (prev_astronaut_y - gy) ** 2) ** 0.5 < GRAVITY_WELL_RADIUS:
            lcd.circle(int(gx), int(gy), GRAVITY_WELL_RADIUS, 0x0000FF)

def draw_astronaut():
    lcd.circle(int(astronaut_x), int(astronaut_y), ASTRONAUT_SIZE, 0xFFFFFF, fillcolor=0xFFFFFF)

def update_movement():
    global astronaut_x, astronaut_y, velocity_x, velocity_y, prev_astronaut_x, prev_astronaut_y
    prev_astronaut_x, prev_astronaut_y = astronaut_x, astronaut_y
    
    # Read IMU tilt
    tilt_x = -imu0.acceleration[0]  # Left-right
    tilt_y = imu0.acceleration[1]  # Up-down 
    
    # Adjust velocity based on tilt
    velocity_x += tilt_x * SCALING_FACTOR
    velocity_y += tilt_y * SCALING_FACTOR
    
    # Apply friction
    velocity_x *= FRICTION
    velocity_y *= FRICTION
    
    # Limit speed
    velocity_x = max(-MAX_SPEED, min(MAX_SPEED, velocity_x))
    velocity_y = max(-MAX_SPEED, min(MAX_SPEED, velocity_y))
    
    # Move astronaut
    astronaut_x += int(velocity_x)
    astronaut_y += int(velocity_y)
    
    # Keep astronaut within bounds
    astronaut_x = max(ASTRONAUT_SIZE, min(SCREEN_WIDTH - ASTRONAUT_SIZE, astronaut_x))
    astronaut_y = max(ASTRONAUT_SIZE, min(SCREEN_HEIGHT - ASTRONAUT_SIZE, astronaut_y))

def check_collisions():
    global astronaut_x, astronaut_y
    
    # Check if astronaut reached goal
    if goal_x < astronaut_x < goal_x + GOAL_SIZE and goal_y < astronaut_y < goal_y + GOAL_SIZE:
        lcd.print("YOU WIN!", 120, 100, 0x00FF00)
        time.sleep(2)
        reset_game()
    
    # Check if astronaut hits a laser
    for lx, ly, laser_length, direction in lasers:
        if direction == "H" and ly <= astronaut_y <= ly + LASER_WIDTH and lx <= astronaut_x <= lx + laser_length:
            lcd.print("GAME OVER!", 120, 100, 0xFF0000)
            time.sleep(2)
            reset_game()
        elif direction == "V" and lx <= astronaut_x <= lx + LASER_WIDTH and ly <= astronaut_y <= ly + laser_length:
            lcd.print("GAME OVER!", 120, 100, 0xFF0000)
            time.sleep(2)
            reset_game()
            
    # Check if astronaut hits a gravity well        
    for gx, gy in gravity_wells:
        if gx-ASTRONAUT_SIZE <= astronaut_x <= gx+ASTRONAUT_SIZE and gy-ASTRONAUT_SIZE <= astronaut_y <= gy+ASTRONAUT_SIZE:
            lcd.print("GAME OVER!", 120, 100, 0xFF0000)
            time.sleep(2)
            reset_game() 
            
def check_gravity_pull():
  global astronaut_x, astronaut_y
  
  for gx, gy in gravity_wells:
    if gx < astronaut_x < gx + GRAVITY_WELL_RADIUS*GRAVITY_COVERAGE and gy < astronaut_y < gy + GRAVITY_WELL_RADIUS*GRAVITY_COVERAGE:
      astronaut_x -= GRAVITY_STRENGTH
      astronaut_y -= GRAVITY_STRENGTH
    elif gx - GRAVITY_WELL_RADIUS*GRAVITY_COVERAGE < astronaut_x < gx and gy - GRAVITY_WELL_RADIUS*GRAVITY_COVERAGE < astronaut_y < gy:
      astronaut_x += GRAVITY_STRENGTH
      astronaut_y += GRAVITY_STRENGTH

def reset_game():
    global astronaut_x, astronaut_y, velocity_x, velocity_y, goal_x, goal_y, gravity_wells, lasers
    astronaut_x = random.randint(0,320)
    astronaut_y = random.randint(0,240)
    velocity_x = 0
    velocity_y = 0
    goal_x = random.randint(20, SCREEN_WIDTH - 20)
    goal_y = random.randint(20, SCREEN_HEIGHT - 20)
    gravity_wells = [(random.randint(40, 280), random.randint(40, 200)) for _ in range(WELL_MAX_QTY)]
    lasers = [(random.randint(50, 270), random.choice([50, 190]), random.randint(50, 150), random.choice(["H", "V"])) for _ in range(LASER_MAX_QTY)]
    draw_static_elements()

def game_loop():
    draw_static_elements()
    while True:
        erase_previous_astronaut()
        update_movement()
        check_collisions()
        check_gravity_pull()
        draw_astronaut()
        wait(0.025)  # 25ms refresh rate
        if btnA.isPressed(): #reset game
          reset_game()
        if btnB.isPressed():#pause game
          pause()
          
def pause():
  wait(0.2)
  while btnB.isPressed() == False:
    if btnA.isPressed():
      reset_game()
      break
    continue
  wait(0.2)

  
# Start game
game_loop()
