from m5stack import *
from m5ui import *
from uiflow import *
import imu
import time
import random

# Initialize display and IMU
lcd.clear()
imu0 = imu.IMU()

# Screen size
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

# Player settings
PLAYER_SIZE = 20
SPEED_MULTIPLIER = 25  # Faster movement
player_y = SCREEN_HEIGHT - 30  # Fixed player position (bottom of screen)

# Block settings
BLOCK_WIDTH = 20
BLOCK_HEIGHT = 20
MAX_BLOCKS = 30  # Max difficulty level
BLOCK_SPEED_INCREASE = 0.7  # Blocks get faster over time

# Game loop
def start_game():
    global player_x, score, blocks
    
    # Reset player position
    player_x = SCREEN_WIDTH // 2

    # Reset score
    score = 0

    # Initialize blocks
    blocks = []
    for _ in range(3):  # Start with 3 blocks
        x_pos = random.randint(0, SCREEN_WIDTH - BLOCK_WIDTH)
        y_pos = random.randint(-100, -20)
        speed = random.uniform(2, 4)
        block = M5Rect(x_pos, y_pos, BLOCK_WIDTH, BLOCK_HEIGHT, color=0xff0000, fillcolor=0xff0000)
        blocks.append({"obj": block, "x": x_pos, "y": y_pos, "speed": speed})

    # Create player object
    player = M5Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE, color=0x00ff00, fillcolor=0x00ff00)

    while True:
        # Restart game if BtnA is pressed
        if btnA.isPressed():
            lcd.clear()
            start_game()
            return
        
        # Read accelerometer values (invert X for correct movement)
        ax = -imu0.acceleration[0]

        # Move player
        player_x += int(ax * SPEED_MULTIPLIER)
        player_x = max(0, min(player_x, SCREEN_WIDTH - PLAYER_SIZE))  # Keep within screen

        # Move blocks
        for block_data in blocks:
            block_data["y"] += block_data["speed"]
            
            # Convert to integers for M5Rect
            block_data["x"] = int(block_data["x"])
            block_data["y"] = int(block_data["y"])
            
            # Reset block when it reaches the bottom
            if block_data["y"] > SCREEN_HEIGHT:
                block_data["y"] = random.randint(-100, -20)
                block_data["x"] = random.randint(0, SCREEN_WIDTH - BLOCK_WIDTH)
                block_data["speed"] += BLOCK_SPEED_INCREASE  # Increase difficulty
                
                # Add a new block every 5 points (max 7)
                if score % 5 == 0 and len(blocks) < MAX_BLOCKS:
                    new_x = random.randint(0, SCREEN_WIDTH - BLOCK_WIDTH)
                    new_y = random.randint(-100, -20)
                    new_block = M5Rect(new_x, new_y, BLOCK_WIDTH, BLOCK_HEIGHT, color=0xff0000, fillcolor=0xff0000)
                    blocks.append({"obj": new_block, "x": new_x, "y": new_y, "speed": random.uniform(2, 4)})

        # Collision detection
        for block_data in blocks:
            if (player_x < block_data["x"] + BLOCK_WIDTH and
                player_x + PLAYER_SIZE > block_data["x"] and
                player_y < block_data["y"] + BLOCK_HEIGHT and
                player_y + PLAYER_SIZE > block_data["y"]):
                
                # Show Game Over screen
                lcd.clear()
                lcd.print("Game Over!", SCREEN_WIDTH//2 - 40, SCREEN_HEIGHT//2, 0xffffff)
                lcd.print("Score: " + str(score), SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT//2 + 20, 0xffffff)
                lcd.print("Press BtnA to Restart", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 40, 0xffffff)

                # Wait for BtnA to restart
                while not btnA.isPressed():
                    time.sleep(0.1)
                
                # Restart the game
                lcd.clear()
                start_game()
                return

        # Update player position
        player.setPosition(int(player_x), int(player_y))  # Ensure integer values

        # Update block positions
        for block_data in blocks:
            block_data["obj"].setPosition(int(block_data["x"]), int(block_data["y"]))  # Ensure integer values

        # Increase score over time
        score += 1
        # Clear previous score area
        lcd.rect(10, 10, 80, 20, 0x000000, fillcolor=0x000000)

        # Print updated score
        lcd.print("Score: " + str(int(score/10)), 10, 10, 0xffffff)

        time.sleep(0.05)  # Smooth movement delay

# Start the game
start_game()

