**SAVE THE ASTRONAUT!**
![WhatsApp Image 2025-01-10 at 6 11 26 PM](https://github.com/user-attachments/assets/e129a09a-12e7-4428-906b-6e9a76806353)

The objective is to get the astronaut to safety while avoiding deadly red lasers and blue gravity wells that can pull into a blackhole!

**HOW TO PLAY:**
1. Tilt the M5stack module to move the astronaut (represented by white ball) around avoiding obstacle to reach green box
2. To reset the level, press A button
3. To pause/resume the game, press B button
4. Have fun!



**Parameter that can be changed to increase game difficulty**

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

**Demo Video**

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/lNbYLPG1SOM/0.jpg)](https://www.youtube.com/watch?v=lNbYLPG1SOM)

**Known Bugs**
1. Sometimes, the random placement of obstacle and the astronaut make it impossible to complete the level
2. The laser or well sometimes are not being drawn properly
3. Touching the laser or well partially did not end the level
