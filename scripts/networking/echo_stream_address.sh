#!/bin/bash

#Get the IP address, and time the trailing whitespace
HOST_IP_ADDRESS=$(hostname -I | tr -d ' ')

echo "Visit http://$HOST_IP_ADDRESS:8080 for the stream"
