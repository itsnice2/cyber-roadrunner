"""
VersionsNr:        1.0.1
VersionsDatum:     22.05.2024

VersionsNr:        1.0.0
VersionsDatum:     22.05.2024
Autor:             L.Niebur
Funktion:          Dieses Programm steuert ein Fahrzeug mit einem Raspberry Pi und
                   verwendet Encoder, um die zurückgelegte Distanz zu messen. Es 
                   verwendet zwei Distanzzähler für die linken und rechten Räder 
                   und überwacht die zurückgelegte Strecke, um sicherzustellen, 
                   dass das Fahrzeug eine bestimmte Distanz fährt. Zudem überprüft 
                   es die Distanz zu einem Hindernis auf der rechten Seite und 
                   passt die Fahrtrichtung an, um einen sicheren Abstand zu halten.
                   Außerdem wird die aktuelle Geschwindigkeit der Räder gemessen und
                   ausgegeben.

Geändert:          L.Niebur 22.05.2024 V 1.0.1
                   - Neue Klasse speed_counter.py mit eingebunden, um die aktuelle Geschwindigkeit zu ermitteln                     
"""

import picar_4wd as fc
import time
import sys
from roadrunners.distance_counter import DistanzZaehler  # Import der DistanzZaehler-Klasse
from speed_counter import GeschwindigkeitsZaehler  # Import der GeschwindigkeitsZaehler-Klasse

# Funktion zur Überprüfung der Distanz zu einem Hindernis
def check_distance(target_distance, speed , angel):
    current_distance = fc.get_distance_at(angel)

    if current_distance > target_distance + 0.1:
        fc.turn_right(speed)
        #print("Abstand überschritten Delta", current_distance)

    elif current_distance < target_distance - 0.1:
        fc.turn_left(speed)
        #print("Abstand unterschritten Delta", current_distance)

# Hauptfunktion zur Steuerung des Fahrzeugs und Überwachung der Distanz und Geschwindigkeit
def main(speed, distance_m, target_distance , angel):
    # Initialisiere die Distanzzähler für die beiden Räder
    left_distance_counter = DistanzZaehler(in_pin=25)
    right_distance_counter = DistanzZaehler(in_pin=4)
    
    left_distance_counter.starten()
    right_distance_counter.starten()
    
    act_distance_left_m = 0
    act_distance_right_m = 0   
    
    mittel_distance = 0
    
    while mittel_distance < distance_m:
        # Aktualisiere die zurückgelegte Strecke basierend auf den Distanzzählern
        act_distance_left_m = left_distance_counter.entfernung_in_metern()
        act_distance_right_m = right_distance_counter.entfernung_in_metern()               

        # Überprüfe, ob die Zielstrecke erreicht wurde
        mittel_distance = (act_distance_left_m + act_distance_right_m) / 2

        if mittel_distance < 0.15:
            fc.forward(20)
        elif mittel_distance >= distance_m - 0.3:
            fc.forward(10)
        else:
            fc.forward(speed)
        
        # Funktion zur Überwachung der Distanz, momentan nur zur rechten Wand
        check_distance(target_distance, speed, angel)

    fc.stop()
    print("#####################################################################################")
    print("#####################################################################################")
    print("#####################################################################################")
    print(f"Gemessener erster Abstand:       {target_distance:.2f}")
    print("#####################################################################################")
    print("#####################################################################################")
    print(f"Zu fahrende Strecke plus Auto:   {distance_m:.2f} Meter")
    print("#####################################################################################")
    print("#####################################################################################")
    print(f"Abstand zur Wand nach der Fahrt: {fc.get_distance_at(angel):.2f} CM")
    print(f"Mittelwert:                      {mittel_distance:.2f} Meter")
    print(f"Aktuelle Strecke Links:          {act_distance_left_m:.2f} Meter")
    print(f"Aktuelle Strecke rechts:         {act_distance_right_m:.2f} Meter")
    print("#####################################################################################")
    print("#####################################################################################")
    print("#####################################################################################")
    left_distance_counter.deinit()
    right_distance_counter.deinit()

if __name__ == "__main__":
    try:
        
        
    

        if len(sys.argv) != 4:
            print("Usage: python fahr_los.py <speed> <distance_m>")
            sys.exit(1)

        laenge_car = 0.2  # Länge des Autos, damit es über die Linie fährt
        speed = int(sys.argv[1])
        distance_m = int(sys.argv[2])
        angel= int(sys.argv[3])
        distance_m = distance_m + laenge_car

        target_distance = fc.get_distance_at(angel)

        main(speed, distance_m, target_distance , angel )
    finally:
        fc.stop()
