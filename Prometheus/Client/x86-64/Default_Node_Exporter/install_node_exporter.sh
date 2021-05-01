#!/bin/bash

# install
curl -JLO https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.linux-amd64.tar.gz
tar xvfz node_exporter-*.tar.gz
rm node_exporter-*.tar.gz
cd node_exporter*amd64 | ./node_exporter
