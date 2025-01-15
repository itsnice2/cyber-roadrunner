import time
import picar_4wd as fc
from roadrunners.distance_counter import DistanzZaehler  # Import der Fahrzeug-Klasse

left_distance_counter  = DistanzZaehler( in_pin=25 )
left_distance_counter.starten()

fc.left_rear.set_power( 100 ) 

time.sleep(5)

fc.stop()

print(left_distance_counter.entfernung_in_metern()) 