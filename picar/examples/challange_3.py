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
from fahrzeug import Fahrzeug  # Import der Fahrzeug-Klasse
import RPi.GPIO as GPIO

# Setze die GPIO-Pin-Nummerierungsmethode
GPIO.setmode(GPIO.BCM)

def main(speed, distance_m, angel):
    fahrzeug_hinfahrt = Fahrzeug(speed, distance_m, angel)

    if fahrzeug_hinfahrt.starten():
        print("Die Fahrt wurde erfolgreich beendet.")
        print("Drehung gestartet.")
        # Drehung um 180 Grad nach rechts
        fc.turn_right(50)
        time.sleep(1.0)  # Passe die Dauer der Drehung an, um eine vollständige Drehung zu erreichen
        fc.stop()
        print("Drehung beendet.")

if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            print("Usage: python challange_3.py <speed> <distance_m> <angel>")
            sys.exit(1)
        
        laenge_car = 0.2  # Länge des Autos, damit es über die Linie fährt
        speed = int(sys.argv[1])
        distance_m = int(sys.argv[2])
        angel = int(sys.argv[3])
        distance_m = distance_m + laenge_car

        main(speed, distance_m, angel)
    finally:
        fc.stop()
        GPIO.cleanup()  # Bereinige die GPIOs beim Beenden des Programms
