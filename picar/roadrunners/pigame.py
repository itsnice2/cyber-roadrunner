import pygame
import time
 
pygame.init()
pygame.joystick.init()
 
joystick = pygame.joystick.Joystick(0)
joystick.init()
 
print('Joystick: ', joystick.get_name())
 
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print('Button pressed')
            elif event.type == pygame.JOYBUTTONUP:
                print('Button released')
 
            if event.type == pygame.JOYAXISMOTION:
                print('Axis motion', event.axis, event.value)
 
        time.sleep(0.1)
 
except KeyboardInterrupt:
    print("Exiting...")
finally:
    pygame.quit()