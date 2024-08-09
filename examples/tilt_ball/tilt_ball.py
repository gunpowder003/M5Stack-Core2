from m5stack import 
from m5ui import 
from uiflow import 
import imu
import time

# Initialize the accelerometer
acc = imu.IMU()

# Initialize display
lcd.setRotation(3)  # Adjust rotation as needed
lcd.fill(0)  # Clear the screen with black color

# Parameters
ball_radius = 15
update_interval = 0.0000001  # 10 ms for faster refresh rate
velocity_x = 0
velocity_y = 0
friction = 0.90  # Lower friction to reduce the rate of slowing down
scale_x = 4.0  # Increase scaling factor to make the ball more responsive to tilt
scale_y = 4.0  # Increase scaling factor to make the ball more responsive to tilt

# Fixed screen dimensions for M5Stack Core2
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

# Define colors
RED = 0xFF0000
BLACK = 0x000000
WHITE = 0xFFFFFF

def draw_ball(x, y)
    lcd.fill(BLACK)  # Clear screen
    lcd.fillCircle(int(x), int(y), ball_radius, RED)  # Draw red ball

def game_over()
    lcd.fill(BLACK)  # Clear screen
    lcd.text(SCREEN_WIDTH  2 - 50, SCREEN_HEIGHT  2 - 10, GAME OVER, WHITE)
    while True
        if btnA.isPressed()
            return  # Exit game over state when button A is pressed

def main()
    global velocity_x, velocity_y

    # Initial ball position at the center of the screen
    ball_x = SCREEN_WIDTH  2
    ball_y = SCREEN_HEIGHT  2

    while True
        if btnA.isPressed()
            break

        # Get accelerometer readings
        ax = acc.acceleration[0]  # X-axis acceleration
        ay = acc.acceleration[1]  # Y-axis acceleration

        # Print accelerometer readings for debugging
        print(AX {.2f}, AY {.2f}.format(ax, ay))

        # Adjust the velocity based on tilt
        velocity_x += -ax  scale_x  # Inverted for proper direction
        velocity_y += ay  scale_y  # Inverted for proper direction

        # Apply friction to simulate slowing down
        velocity_x = friction
        velocity_y = friction

        # Update ball position based on velocity
        ball_x += velocity_x
        ball_y += velocity_y

        # Debugging Print ball position and velocity for boundary checks
        print(Ball X {.2f}, Ball Y {.2f}.format(ball_x, ball_y))
        print(Velocity X {.2f}, Velocity Y {.2f}.format(velocity_x, velocity_y))

        # Keep coordinates within screen boundaries
        if ball_x  ball_radius or ball_x  SCREEN_WIDTH - ball_radius or 
           ball_y  ball_radius or ball_y  SCREEN_HEIGHT - ball_radius
            game_over()
            lcd.fill(0)  # Clear the screen after game over
            time.sleep(1)  # Wait for a second before restarting the game
            main()  # Restart the game

        draw_ball(ball_x, ball_y)

        time.sleep(update_interval)

# Start the game
main()

