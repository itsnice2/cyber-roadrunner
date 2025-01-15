import time
import picar_4wd as fc
from roadrunners.distance_counter import DistanzZaehler  # Import der Fahrzeug-Klasse

right_distance_counter  = DistanzZaehler( in_pin=4 )
right_distance_counter.starten()

fc.right_rear.set_power( 100 ) 

time.sleep(5)

fc.stop()

print(right_distance_counter.entfernung_in_metern()) 