import prometheus_client
import time
import subprocess

UPDATE_PERIOD = 15

temp_cmd = "vcgencmd measure_temp|grep -o -E '[0-9]+\.[0-9]'"
location_cmd = "hostname"
location = subprocess.check_output(location_cmd)
location = location.returned_output.decode("utf-8")


pi_temperature = prometheus_client.Gauge('system_temperature_celsius','temperature of system in degrees celsius',['location'])

if __name__ == '__main__':
    prometheus_client.start_http_server(9999)

while True:
    temperature = subprocess.check_output(temp_cmd, shell=True)
    temperature = temperature.decode("utf-8")

    pi_temperature.labels(location).set(temperature)

    time.sleep(UPDATE_PERIOD)
