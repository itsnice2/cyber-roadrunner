import socket
import inputs
import requests

# Konfigurationsparameter
RASPBERRY_PI_IP = '192.168.5.194'  # IP-Adresse Ihres Raspberry Pi
PORT = 5000

# Funktionen zum Senden der Steuerbefehle
def send_command(command):
    url = f'http://{RASPBERRY_PI_IP}:{PORT}/control'
    data = {'command': command}
    response = requests.post(url, data=data)
    print(response.text)

# Hauptschleife zum Lesen der Gamepad-Eingaben
while True:
    events = inputs.get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)  # Debugging-Zeile
        if event.ev_type == 'Key':
            if event.code == 'BTN_NORTH' and event.state == 1:
                print("Vorwärts")
                send_command('forward')
            elif event.code == 'BTN_SOUTH' and event.state == 1:
                print("Rückwärts")
                send_command('backward')
            elif event.code == 'BTN_WEST' and event.state == 1:
                print("Links")
                send_command('left')
            elif event.code == 'BTN_EAST' and event.state == 1:
                print("Rechts")
                send_command('right')
            elif event.code == 'BTN_TL' and event.state == 1:  # Beispiel: BTN_TR
                print("Stop")
                send_command('stop')

