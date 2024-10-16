## Particle Tracking Velocimetry
This is the code I wrote for my first year University of Birmingham "Labs and Data analysis" Chemical engineering module's 'Particle Tracking Velocimetry' project. 
#### The brief: 
To construct a 'home experiment' to measure the coefficient of restitution of an object using particle tracking velocimetry.

### What is it?
This code simply tracks a circular object from a video from your library (but can also track live local-cam video too with some altercations). It is currently tailored to a table tennis ball and plots the locations of the found circle (representing the ball) in every frame, and calculates the corresponding coefficient of restitution (COR).
It uses the acclaimed cv2 python library to track the ball. See OpenCV.org

The code has comments explaining almost every step/ line of code.
### Limitations:
This code is by no means perfect and can most definitely be improved upon, it is one of my first python projects and there is likely many other more advanced projects elsewhere.

The exact cv2 code written was dedicated to my recorded videos, hence to get an accurate model from another source certain variables will need to be altered.

Note it is necessary to press 'q' before the end of the video(s) to prevent an error.
 
