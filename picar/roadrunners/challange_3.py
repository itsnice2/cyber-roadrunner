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

import os
import sys
import time
import picar_4wd as fc
from fahrzeug import Fahrzeug  # Import der Fahrzeug-Klasse
import speed_counter as sc

def main(speed, turn_speed, distance_m, angel, target_distance ):
    print("################################################################################")
    print("Abstand Wand vor Fahrt: ", fc.get_distance_at(angel))
    print("################################################################################\n")
    turn = False
    fahre_zu = False
    fahrzeug_hinfahrt_hin = Fahrzeug(speed, distance_m, angel, target_distance)
    akt_target_wall = 0.0
    dreh_speed = turn_speed

    if fahrzeug_hinfahrt_hin.starten():
        #print("Die Fahrt wurde erfolgreich beendet.")
        akt_target_wall = fahrzeug_hinfahrt_hin.akt_distance_wall()
        fc.servo.set_angle(angel * (-1))
        time.sleep(1)
        turn = True

    if turn:        
        # Phase 1: Mindestens 2 Sekunden drehen
        print("################################################################################")
        print("Drehung gestartet.")
        print("################################################################################\n")
        start_time_turn = time.time()
        min_turn_duration = 0.2  # Minimale Drehzeit in Sekunden

        fc.left_front.set_power(-dreh_speed)
        fc.left_rear.set_power(-dreh_speed)
        fc.right_front.set_power(dreh_speed)
        fc.right_rear.set_power(dreh_speed)

        while time.time() - start_time_turn < min_turn_duration:
            
            time.sleep(0.1)  # Kurze Pause, um die Schleife nicht zu schnell laufen zu lassen

        # Phase 2: Drehung basierend auf der Abstandsüberprüfung
        fc.left_front.set_power(-dreh_speed)
        fc.left_rear.set_power(-dreh_speed)
        fc.right_front.set_power(dreh_speed)
        fc.right_rear.set_power(dreh_speed)

        while turn:
            target = fc.get_distance_at(angel * (-1))
            #print("################################################################################")
            #print("Aktueller Abstand: ", target)
            #print("################################################################################")
             
            
            if target <= ( akt_target_wall + 3 ) and target != -2:
                print("Übergebener Abstand:", akt_target_wall)
                print("Gemessener Abstand:", target)
                print("################################################################################")
                print("Drehung beendet.")
                print("################################################################################\n")
                turn = False
                fahre_zur = True                

            time.sleep(0.05)  # Kurze Pause, um die Schleife nicht zu schnell laufen zu lassen

    if  fahre_zur:
        print("################################################################################")
        print("Rückfahrt gestartet")
        print("################################################################################")
        fahrzeug_hinfahrt_zur = Fahrzeug(speed, distance_m , ( angel * (-1) ), target_distance )
        fahrzeug_hinfahrt_zur.starten()

    
    fc.stop()
    print("################################################################################")
    print("Fahrt beendet.")
    print("################################################################################\n")

if __name__ == "__main__":
    try:
        if len(sys.argv) != 5:
            print("Usage: python challange_3.py <speed> <distance_m> <angel>")
            sys.exit(1)

        if fc.power_read() < 7.0:
            print("Die Ladung des Akkus reicht nicht aus", fc.power_read())
            sys.exit(1)

        print("\n################################################################################")
        print("Die Aktuelle Ladung des Akkus", fc.power_read() ," Volt")  
        print("################################################################################\n")
  
        
        laenge_car = 0.2  # Länge des Autos, damit es über die Linie fährt
        speed = int(sys.argv[1])
        turn_speed = int(sys.argv[2])
        distance_m = int(sys.argv[3])
        angel = int(sys.argv[4])
        distance_m = distance_m + laenge_car
        fc.servo.set_angle(angel)
        time.sleep(1)
        geschwindigkeit = sc.GeschwindigkeitsZaehler()
        #geschwindigkeit = geschwindigkeit.geschwindigkeit_in_m_pro_s()
        geschwindigkeit = "echo " + str( geschwindigkeit.geschwindigkeit_in_m_pro_s() ) + " >> ~/virtual-env/geschwindigkeit.txt"
 
        os.system(geschwindigkeit)

        target_distance = fc.get_distance_at( angel )

        main(speed, turn_speed, distance_m, angel, target_distance)
    finally:
        fc.stop()
