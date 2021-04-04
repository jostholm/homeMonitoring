import prometheus_client
import time

location2 = "<hostName>"


UPDATE_PERIOD = 15

pi_temperature = prometheus_client.Gauge('system_temperature_celsius','temperature of system in degrees celsius',['location'])

if __name__ == '__main__':
  prometheus_client.start_http_server(9999)

while True:
  with open('/home/jostholm/Prometheus/temperature/temp_measure.txt', 'r') as g:
    try:
        temperature = g.readline()
    except:
        temperature = temperature

    pi_temperature.labels(location2).set(temperature)
    time.sleep(UPDATE_PERIOD)
