import picar_4wd as fc 
import time
import math
from fahrzeug import Fahrzeug
#angle_min   = 0
#distance_min= 0

target_distance         = 0
toleranz                = 0.25
toleranz_max            = 6
speed                   = 50
korrektur_speed         = speed * 0.92
turn_counter            = 0




def scan_rechts(): 
    
    ANGLE_RANGE = 90 

    STEP = 3 
    steps = int(ANGLE_RANGE/STEP) 
    us_step = STEP 
    max_angle = ANGLE_RANGE
    min_angle = -ANGLE_RANGE 
    current_angle = min_angle 
    distances = [] 
    global angle_min, distance_min, distance
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
        richtung = -90
        ausrichten(richtung)
        print("hallo")
        return angle_min, distance_min, richtung


    else: 
        print("Keine gültigen Distanzen gefunden.")  




def scan_links(): 
    
    ANGLE_RANGE = 90 

    STEP = 3 
    steps = int(ANGLE_RANGE/STEP) 
    us_step = STEP 
    max_angle = ANGLE_RANGE
    min_angle = 0 
    current_angle = min_angle 
    distances = [] 
    global angle_min, distance_min, distance
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
        richtung = 90
        ausrichten(richtung)
        print("hallo")
        return angle_min, distance_min, richtung


    else: 
        print("Keine gültigen Distanzen gefunden.")  








def check_0_seite(): 
    
    global angle_min, distance_min, distance
    angle_min = 0
    weg_frei= True

    #schwenken des sensors in (steps) schritten 

    while(weg_frei == True):
        
        fc.forward(speed)
        #distance = fc.get_distance_at(0)
        #time.sleep(0.1)
        distance = fc.get_distance_at(0)
         
        if distance < 0:
            #print("Distance:", distance) 
            continue 
        else:
            print("check_distance: ", distance, "bei winkel: 0")
            if distance < 20:
                print("stop")
                weg_frei = False
                fc.turn_left(speed)
                time.sleep(0.5)
                scan_rechts()

            #else:
                #distance = fc.get_distance_at(0)
                #an_wand_entlang(-90)

              

       




def ausrichten(richtung):
    global target_distance, turn_counter
    current_distance = fc.get_distance_at(richtung)
    print("wpgh", angle_min)
    distance_corr = distance_min + (12,5-(12,5*math.sin(math.radians(abs(angle_min)))))
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
    if( turn_counter % 2 == 0):
        an_wand_entlang(richtung)
    else:    
        check_0_seite()






def an_wand_entlang(angel):
    turn_left               = False
    turn_right              = False
    forward                 = False
    max_target_distance     = target_distance + toleranz
    min_target_distance     = target_distance - toleranz
    distance = fc.get_distance_at(-90)
    print("ziel distanz zur wand", target_distance)
    if fc.get_distance_at(-90) > 0 :

        #if current_distance > target_distance + self.toleranz and current_distance < target_distance + 20:
        if distance > max_target_distance and not distance > target_distance + toleranz_max: 
            if  turn_right == False: 
                fc.left_front.set_power( speed )
                fc.right_front.set_power( speed - korrektur_speed)
                fc.left_rear.set_power( speed )                     
                fc.right_rear.set_power( speed - korrektur_speed)
            turn_right = True    
            turn_left  = False
            forward    = False           
            print("Abstand zu gross", distance, max_target_distance)
        #elif current_distance < target_distance - self.toleranz and current_distance > target_distance - 10: 
        elif distance < min_target_distance and not distance < target_distance - toleranz_max :    
            if turn_left == False:
                fc.left_front.set_power( speed - korrektur_speed) 
                fc.right_front.set_power( speed )
                fc.left_rear.set_power( speed - korrektur_speed)                    
                fc.right_rear.set_power( speed )
            turn_right = False
            turn_left  = True
            forward    = False
            print("Abstand zu klein", distance, max_target_distance)
        else:
            if forward == False:    
                fc.left_front.set_power( speed) 
                fc.right_front.set_power( speed )
                fc.left_rear.set_power( speed )                    
                fc.right_rear.set_power( speed )
            turn_right = False 
            turn_left  = False
            forward    = True
    else:
        fc.stop
            #print("Geradeaus")
            #print( current_distance )





 

if __name__ == "__main__": 

    try: 
        for i in range(1):
             
            #scan_rechts()
            check_0_seite()
            time.sleep( 0.1 )

    finally: 
        fc.stop() 

 

 

 

 
