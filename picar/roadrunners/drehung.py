"""
VersionsNr:        1.0.1
VersionsDatum:     22.05.2024

VersionsNr:        1.0.0
VersionsDatum:     22.05.2024
Autor:             L.Niebur
Funktion:          Diese Klasse steuert die Drehung eines Fahrzeugs mit einem Raspberry Pi.
                   Es dreht das Fahrzeug für mindestens 2 Sekunden und stoppt dann die
                   Drehung, sobald der gemessene Abstand kleiner oder gleich dem übergebenen
                   Zielabstand ist.

Geändert:          L.Niebur 22.05.2024 V 1.0.1
"""

import time
import picar_4wd as fc

class Drehung:
    def __init__(self, speed, angel, akt_target_wall):
        self.speed = speed
        self.angel = angel
        self.akt_target_wall = akt_target_wall
        self.turn_speed = 100
        self.toleranz = 4
        self.akt_turn_begin_distance = fc.get_distance_at()


    def starten(self):
        turn = True
        fahre_zur = False
        
        # Phase 1: Mindestens 2 Sekunden drehen
        print("Drehung gestartet.")
        start_time_turn = time.time()
        min_turn_duration = 2  # Minimale Drehzeit in Sekunden

        fc.left_front.set_power(-self.turn_speed)
        fc.left_rear.set_power(-self.turn_speed)
        fc.right_front.set_power(self.turn_speed)
        fc.right_rear.set_power(self.turn_speed)

        while time.time() - start_time_turn < min_turn_duration:
            time.sleep(0.1)  # Kurze Pause, um die Schleife nicht zu schnell laufen zu lassen

        # Phase 2: Drehung basierend auf der Abstandsüberprüfung
        fc.left_front.set_power(-self.turn_speed)
        fc.left_rear.set_power(-self.turn_speed)
        fc.right_front.set_power(self.turn_speed)
        fc.right_rear.set_power(self.turn_speed)

        while turn:
            target = fc.get_distance_at(self.angel * (-1))
            if target <= (self.akt_turn_begin_distance + self.toleranz) and target != -2:
                turn = False
                fahre_zur = True

            time.sleep(0.01)  # Kurze Pause, um die Schleife nicht zu schnell laufen zu lassen

        fc.stop()
        print("Drehung beendet.")
        return fahre_zur
