"""
VersionsNr:        1.0.0
VersionsDatum:     22.05.2024

VersionsNr:        1.0.0
VersionsDatum:     22.05.2024
Autor:             L.Niebur
Funktion:          Diese Klasse liest Impulse von einem Geber (Encoder) ein,
                   zählt diese und berechnet die aktuelle Geschwindigkeit basierend
                   auf der Anzahl der Impulse und dem Umfang des Rades. Die
                   Geschwindigkeit kann in Metern pro Sekunde abgefragt werden. Die
                   Klasse verwendet Multithreading, um die Impulse kontinuierlich in einem
                   Hintergrundthread zu zählen und die Geschwindigkeit zu berechnen.
"""

import RPi.GPIO as GPIO
import time
import threading
import math

class GeschwindigkeitsZaehler:
    RAD_DM = 6.6  # Raddurchmesser

    def __init__( self, in_pin ):
        self.pin           = in_pin
        self.imp_z         = 0
        self.prev_sig      = False
        self.start_time    = time.time()
        self.timer_flag    = True
        self.speed_m_per_s = 0.0
        self.lock          = threading.Lock()
        self.timer         = threading.Thread( target=self.aktualisiere_geschwindigkeit, name="GeschwindigkeitsThread" )
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

    # Startet den Hintergrundthread zur Geschwindigkeitsmessung
    def starten( self ):
        self.timer.start()
        print( 'Geschwindigkeitsmessung gestartet' )

    # Aktualisiert den Impulszähler bei einer Flanke
    def aktualisiere_impuls( self, akt_sig ):
        if akt_sig and not self.prev_sig:
            self.imp_z += 1
            self.berechne_geschwindigkeit()
        self.prev_sig = akt_sig

    # Berechnet die aktuelle Geschwindigkeit basierend auf den Impulsen
    def berechne_geschwindigkeit( self ):
        umfang = self.RAD_DM * math.pi
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        with self.lock:
            if elapsed_time > 0:
                self.speed_m_per_s = ( self.imp_z / 20.0 ) * umfang / elapsed_time
            self.imp_z = 0
            self.start_time = current_time

    # Kontinuierliche Aktualisierung der Impulse im Hintergrundthread
    def aktualisiere_geschwindigkeit( self) :
        while self.timer_flag:
            akt_sig = GPIO.input( self.pin )
            self.aktualisiere_impuls( akt_sig )
            time.sleep( 0.0008 )

    # Gibt die aktuelle Geschwindigkeit in Metern pro Sekunde zurück
    def geschwindigkeit_in_m_pro_s( self ):
        with self.lock:
            return self.speed_m_per_s

    # Stoppt den Hintergrundthread und bereinigt die GPIOs
    def deinit( self ):
        self.timer_flag = False
        self.timer.join()
        GPIO.cleanup()
        print( 'Geschwindigkeitsmessung gestoppt' )