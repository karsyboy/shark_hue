#!/bin/bash

LED SETUP
# Set NETMODE to DHCP_CLIENT for Shark Jack v1.1.0+
NETMODE DHCP_CLIENT
# Wait for an IP address to be obtained
while ! ifconfig eth0 | grep "inet addr"; do sleep 1; done
#Starts the Attack
python3 /root/payload/shark_hue.py