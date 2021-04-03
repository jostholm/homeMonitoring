#!/bin/bash

# install
curl -LJO https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.linux-armv6.tar.gz
tar xvfz node_exporter-*.tar.gz
rm node_exporter-*.tar.gz
cd node_exporter*armv6 | ./node_exporter
