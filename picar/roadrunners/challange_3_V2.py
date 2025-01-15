"""
VersionsNr:        1.0.1
VersionsDatum:     22.05.2024

VersionsNr:        1.0.0
VersionsDatum:     22.05.2024
Autor:             L.Niebur
Funktion:          Dieses Programm steuert ein Fahrzeug mit einem Raspberry Pi und
                   ruft die Fahrzeugklasse auf, um die zurückgelegte Distanz zu messen,
                   Hindernisse zu überwachen und die aktuelle Geschwindigkeit der Räder zu messen.

Geändert:          L.Niebur 22.05.2024 V 1.0.1
"""

import sys
import time
import picar_4wd as fc
from roadrunners.class.fahrzeug import Fahrzeug  # Import der Fahrzeug-Klasse
from drehung import Drehung  # Import der Drehung-Klasse

def main(speed, distance_m, angel):
    print("Abstand Wand vor Fahrt: ", fc.get_distance_at(angel))
    turn = False
    fahrzeug_hinfahrt_hin = Fahrzeug(speed, distance_m, angel)
    akt_target_wall = 0.0

    if fahrzeug_hinfahrt_hin.starten():
        print("Die Fahrt wurde erfolgreich beendet.")
        akt_target_wall = fahrzeug_hinfahrt_hin.akt_distance_wall()
        fc.servo.set_angle(angel * (-1))
        time.sleep(1)
        turn = True

    if turn:        
        drehung = Drehung(speed, angel, akt_target_wall)
        if drehung.starten():
            print("Die Drehung wurde erfolgreich beendet.")

    if drehung.starten():
        print("Rückfahrt gestartet")
        fahrzeug_hinfahrt_zur = Fahrzeug(speed, distance_m, (angel * (-1)))
        fahrzeug_hinfahrt_zur.starten()

    fc.stop()

if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            print("Usage: python challange_3.py <speed> <distance_m> <angel>")
            sys.exit(1)

        if fc.power_read() < 7.0:
            print("Die Ladung des Akkus reicht nicht aus", fc.power_read())
            sys.exit(1)

        print("Die Aktuelle Ladung des Akkus", fc.power_read())    
        
        laenge_car = 0.2  # Länge des Autos, damit es über die Linie fährt
        speed = int(sys.argv[1])
        distance_m = int(sys.argv[2])
        angel = int(sys.argv[3])
        distance_m = distance_m + laenge_car
        fc.servo.set_angle(angel)
        time.sleep(1)

        main(speed, distance_m, angel)
    finally:
        fc.stop()
