game where you need to maintain the ball on the screen for as long as possible by 
tilting the Core2. It utilize MPU6050 sensor to read tilting value and refresh the ball position accordingly

You can play around with several parameter to change the ball behaviour
# Parameters
ball_radius = 15
update_interval = 0.0000001  # 10 ms for faster refresh rate
velocity_x = 0
velocity_y = 0
friction = 0.90  # Lower friction to reduce the rate of slowing down
scale_x = 4.0  # Increase scaling factor to make the ball more responsive to tilt
scale_y = 4.0  # Increase scaling factor to make the ball more responsive to tilt
