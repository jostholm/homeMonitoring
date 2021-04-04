#!/bin/bash

while true; do
  vcgencmd measure_temp|grep -o -E '[0-9]+\.[0-9]' > /home/jostholm/Prometheus/temperature/temp_measure.txt
  sleep 10;
done
