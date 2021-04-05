import prometheus_client
import time
import os

location = os.system("hostname")
UPDATE_PERIOD = 15

pi_temperature = prometheus_client.Gauge('system_temperature_celsius','temperature of system in degrees celsius',['location'])

if __name__ == '__main__':
    prometheus_client.start_http_server(9999)

while True:
    temperature = os.system("vcgencmd measure_temp|grep -o -E '[0-9]+\.[0-9]'")

    try:
        pi_temperature.labels(location).set(temperature)
        print('temperature=' + str(temperature))
        print('hostname=' +location)
    except:
        print('something went wrong with' + str(temperature))

    time.sleep(UPDATE_PERIOD)
