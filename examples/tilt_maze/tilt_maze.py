from m5stack import *
from m5ui import *
from uiflow import *
import imu
import random
import collections  # Needed for Breadth FS
import time

# Initialize display and IMU
setScreenColor(0x000000)
imu0 = imu.IMU()

# Maze settings
grid_size = 40  # Fit 320x240 screen
maze_width = 8
maze_height = 6
maze = [[1] * maze_width for _ in range(maze_height)]  # Start with walls

# Ball properties
ball_radius = 8
ball_speed = 0.5  # Base sensitivity
ball_velocity_x = 0  # Initial velocity on X-axis
ball_velocity_y = 0  # Initial velocity on Y-axis
ball_max_speed = 5  # Limit max speed to prevent overshooting
scaling_factor = 2  # Scaling factor for responsiveness (higher = more responsive)
friction = 0.90  # Inertia / friction factor to slow the ball over time
scale_x = 2.0  # Scaling factor for X-axis tilt
scale_y = 2.0  # Scaling factor for Y-axis tilt

# Fixed screen dimensions for M5Stack Core2
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

# Start and end positions
start_x, start_y = 0, 0
end_x, end_y = 0, 0
ball_x, ball_y = 0, 0

# Maze generation using DFS (Always Solvable)
def generate_maze():
    global maze, start_x, start_y, end_x, end_y, ball_x, ball_y

    # Initialize the maze with walls
    maze = [[1] * maze_width for _ in range(maze_height)]

    # Choose a random starting point
    start_x, start_y = random.randint(0, maze_width - 1), random.randint(0, maze_height - 1)

    # DFS-based maze generation
    def carve_maze(x, y):
        maze[y][x] = 0  # Mark as path

        # Randomize movement direction manually (since shuffle is unavailable)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for i in range(len(directions) - 1, 0, -1):  # Fisher-Yates shuffle
            j = random.randint(0, i)  # Randomly shuffle directions
            directions[i], directions[j] = directions[j], directions[i]

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < maze_width and 0 <= ny < maze_height and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0  # Open wall
                carve_maze(nx, ny)

    carve_maze(start_x, start_y)

    # Find the farthest point using BFS
    def find_farthest_point(sx, sy):
        visited = [[False] * maze_width for _ in range(maze_height)]
        queue = collections.deque([(sx, sy, 0)])  # (x, y, distance)
        visited[sy][sx] = True
        farthest_x, farthest_y, max_dist = sx, sy, 0

        while queue:
            x, y, dist = queue.popleft()
            if dist > max_dist:
                max_dist = dist
                farthest_x, farthest_y = x, y

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < maze_width and 0 <= ny < maze_height and not visited[ny][nx] and maze[ny][nx] == 0:
                    visited[ny][nx] = True
                    queue.append((nx, ny, dist + 1))

        return farthest_x, farthest_y

    # Set the farthest valid end point
    end_x, end_y = find_farthest_point(start_x, start_y)

    # Set ball to start position
    ball_x, ball_y = start_x * grid_size + grid_size // 2, start_y * grid_size + grid_size // 2

generate_maze()

# Function to draw the maze
def draw_maze():
    lcd.clear(0x000000)  # Black background
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                lcd.rect(x * grid_size, y * grid_size, grid_size, grid_size, color=0xFFFFFF, fillcolor=0xFFFFFF)

    # Draw red flag at the destination
    flag_x, flag_y = end_x * grid_size + grid_size // 2, end_y * grid_size + grid_size // 2
    lcd.triangle(flag_x, flag_y - 10, flag_x - 6, flag_y + 6, flag_x + 6, flag_y + 6, color=0xFF0000, fillcolor=0xFF0000)

# Function for game over screen
def game_over():
    lcd.fill(0x000000)  # Clear screen
    lcd.text(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 10, "GAME OVER", 0xFFFFFF)
    while True:
        if btnA.isPressed():
            return  # Exit game over state when button A is pressed

# Main game loop
def game_loop():
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y

    draw_maze()  # Draw maze once at the start

    while True:
        # Erase previous ball position
        lcd.circle(int(ball_x), int(ball_y), ball_radius, color=0x000000, fillcolor=0x000000)

        # Get accelerometer readings
        ax = imu0.acceleration[0]  # X-axis acceleration
        ay = imu0.acceleration[1]  # Y-axis acceleration

        # Apply scaling factor to tilt input for higher responsiveness
        ball_velocity_x += -ax * scale_x  # Inverted for proper direction
        ball_velocity_y += ay * scale_y  # Apply to Y-axis (up-down)

        # Apply friction to simulate slowing down
        ball_velocity_x *= friction
        ball_velocity_y *= friction

        # Update ball position based on velocity
        ball_x += ball_velocity_x
        ball_y += ball_velocity_y

        # Ensure the ball stays within the maze boundaries
        ball_x = max(0, min(SCREEN_WIDTH - 1, ball_x))
        ball_y = max(0, min(SCREEN_HEIGHT - 1, ball_y))

        # Convert the ball's position to integers for grid-based calculation
        grid_x = int(ball_x // grid_size)
        grid_y = int(ball_y // grid_size)

        # Prevent moving into walls by checking if the ball is inside the maze grid
        if 0 <= grid_x < maze_width and 0 <= grid_y < maze_height and maze[grid_y][grid_x] == 0:
            ball_x, ball_y = ball_x, ball_y
        else:
            # Adjust ball position if it hits a wall
            # Check in all four directions to find the point of collision
            if maze[grid_y][grid_x] == 1:  # If ball is colliding with a wall
                # Move ball back to a valid position (slightly inside the grid)
                ball_x -= ball_velocity_x  # Revert X velocity
                ball_y -= ball_velocity_y  # Revert Y velocity

            # Reverse velocity after collision
            ball_velocity_x = -ball_velocity_x
            ball_velocity_y = -ball_velocity_y

        # Draw ball at new position
        lcd.circle(int(ball_x), int(ball_y), ball_radius, color=0x00FFFF, fillcolor=0x00FFFF)

        # Check if player reaches the goal
        grid_x = int(ball_x // grid_size)  # Ensure conversion to int before accessing grid
        grid_y = int(ball_y // grid_size)
        if grid_x == end_x and grid_y == end_y:
            lcd.print("YOU WIN!", 100, 110, 0xFFFF00)
            wait(2)
            generate_maze()
            draw_maze()
            ball_x, ball_y = start_x * grid_size + grid_size // 2, start_y * grid_size + grid_size // 2

        # Restart if Button A is pressed
        if btnA.isPressed():
            generate_maze()
            draw_maze()
            ball_x, ball_y = start_x * grid_size + grid_size // 2, start_y * grid_size + grid_size // 2

        wait_ms(30)  # Reduce flickering


game_loop()
