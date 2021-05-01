#followed instructions from https://leanpub.com/rpcmonitor/read
#remember to install prometheus client <pip install prometheus_client>
#This python script is run by the temp_exporter.service which should also be defined.
import prometheus_client
import time
import subprocess

#Define how often the loop should run, ie, update frequency, the temperature measurement bash command and the bash hostname command.
UPDATE_PERIOD = 15
temp_cmd = "vcgencmd measure_temp|grep -o -E '[0-9]+\.[0-9]'"
location_cmd = "hostname| tr -d '\n'"

#Run the command to retrieve the hostname
location = subprocess.check_output(location_cmd, shell=True)

#define the temperature prometheus Gauge
pi_temperature = prometheus_client.Gauge('system_temperature_celsius','temperature of system in degrees celsius',['location'])


if __name__ == '__main__':
    prometheus_client.start_http_server(9999)

#Loop to keep getting and publishing the temperature and then sleep
while True:
    temperature= subprocess.check_output(temp_cmd, shell=True)
    pi_temperature.labels(location.decode("utf-8")).set(temperature.decode("utf-8"))

    time.sleep(UPDATE_PERIOD)
