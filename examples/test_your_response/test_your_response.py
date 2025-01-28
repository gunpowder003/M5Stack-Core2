from m5stack import *
from m5ui import *
from uiflow import *
import time
import random

# Initialize the screen
setScreenColor(0x000000)
label = M5TextBox(50, 100, "Tap to Start!", lcd.FONT_DejaVu24, 0xFFFFFF, rotate=0)

game_started = False
target_visible = False
start_time = 0
reaction_time = 0
target_time = 0
high_score = None  # Track the fastest reaction time

def buttonA_wasPressed():
    global game_started, target_visible, start_time
    if not game_started:
        start_game()
    elif target_visible:
        end_game()

def start_game():
    global game_started, target_visible, start_time, target_time
    game_started = True
    target_visible = False
    setScreenColor(0x000000)
    label.setText("Wait for the target...")
    start_time = time.ticks_ms()
    target_time = start_time + random.randint(1000, 5000)  # Random delay between 1 and 5 seconds

def show_target():
    global target_visible, start_time
    target_visible = True
    setScreenColor(0x00FF00)  # Green screen
    label.setText("Tap Now!")
    start_time = time.ticks_ms()  # Reset the timer for reaction time

def end_game():
    global game_started, target_visible, reaction_time, high_score
    reaction_time = time.ticks_ms() - start_time
    game_started = False
    target_visible = False

    # Update high score
    if high_score is None or reaction_time < high_score:
        high_score = reaction_time

    # Display results
    setScreenColor(0x000000)
    label.setText("Reaction Time: " + str(reaction_time) + " ms\nHigh Score: " + str(high_score) + " ms\nTap to Restart!")

# Bind button A to the game
btnA.wasPressed(buttonA_wasPressed)

# Main loop
while True:
    if game_started and not target_visible and time.ticks_ms() >= target_time:
        show_target()
    wait_ms(100)
