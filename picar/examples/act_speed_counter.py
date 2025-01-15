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
    INTERVAL = 0.1  # Zeitintervall in Sekunden für die Geschwindigkeitsmessung

    def __init__(self, in_pin):
        self.pin = in_pin
        self.imp_z = 0
        self.prev_sig = False
        self.speed_m_per_s = 0.0
        self.lock = threading.Lock()
        self.timer_flag = True
        self.timer = threading.Thread(target=self.messe_geschwindigkeit, name="GeschwindigkeitsThread")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Startet den Hintergrundthread zur Geschwindigkeitsmessung
    def starten(self):
        self.timer.start()
        print('Geschwindigkeitsmessung gestartet')

    # Aktualisiert den Impulszähler bei einer Flanke
    def aktualisiere_impuls(self, akt_sig):
        if akt_sig and not self.prev_sig:
            self.imp_z += 1
        self.prev_sig = akt_sig

    # Misst die Geschwindigkeit basierend auf Impulsen innerhalb eines festen Intervalls
    def messe_geschwindigkeit(self):
        while self.timer_flag:
            start_time = time.time()
            imp_counter = 0

            while time.time() - start_time < self.INTERVAL:
                akt_sig = GPIO.input(self.pin)
                if akt_sig and not self.prev_sig:
                    imp_counter += 1
                self.prev_sig = akt_sig
                time.sleep(0.0001)  # Sehr kurzes Schlafintervall, um die Signalflanken zu erfassen

            umfang = self.RAD_DM * math.pi
            with self.lock:
                self.speed_m_per_s = (imp_counter / 20.0) * umfang / self.INTERVAL

    # Gibt die aktuelle Geschwindigkeit in Metern pro Sekunde zurück
    def geschwindigkeit_in_m_pro_s(self):
        with self.lock:
            return self.speed_m_per_s

    # Stoppt den Hintergrundthread und bereinigt die GPIOs
    def deinit(self):
        self.timer_flag = False
        self.timer.join()
        GPIO.cleanup()
        print('Geschwindigkeitsmessung gestoppt')
