import picar_4wd as fc 
import sys
import time
import math
from fahrzeug import Fahrzeug

anzahl_hindernisse 		= 3 ####hier die genaue Anzahl der Hindernisse angeben
target_distance         = 0
toleranz                = 0.25
toleranz_max            = 6
speed                   = int(sys.argv[1])
korrektur_speed         = speed * 0.92
turn_counter            = 0
richtung                = -90
ausrichtung		        = int(sys.argv[2])

### Ausrichten 1 #####################################################################################################################
def ausrichten1(ausrichtung):
    ANGLE_RANGE = 90 

    STEP = 3 
    steps = int(ANGLE_RANGE/STEP) 
    us_step = STEP 
    max_angle = ANGLE_RANGE

    if ausrichtung == "rechts":
        min_angle = -ANGLE_RANGE
    elif ausrichtung == "links":
        min_angle = 0  
    current_angle = min_angle 
    distances = [] 
    global angle_min, distance_min, distance, richtung
    angle_min = 0
    distance_min = 0

    #schwenken des sensors in (steps) schritten 

    for i in range(steps): 
        current_angle += us_step 
        if current_angle >= max_angle: 
            current_angle = max_angle 
            us_step = -STEP 

        elif current_angle <= min_angle: 
            current_angle = min_angle 
            us_step = STEP  

        #messen des abstandes zur Wand 
        distance = fc.get_distance_at(current_angle) 

        #keine wand gefunden verwerfen 
        if distance < 0:
            print(f"Angle: {current_angle}, Distance: {distance}") 
            continue 

        #in einem array speichern 
        else: 
            distances.append((current_angle, distance)) 
            print(f"Angle: {current_angle}, Distance: {distance}") 

    #ermitteln des mindesabstandes zur Wand 
    if distances: 
        min_distance_angle = min(distances, key=lambda x: x[1]) 
        print(f"Der minimale Abstand gerade ist: {min_distance_angle[1]}, bei einem Winkel von: {min_distance_angle[0]}")              

        #Rückgabe minimaler Abstand und dessen Winkel  
        #return min_distance_angle[1], min_distance_angle[0]  
        angle_min = min_distance_angle[0]
        distance_min = min_distance_angle[1]
        
        if ausrichtung == "rechts":
            richtung = -90
        elif ausrichtung == "links":
            richtung = 90  
            
        ausrichten2(richtung)
        return angle_min, distance_min, richtung


    else: 
        print("Keine gültigen Distanzen gefunden.")

### Ausrichten 2 #####################################################################################################################
def ausrichten2(richtung):
    global target_distance, turn_counter
    current_distance = fc.get_distance_at(richtung)
    #print("angle_min", angle_min)
    distance_corr = distance_min +  (1.2 *(12.5-(12.5*math.sin(math.radians(abs(angle_min)))))) 	###Korrekturfaktor verändert und ungetestet
    target_distance = distance_corr 
    print("distance_min: ", distance_min, "distance_corr: ", distance_corr )
    print( "current_distance_init: ", current_distance)

    while current_distance > distance_corr or current_distance < 0:
        fc.turn_left(50)
        current_distance = fc.get_distance_at(richtung)
        print( "current_distance: ", current_distance)
        time.sleep (0.01)
    turn_counter = turn_counter + 1
    time.sleep (0.5)

def main(speed, ausrichtung):
    # Akku-Check #############################################################################
    
    if fc.power_read() < 7.0:
        print("Die Ladung des Akkus reicht nicht aus", fc.power_read())
        sys.exit(1)
    print("Akkucheck ok: " + str(fc.power_read()))
    
    # Ausrichten #############################################################################

    if ausrichtung == "vorne":
        print( fc.get_distance_at(0) )
    else:
        ausrichten1(ausrichtung)

    # Sensor nach vorn und losfahren #########################################################
    #fc.forward(speed)
    #print(">>>>> Los geht's! <<<<<")

    # Ziellinie erreicht? ####################################################################
    #while ziellinie_erreicht = False:
        #mach was
    
        # Hindernis? #############################################################################
        #if hindernis_erkannt() = True:
            # abstand_links messen
            # abstand_rechts messen
            #if abstand_links < abstand_rechts:
                #Drehung 90° rechts
                #while hindernis_weg = False
                #fc.forward(speed)
            #else:
                #Drehung 90° links
        #else:
            #mach was anderes

if __name__ == "__main__": 
    while True:
        try:
            main(speed, ausrichtung)
        finally:
            fc.stop()
