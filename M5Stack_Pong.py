from m5stack import *
from m5ui import *
from uiflow import *
import random
import time

# Initialize screen
lcd.setRotation(3)
lcd.fill(0x000000)  # Black color

# Variables
paddle_left_y = 20
paddle_right_y = 20
ball_x = 160
ball_y = 120
ball_speed_x = 3
ball_speed_y = 2
paddle_width = 10
paddle_height = 60
ball_radius = 5  # Smaller radius for the ball

# Score variables
score_left = 0
score_right = 0

# Track previous positions
prev_paddle_left_y = paddle_left_y
prev_paddle_right_y = paddle_right_y
prev_ball_x = ball_x
prev_ball_y = ball_y

# Function to draw paddles and ball
def draw_objects():
    lcd.fillRect(0, paddle_left_y, paddle_width, paddle_height, 0xFFFFFF)  # Solid white for left paddle
    lcd.fillRect(320 - paddle_width, paddle_right_y, paddle_width, paddle_height, 0xFFFFFF)  # Solid white for right paddle
    lcd.fillCircle(int(ball_x), int(ball_y), int(ball_radius), 0xFF0000)  # Red color for ball

# Function to clear previous drawings
def clear_previous():
    lcd.fillRect(0, prev_paddle_left_y, paddle_width, paddle_height, 0x000000)  # Clear previous left paddle position
    lcd.fillRect(320 - paddle_width, prev_paddle_right_y, paddle_width, paddle_height, 0x000000)  # Clear previous right paddle position
    lcd.fillCircle(int(prev_ball_x), int(prev_ball_y), int(ball_radius), 0x000000)  # Clear previous ball position

# Function to draw the scoreboard
def draw_scoreboard():
  lcd.fillRect(0, 0, 30, 10, 0x000000)
  lcd.fillRect(300, 0, 30, 10, 0x000000)
  lcd.print(score_left, 0,0, 0xffffff)
  lcd.print(score_right, 300,0, 0xffffff)
    #lcd.fillRect(0, 0, 320, 20, 0x000000)  # Clear top bar
    #lcd.setTextColor(0xFFFFFF)  # Set text color to white
    #lcd.setTextSize(2)  # Set text size
    # Calculate x-coordinate for centering text
    #text_width = len(f"{score_left} - {score_right}") * 12  # Approximate width based on text size
    #x_position = (320 - text_width) // 2
    #lcd.print(([score_left] + [score_right]), 160, 5, 0xFFFFFF)  # Print the score at the calculated position

# Function to adjust ball direction upon collision
def adjust_ball_trajectory(paddle_y):
    global ball_speed_x, ball_speed_y
    # Compute the relative position where the ball hits the paddle
    hit_position = (ball_y + ball_radius) - (paddle_y + paddle_height / 2)
    # Adjust the angle based on the hit position
    angle_adjustment = hit_position / (paddle_height / 2)
    ball_speed_x = -ball_speed_x  # Reverse horizontal direction
    ball_speed_y += angle_adjustment * 2  # Adjust vertical direction

# Function to reset the game
def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score_left, score_right
    ball_x = 160
    ball_y = 120
    ball_speed_x = 3 * (1 if random.choice([True, False]) else -1)  # Randomly start left or right
    ball_speed_y = 2 * (1 if random.choice([True, False]) else -1)  # Randomly start up or down
    #score_left = 0
    #score_right = 0

# Draw initial objects
draw_scoreboard()

# Main game loop
last_update_time = time.ticks_ms()
frame_rate = 60  # Target frame rate in Hz
frame_duration = 1000 // frame_rate  # Duration of one frame in milliseconds

while True:
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_update_time) >= frame_duration:
        # Clear previous positions
        clear_previous()
        
        # Update paddles
        if btnA.isPressed() and paddle_left_y > 0:
            paddle_left_y -= 5
        if btnB.isPressed() and paddle_left_y < 240 - paddle_height:
            paddle_left_y += 5
        
        # Controlled movement for right paddle
        if paddle_right_y + paddle_height / 2 < ball_y + ball_radius:
            if paddle_right_y < 240 - paddle_height:
                paddle_right_y += 2  # Move down
        elif paddle_right_y + paddle_height / 2 > ball_y + ball_radius:
            if paddle_right_y > 0:
                paddle_right_y -= 2  # Move up
        
        # Update ball position
        prev_ball_x = ball_x
        prev_ball_y = ball_y
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        
        # Ball collision with top/bottom walls
        if ball_y <= ball_radius or ball_y >= 240 - ball_radius:
            ball_speed_y = -ball_speed_y
        
        # Ball collision with paddles
        if (ball_x <= paddle_width + ball_radius and paddle_left_y < ball_y + ball_radius and paddle_left_y + paddle_height > ball_y - ball_radius):
            adjust_ball_trajectory(paddle_left_y)
        elif (ball_x >= 320 - paddle_width - ball_radius and paddle_right_y < ball_y + ball_radius and paddle_right_y + paddle_height > ball_y - ball_radius):
            adjust_ball_trajectory(paddle_right_y)
        
        # Ball out of bounds
        if ball_x <= 0:
            score_right += 1  # Right player scores
            reset_game()
        elif ball_x >= 320:
            score_left += 1  # Left player scores
            reset_game()
        
        # Draw updated objects
        draw_objects()
        draw_scoreboard()  # Draw the scoreboard
        
        # Update previous positions
        prev_paddle_left_y = paddle_left_y
        prev_paddle_right_y = paddle_right_y
        prev_ball_x = ball_x
        prev_ball_y = ball_y
        last_update_time = current_time
    
    # Reset score with button C
    if btnC.isPressed():
        reset_game()
        score_left = 0
        score_right = 0
        draw_scoreboard()  # Redraw the scoreboard after reset
    
    # Small delay to avoid too tight loop
    wait_ms(10)
