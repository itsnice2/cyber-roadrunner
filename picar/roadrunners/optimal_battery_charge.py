"""
VersionsNr:        1.0.1
VersionsDatum:     22.05.2024

VersionsNr:        1.0.0
VersionsDatum:     22.05.2024
Autor:             L.Niebur
Funktion:          Dieses Programm soll das Car so lange laufen lassen bis die optimale Ladung der Batterien 
                   erreicht ist.

Geändert:          L.Niebur 22.05.2024 V 1.0.1
"""
import time
import picar_4wd as fc

def main():
    akt_power = fc.power_read()
    fc.forward(100)
    while akt_power >= 8.3:
        print("\n################################################################################")
        print("Die Aktuelle Ladung des Akkus", akt_power ," Volt")  
        print("################################################################################\n")
        time.sleep(2)
        akt_power = fc.power_read()


    print("\n################################################################################")
    print("Die Ladung ist optimal", akt_power ," Volt")  
    print("################################################################################\n")



if __name__ == "__main__":
    try:
        print("\n################################################################################")
        print("Die Aktuelle Ladung des Akkus", fc.power_read() ," Volt")  
        print("################################################################################\n")
  
        
        

        main()
    finally:
        fc.stop()