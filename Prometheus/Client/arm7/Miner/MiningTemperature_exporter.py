#followed instructions from https://leanpub.com/rpcmonitor/read, rember <pip install prometheus_client>
#Additional resources for mcp 3008: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
# https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/
#This python script is run by the temp_exporter.service which should also be defined.

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import prometheus_client
import time
import subprocess


#sets offset constants
offset = 0.5
milliGrade = 0.01
n=0
#Define how often the loop should run, ie, update frequency, the temperature measurement bash command and the bash hostname command.
UPDATE_PERIOD = 15
temp_cmd = "vcgencmd measure_temp|grep -o -E '[0-9]+\.[0-9]'"
location_cmd = "hostname| tr -d '\n'"

#Run the command to retrieve the hostname
location = subprocess.check_output(location_cmd, shell=True)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0-5
chan=[AnalogIn(mcp, MCP.P0),AnalogIn(mcp, MCP.P1),AnalogIn(mcp, MCP.P2), AnalogIn(mcp, MCP.P3), AnalogIn(mcp, MCP.P4),AnalogIn(mcp, MCP.P5)]

#Map USB slot ID to the order on thhe mcp3008 pins
USB=['USB4','USB3','USB2','USB6','USB7','USB5']


#define the temperature prometheus Gauge
pi_temperature = prometheus_client.Gauge('temperature_system_celsius','temperature of system in degrees celsius',['location'])
asic_temperature=prometheus_client.Gauge('temperature_asic_celsius','temperature of asics in degrees celsius',['location'])

#start prometheus http server on port 9999 if this is run as main
if __name__ == '__main__':
    prometheus_client.start_http_server(9999)

#Loop to keep getting and publishing the temperature and then sleep
while True:
	temperature= subprocess.check_output(temp_cmd, shell=True)
	pi_temperature.labels(location.decode("utf-8")).set(temperature.decode("utf-8"))
    #counter = the amount of channels currently used by mcp3008, (6/8)
	while (n<6):
		print('Temperature Channel',n,': ', (chan[n].voltage-0.5)/0.01)
		temperature2=((chan[0].voltage-0.5)/0.01)
		asic_temperature.labels(USB[n]).set(temperature2)
		n = n+1
	n=0
	time.sleep(UPDATE_PERIOD)
