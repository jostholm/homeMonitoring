#!/bin/sh

#create the userinit.sh file to run script commands on motioneyeOS startup
touch /data/etc/userinit.sh

echo "cd /home/ftp/storage/prometheus/node_exporter-1.1.2.linux-armv6/" > /data/etc/userinit.sh
echo "nohup ./node_exporter" >> /data/etc/userinit.sh
