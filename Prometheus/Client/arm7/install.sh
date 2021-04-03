#!/bin/bash

# install
wget https://github.com/prometheus/prometheus/releases/download/v2.26.0/prometheus-2.26.0.linux-armv7.tar.gz
tar xvfz node_exporter-*.tar.gz
rm node_exporter-*.tar.gz
cd node_exporter*armv7 | ./node_exporter
