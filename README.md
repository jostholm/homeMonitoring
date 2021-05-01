# homeMonitoring
Part of the homeMonitoring project is to keep track of a RaspberryPi that is controlling 6 GekkoScience USB miners and displaying various metrics in Grafana.

 ![Alt text](/Grafana/miningDashexample3.png?raw=true "Example")
 
Metrics are collected through
 1. CG Miner API - Statistics about the miners and the pool
 2. Fibaro Wall Plug - power consumption
 3. Temperature - Analogue Sensors TMP36 TO92 and Internal Raspberry Pi measurements
 
The metrics are read and exported by two separate exporters, the CGMiner_API_exporter.py and MiningTemperature_exporter.py.

Ohh and BTW, this is a total n00b project :)
