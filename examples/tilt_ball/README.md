Game where you need to maintain the ball on the screen for as long as possible by 
tilting the Core2. It utilize MPU6050 sensor to read tilting value and refresh the ball position accordingly

To play:
1. tilt the device
2. it will be game over if the ball touch the screen border
3. Press left button (button A to restart)
4. Enjoy!
   
You can play around with several parameter to change the ball behaviour
Harder setting:<br/>
friction = 0.95  # Lower friction to reduce the rate of slowing down<br/>
scale_x = 30.0  # Increase scaling factor to make the ball more responsive to tilt<br/>
scale_y = 30.0 <br/>

Parameters
ball_radius = 15<br/>
update_interval = 0.0000001  # 10 ms for faster refresh rate<br/>
velocity_x = 0<br/>
velocity_y = 0<br/>
friction = 0.90  # Lower friction to reduce the rate of slowing down<br/>
scale_x = 4.0  # Increase scaling factor to make the ball more responsive to tilt<br/>
scale_y = 4.0  # Increase scaling factor to make the ball more responsive to tilt<br/>


Gameplay:<br/>
[![TILT_BALL](http://img.youtube.com/vi/HZU05NTX5SQ/0.jpg)](http://www.youtube.com/watch?v=HZU05NTX5SQ "TILT_BALL")

