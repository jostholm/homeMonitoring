import prometheus_client
import time


UPDATE_PERIOD = 15

pi_temperature = prometheus_client.Gauge('system_temperature_celsius','temperature of system in degrees celsius'.['location'])

if __name__ == '__main__':
  prometheus_client.start_http_server(9999)

while True:
  with open('/home/jostholm/Prometheus/temperature/temp_measure.txt', 'r') as g:
    temperature = g.readline()

    pi_temperature.labels('miningPi').set(temperature)
    time.sleep(UPDATE_PERIOD)
