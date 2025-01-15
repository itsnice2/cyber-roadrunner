import pygame
import picar_4wd as fc

# Initialisieren der pygame-Bibliothek und des Gamepads
pygame.init()
pygame.joystick.init()

# Überprüfen, ob ein Gamepad angeschlossen ist
if pygame.joystick.get_count() == 0:
    print("Kein Gamepad angeschlossen!")
    exit()

# Erstes angeschlossenes Gamepad auswählen
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initiale Werte
power_val = 50
max_power_val = 100
min_power_val = 10

print("Drücken Sie 'q' zum Beenden.")

def scale_axis(value, deadzone=0.1, scale=1):
    """Achsenwert skalieren und Deadzone anwenden."""
    if abs(value) < deadzone:
        return 0
    return value * scale

def handle_gamepad_input():
    """Eingaben des Gamepads lesen und PiCar steuern."""
    global power_val
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                # Achsenbewegungen lesen
                x_axis = joystick.get_axis(0)  # Lenkung
                y_axis = joystick.get_axis(1)  # Geschwindigkeit

                # Steuerungslogik für die Lenkung
                x_scaled = scale_axis(x_axis)
                y_scaled = scale_axis(y_axis)

                if y_scaled < -0.1:
                    fc.forward(int(-y_scaled * power_val))
                elif y_scaled > 0.1:
                    fc.backward(int(y_scaled * power_val))
                elif x_scaled < -0.1:
                    fc.turn_left(int(-x_scaled * power_val))
                elif x_scaled > 0.1:
                    fc.turn_right(int(x_scaled * power_val))
                else:
                    fc.stop()
            
            elif event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(0):  # A Button
                    if power_val <= max_power_val - 10:
                        power_val += 10
                        print("Leistungswert erhöht:", power_val)
                elif joystick.get_button(1):  # B Button
                    if power_val >= min_power_val + 10:
                        power_val -= 10
                        print("Leistungswert verringert:", power_val)
                elif joystick.get_button(6):  # Back Button
                    print("Beenden")
                    running = False

    pygame.quit()

if __name__ == '__main__':
    handle_gamepad_input()
