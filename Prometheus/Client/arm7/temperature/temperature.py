import prometheus_client
import time
import subprocess

UPDATE_PERIOD = 15

temp_cmd = "vcgencmd measure_temp|grep -o -E '[0-9]+\.[0-9]'"
location_cmd = "hostname"
location = subprocess.check_output(location_cmd)



pi_temperature = prometheus_client.Gauge('system_temperature_celsius','temperature of system in degrees celsius',['location'])

if __name__ == '__main__':
    prometheus_client.start_http_server(9999)

while True:
    temperature = subprocess.check_output(temp_cmd, shell=True)
    pi_temperature.labels(location.returned_output.decode("utf-8")).set(temperature.decode("utf-8"))

    time.sleep(UPDATE_PERIOD)
