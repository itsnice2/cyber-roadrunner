import picar_4wd as fc
import sys
import asyncio
from inputs import get_gamepad
import inputs
import time
 
power_val = 50
 
def process_event(event):
    global power_val
    if event.ev_type == 'Absolute':
        if event.code == 'ABS_X':
            # Left thumbstick X axis
            if event.state < -8000:
                fc.turn_left(power_val)
            elif event.state > 8000:
                fc.turn_right(power_val)
            else:
                fc.stop()
        elif event.code == 'ABS_Y':
            # Left thumbstick Y axis
            if event.state < -8000:
                fc.forward(power_val)
            elif event.state > 8000:
                fc.backward(power_val)
            else:
                fc.stop()
        elif event.code == 'ABS_Z':
            # Left trigger
            if event.state > 0:
                if power_val <= 90:
                    power_val += 10
                    print("Power_val increased to:", power_val)
        elif event.code == 'ABS_RZ':
            # Right trigger
            if event.state > 0:
                if power_val >= 10:
                    power_val -= 10
                    print("Power_val decreased to:", power_val)
    elif event.ev_type == 'Key':
        if event.code == 'BTN_SOUTH' and event.state == 1:
            # A button pressed
            print("A button pressed, stopping.")
            fc.stop()
        elif event.code == 'BTN_WEST' and event.state == 1:
            # X button pressed, quit
            print("X button pressed, quitting.")
            return False
    return True
 
def Gamepad_control():
    print("If you want to quit, press the X button on the gamepad.")
    try:
        while True:
            events = get_gamepad()
            for event in events:
                if not process_event(event):
                    return
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Quit")
 
if __name__ == '__main__':
    Gamepad_control()