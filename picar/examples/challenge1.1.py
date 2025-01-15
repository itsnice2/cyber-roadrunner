import picar_4wd as fc
import time
import sys

# Programm aufrufen mit z.B.: python challenge1.py 100 10 r ###############################
# Argumente der Reihe nach: Geschwindigkeit, Länge der Strecke, Wandseite
speed       = int( sys.argv[1] )
distance    = int( sys.argv[2] )
wandSeite   = str( sys.argv[3] )


##### Variablen für Ultraschallsensors: in welche Richtung zeigen? ########################
rechts = -90
links = 90
vorne = 0
richtung = 0


##### Variablen für die Erkennung einer Start- und Ziellinie ##############################
startLinie = False
zielLinie = False


##### Funktion: Wurde die Ziellinie erreicht? #############################################
def ziellinieErreicht():

    global startLinie
    global zielLinie

    # Wenn Ziellinie nicht erreicht
    if zielLinie == False:
        return False

    # Wenn Ziellinie erreicht
    if zielLinie == True:
        return True

##### Funktion: Strecke fahren #########################################################

def fahreStecke(distance):
    print()

##### Funktion: Abstandskorrektur #########################################################
def abstandHalten(abstand):

    global abstandWand

    
    if (fc.get_distance_at() >=  abstandWand + 0.5 ):
        # Korrektur nach rechts
        fc.turn_right(speed)
    elif (fc.get_distance_at() >=  abstandWand - 0.5 ):
        # Korrektur nach links
        fc.turn_left(speed)


##### SERVO EINSTELLEN ####################################################################

if wandSeite == "r":
    # schwenke den Servo nach rechts
    

    # Versuch 1
    try:
        abstandWand = fc.get_distance_at(rechts)
        richtung = rechts
    except:
        print("Fehler: Abstandsmessung fehlerhaft")
    finally:
        abstandWand = fc.get_distance_at(rechts)
elif wandSeite == "l":
    # schwenke den Servo nach links
    abstandWand = fc.get_distance_at(links)
    richtung = links
elif wandSeite == "v":
    # schwenke den Servo nach vorne
    abstandWand = fc.get_distance_at(vorne)
    richtung = vorne



################################################################################
##### START DES PROGRAMMS ######################################################
################################################################################

# Starte das Fahrzeug / Fahre los
fc.forward(speed)

#print(abstandWand)
#time.sleep(5)

#while ziellinieErreicht == False:
while True:
    try:
        abstandHalten(abstandWand, richtung)
        
    finally:
        fc.stop()

#    print(wandSeite)
#    print(speed)

#    if ziellinieErreicht() == True:
#        # Stoppe das Fahrzeug
#        fc.stop()
#        break
#    
#    #abstandWand()
