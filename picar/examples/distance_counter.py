"""
VersionsNr:        1.0.1
VersionsDatum:     22.05.2024

VersionsNr:        1.0.0
VersionsDatum:     22.05.2024
Autor:             L.Niebur
Funktion:          Diese Klasse liest Impulse von einem Geber (Encoder) ein,
                   zählt diese und berechnet die zurückgelegte Distanz basierend
                   auf der Anzahl der Impulse und dem Umfang des Rades. Die
                   Distanz kann in Metern abgefragt werden. Die Klasse verwendet
                   Multithreading, um die Impulse kontinuierlich in einem
                   Hintergrundthread zu zählen.

Geändert:          L.Niebur 22.05.2024 V 1.0.1
                   - In der Methode "aktualisiere_distanz()"
                     wurde time.sleep(0.0008) geändert, vorher time.sleep(0.0025)
                     somit positioniert das Car immer gleich egal welche Geschwindigkeit.
"""

import RPi.GPIO as GPIO
import time
import threading
import math

class DistanzZaehler:
    RAD_DM = 6.7  # Raddurchmesser

    def __init__(self, in_pin):
        self.pin        = in_pin
        self.imp_z      = 0
        self.prev_sig   = False
        self.timer_flag = True
        self.dist_cm    = 0.0
        self.lock       = threading.Lock()
        self.timer      = threading.Thread( target=self.aktualisiere_distanz, name="DistanzThread" )
        GPIO.setmode( GPIO.BCM ) 
        GPIO.setup( in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
        
    # Startet den Hintergrundthread zur Impulsmessung
    def starten( self ):
        self.timer.start()

    # Aktualisiert den Impulszähler bei einer Flanke
    def aktualisiere_impuls( self, akt_sig ):
        if akt_sig and not self.prev_sig:
            self.imp_z += 1
            self.berechne_distanz()
        self.prev_sig = akt_sig

    # Berechnet die zurückgelegte Distanz basierend auf den Impulsen
    def berechne_distanz( self ):
        umfang = self.RAD_DM * math.pi
        with self.lock:
            self.dist_cm = ( self.imp_z / 20.0 ) * umfang

    # Kontinuierliche Aktualisierung der Impulse im Hintergrundthread
    def aktualisiere_distanz( self ):
        while self.timer_flag:
            akt_sig = GPIO.input( self.pin )
            self.aktualisiere_impuls( akt_sig )
            time.sleep(0.0001)                                              # V 1.0.1

    # Gibt die zurückgelegte Distanz in Metern zurück
    def entfernung_in_metern( self ):
        with self.lock:
            return self.dist_cm / 100.0                                     # Konvertiert cm in Meter

    # Stoppt den Hintergrundthread und bereinigt die GPIOs
    def deinit( self ):
        self.timer_flag = False
        self.timer.join()
        GPIO.cleanup()