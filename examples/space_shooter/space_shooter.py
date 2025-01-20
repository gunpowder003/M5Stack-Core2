from m5stack import * 
from m5ui import *
from uiflow import *
import random
import time

# Screen settings
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
player_width = 40
player_height = 10
bullet_width = 5
bullet_height = 10
asteroid_width = 20
asteroid_height = 20
bullet_speed = 5
asteroid_speed = 0 # need to be int, if speed = 0, it became random
max_speed = 5 #int: max speed of asteroid when random speed is chosen
score = 0
game_over = False

# Initialize player (spaceship) properties
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10

# Bullet list
bullets = []

# Asteroid list
asteroids = []

# Initialize display
setScreenColor(0x000000)

# Draw player spaceship
def draw_player():
    lcd.fillRect(player_x, player_y, player_width, player_height, 0x00FF00)

# Draw bullets
def draw_bullets():
    for bullet in bullets[:]:
        lcd.fillRect(bullet[0], bullet[1], bullet_width, bullet_height, 0xFFFFFF)

# Draw asteroids
def draw_asteroids():
    for asteroid in asteroids[:]:
        lcd.fillRect(asteroid[0], asteroid[1], asteroid_width, asteroid_height, 0xFF0000)

# Clear player
def clear_player():
    lcd.fillRect(player_x, player_y, player_width, player_height, 0x000000)

# Clear bullets
def clear_bullets():
    for bullet in bullets[:]:
        lcd.fillRect(bullet[0], bullet[1], bullet_width, bullet_height, 0x000000)

# Clear asteroids
def clear_asteroids():
    for asteroid in asteroids[:]:
        lcd.fillRect(asteroid[0], asteroid[1], asteroid_width, asteroid_height, 0x000000)

# Clear score area
def clear_score():
    lcd.fillRect(10, 10, 100, 20, 0x000000)  # Clear a specific area for the score

# Move player left and right
def move_player():
    global player_x
    if btnA.isPressed() and player_x > 0:
        player_x -= 5
    if btnC.isPressed() and player_x < SCREEN_WIDTH - player_width:
        player_x += 5

# Shoot bullets automatically
def shoot_bullet():
    global bullets
    bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])

# Move bullets
def move_bullets():
    global bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

# Generate asteroids
def generate_asteroid():
    x_position = random.randint(0, SCREEN_WIDTH - asteroid_width)
    asteroid_speed = random.randint(1,max_speed)
    asteroids.append([x_position, 0, asteroid_speed])

# Move asteroids
def move_asteroids():
    global score
    for asteroid in asteroids[:]:
        if asteroid_speed != 0:
          asteroid[1] += asteroid_speed
          if asteroid[1] > SCREEN_HEIGHT:
              asteroids.remove(asteroid)
              score += 1
        elif asteroid_speed == 0:
          asteroid[1] += asteroid[2]
          if asteroid[1] > SCREEN_HEIGHT:
              asteroids.remove(asteroid)
              score += 1

# Check for collisions between bullets and asteroids
def check_collisions():
    global asteroids, bullets, score
    to_remove_bullets = []
    to_remove_asteroids = []
    
    for asteroid in asteroids[:]:
        for bullet in bullets[:]:
            if (bullet[0] < asteroid[0] + asteroid_width and bullet[0] + bullet_width > asteroid[0] and 
               bullet[1] < asteroid[1] + asteroid_height and bullet[1] + bullet_height > asteroid[1]):
                to_remove_asteroids.append(asteroid)
                to_remove_bullets.append(bullet)
                score += 5  # Increase score when an asteroid is destroyed

    # Remove the marked bullets and asteroids after the collision check
    for bullet in to_remove_bullets:
        bullets.remove(bullet)
    for asteroid in to_remove_asteroids:
        asteroids.remove(asteroid)

# Check if asteroid hits the player
def check_game_over():
    global game_over
    for asteroid in asteroids[:]:
        if (asteroid[0] < player_x + player_width and asteroid[0] + asteroid_width > player_x and
            asteroid[1] < player_y + player_height and asteroid[1] + asteroid_height > player_y):
            game_over = True
            

# Display score
def display_score():
    clear_score()  # Ensure the score area is clear before drawing
    lcd.text(10, 10, "Score: {}".format(score), 0xFFFFFF)

  
# Main game loop
shoot_timer = 0
while True:
    if game_over:
        lcd.clear()
        lcd.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, "GAME OVER", 0xFF0000)
        lcd.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 20, "Score: {}".format(score), 0xFFFFFF)
        lcd.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 40, "Press B to restart", 0xFFFFFF)
        #break
        while True:
          if btnB.isPressed():
            lcd.clear()
            shoot_timer = 0
            game_over = False
            score = 0
            bullets.clear()
            asteroids.clear()
            player_x = SCREEN_WIDTH // 2 - player_width // 2
            player_y = SCREEN_HEIGHT - player_height - 10
            break
        continue  

    # Clear previous frame
    clear_player()
    clear_bullets()
    clear_asteroids()

    # Move player, move bullets, and move asteroids
    move_player()
    move_bullets()
    move_asteroids()
    check_collisions()
    check_game_over()

    # Automatically shoot bullets at regular intervals
    shoot_timer += 1
    if shoot_timer >= 10:  # Adjust interval to control shooting frequency
        shoot_bullet()
        shoot_timer = 0

    # Generate new asteroids randomly
    if random.randint(1, 50) == 1:
        generate_asteroid()

    # Draw current frame
    draw_player()
    draw_bullets()
    draw_asteroids()
    display_score()

    # Wait a bit before the next frame
    time.sleep(0.03)
