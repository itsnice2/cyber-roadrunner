import pygame
import time
import RPi.GPIO as GPIO
 
# GPIO-Setup (angepasst an dein Pi-Car)
MOTOR_LEFT_FORWARD = 17
MOTOR_LEFT_BACKWARD = 18
MOTOR_RIGHT_FORWARD = 22
MOTOR_RIGHT_BACKWARD = 23
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_BACKWARD, GPIO.OUT)
 
def motor_control(left_f, left_b, right_f, right_b):
    GPIO.output(MOTOR_LEFT_FORWARD, left_f)
    GPIO.output(MOTOR_LEFT_BACKWARD, left_b)
    GPIO.output(MOTOR_RIGHT_FORWARD, right_f)
    GPIO.output(MOTOR_RIGHT_BACKWARD, right_b)
 
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()
 
print('Joystick: ', joystick.get_name())
 
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                left_y = joystick.get_axis(1)  # Left stick Y axis
                right_y = joystick.get_axis(3)  # Right stick Y axis
 
                if left_y < -0.1:
                    motor_control(1, 0, 0, 0)  # Left motor forward
                elif left_y > 0.1:
                    motor_control(0, 1, 0, 0)  # Left motor backward
                elif right_y < -0.1:
                    motor_control(0, 0, 1, 0)  # Right motor forward
                elif right_y > 0.1:
                    motor_control(0, 0, 0, 1)  # Right motor backward
                else:
                    motor_control(0, 0, 0, 0)  # Stop all motors
 
        time.sleep(0.1)
 
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
    pygame.quit()