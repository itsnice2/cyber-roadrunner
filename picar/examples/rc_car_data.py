from influxdb import InfluxDBClient
import time
import random

client = InfluxDBClient(host='192.168.1.114', port=8086, username='your_username', password='your_password', database='rc_car')

while True:
    data = [
        {
            "measurement": "car_metrics",
            "tags": {
                "car": "rc1"
            },
            "fields": {
                "speed": random.uniform(0, 100),
                "battery_level": random.uniform(0, 100)
            }
        }
    ]
    client.write_points(data)
    time.sleep(5)
