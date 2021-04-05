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
    except ValueError:
        print("something went wrong setting temperature " temperature )
    except:
        print("something else went wrong")

    time.sleep(UPDATE_PERIOD)
