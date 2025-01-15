"""
VersionsNr:        1.0.1
VersionsDatum:     22.05.2024

VersionsNr:        1.0.0
VersionsDatum:     22.05.2024
Autor:             L.Niebur
Funktion:          Diese Klasse steuert ein Fahrzeug mit einem Raspberry Pi und
                   verwendet Encoder, um die zurückgelegte Distanz zu messen. Es 
                   verwendet zwei Distanzzähler für die linken und rechten Räder 
                   und überwacht die zurückgelegte Strecke, um sicherzustellen, 
                   dass das Fahrzeug eine bestimmte Distanz fährt. Zudem überprüft 
                   es die Distanz zu einem Hindernis auf der rechten Seite und 
                   passt die Fahrtrichtung an, um einen sicheren Abstand zu halten.
                   Außerdem wird die aktuelle Geschwindigkeit der Räder gemessen und
                   ausgegeben.

Geändert:          L.Niebur 22.05.2024 V 1.0.1
"""

import picar_4wd as fc
import time
from distance_counter import DistanzZaehler  # Import der DistanzZaehler-Klasse

class Fahrzeug:
    def __init__( self, speed, distance_m, angel, target_distance ):
        self.speed           = speed
        self.distance_m      = distance_m
        self.angel           = angel
        self.target_distance = target_distance
        self.turn_left       = False
        self.turn_right      = False
        self.forward         = False
        self.toleranz        = 0.25
        self.toleranz_max    = 6
        self.korrektur_speed = speed * 0.92
        self.min_target_distance = target_distance - self.toleranz
        self.max_target_distance = target_distance + self.toleranz

        
        # Initialisiere die Distanzzähler für die beiden Räder
        self.left_distance_counter  = DistanzZaehler( in_pin=25 )
        self.right_distance_counter = DistanzZaehler( in_pin=4 )
        
    def starten(self):
        self.left_distance_counter.starten()
        self.right_distance_counter.starten()
        
        act_distance_left_m  = 0
        act_distance_right_m = 0   
        mittel_distance      = 0        
        
        while act_distance_left_m < self.distance_m or  act_distance_right_m < self.distance_m :
            # Aktualisiere die zurückgelegte Strecke basierend auf den Distanzzählern
            act_distance_left_m  = self.left_distance_counter.entfernung_in_metern()
            act_distance_right_m = self.right_distance_counter.entfernung_in_metern()
            
            # Überprüfe, ob die Zielstrecke erreicht wurde
            mittel_distance = ( act_distance_left_m + act_distance_right_m ) / 2
            
            #print("Mittelwert Strecke", mittel_distance)
            #if mittel_distance < 0.05:
                #if self.forward == False:
                    #fc.forward(self.speed)
                #self.forward = True
                #print("start")
            #elif mittel_distance >= self.distance_m - 0.1:
                #if self.forward == False:
                    #fc.forward(10)
                #self.forward = True
                #print("Ziel")
            #else:
                #fc.forward(self.speed)                
                #Funktion zur Überwachung der Distanz, momentan nur zur rechten Wand
            self.check_distance(self.target_distance, self.speed, self.angel)
        
        fc.stop()
        self.ausgabe(mittel_distance, act_distance_left_m, act_distance_right_m)
        self.left_distance_counter.deinit()
        self.right_distance_counter.deinit()

        return True

    def check_distance( self, target_distance, speed, angel ):
        current_distance = fc.get_distance_at( angel )
        #print("Aktueller Abstand: ", current_distance , " Soll: " , target_distance )
        #print("Winkel Sensor" , angel)
        #print("Flag Turn left", self.turn_left)
        #print("Flag Turn right", self.turn_right)
        #print("forward", self.forward)

        
        if angel == -90:

            #if current_distance > target_distance + self.toleranz and current_distance < target_distance + 20:
            if current_distance > self.max_target_distance and not current_distance > target_distance + self.toleranz_max: 
                if  self.turn_right == False: 
                    fc.left_front.set_power( speed )
                    fc.right_front.set_power( speed - self.korrektur_speed)
                    fc.left_rear.set_power( speed )                     
                    fc.right_rear.set_power( speed - self.korrektur_speed)
                self.turn_right = True    
                self.turn_left  = False
                self.forward    = False           
                #print("Abstand zu gross", current_distance)
            #elif current_distance < target_distance - self.toleranz and current_distance > target_distance - 10: 
            elif current_distance < self.min_target_distance and not current_distance < target_distance - self.toleranz_max :    
                if self.turn_left == False:
                    fc.left_front.set_power( speed - self.korrektur_speed) 
                    fc.right_front.set_power( speed )
                    fc.left_rear.set_power( speed - self.korrektur_speed)                    
                    fc.right_rear.set_power( speed )
                self.turn_right = False
                self.turn_left  = True
                self.forward    = False
                #print("Abstand zu klein", current_distance)
            else:
                if self.forward == False:    
                    fc.left_front.set_power( speed) 
                    fc.right_front.set_power( speed )
                    fc.left_rear.set_power( speed )                    
                    fc.right_rear.set_power( speed )
                self.turn_right = False 
                self.turn_left  = False
                self.forward    = True
                #print("Geradeaus")
                #print( current_distance )

        else:
            #if current_distance < target_distance - self.toleranz and current_distance > target_distance - 10: 
            if current_distance < target_distance + self.toleranz: 
                if  self.turn_right == False: 
                    fc.left_front.set_power( speed )
                    fc.right_front.set_power( speed - self.korrektur_speed)
                    fc.left_rear.set_power( speed )                     
                    fc.right_rear.set_power( speed - self.korrektur_speed)
                self.turn_right = True    
                self.turn_left  = False
                self.forward    = False           
                #print("Abstand zu klein")
            #elif current_distance > target_distance + self.toleranz and current_distance < target_distance + 20: 
            elif current_distance > target_distance - self.toleranz  :    
                if self.turn_left == False:
                    fc.left_front.set_power( speed - self.korrektur_speed) 
                    fc.right_front.set_power( speed )
                    fc.left_rear.set_power( speed - self.korrektur_speed)                    
                    fc.right_rear.set_power( speed )
                self.turn_right = False
                self.turn_left  = True
                self.forward    = False
                #print("Abstand zu gross")
                
            else:
                if self.forward == False:    
                    fc.forward(speed)
                self.turn_right = False 
                self.turn_left  = False
                self.forward    = True
                #print("Geradeaus")
        


    def ausgabe(self, mittel_distance, act_distance_left_m, act_distance_right_m):
        print("################################################################################")       
        print(f"Gemessener erster Abstand:       {self.target_distance:.2f}")        
        print(f"Zu fahrende Strecke plus Auto:   {self.distance_m:.2f} m")        
        print(f"Abstand zur Wand nach der Fahrt: {fc.get_distance_at(self.angel):.2f} cm")
        print(f"Mittelwert:                      {mittel_distance:.2f} m")
        print(f"Aktuelle Strecke Links:          {act_distance_left_m:.2f} m")
        print(f"Aktuelle Strecke rechts:         {act_distance_right_m:.2f} m")        
        print("################################################################################\n")

    def akt_distance_wall(self):
        return fc.get_distance_at(self.angel)

