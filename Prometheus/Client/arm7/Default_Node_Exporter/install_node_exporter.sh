#!/bin/bash

# install
curl -JLO https://github.com/prometheus/node_exporter/releases/download/v1.4.0/node_exporter-1.4.0.linux-armv7.tar.gz
tar xvfz node_exporter-*.tar.gz
rm node_exporter-*.tar.gz
cd node_exporter*armv7 | ./node_exporter
