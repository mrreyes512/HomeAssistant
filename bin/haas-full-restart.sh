#!/bin/bash
docker stop home-assistant
docker rm home-assistant
docker run --restart=always -d --name="home-assistant" -v /usr/local/etc/homeassistant:/config -v /etc/localtime:/etc/localtime:ro -v /home/graeme/home-assistant-backup:/backup --device=/dev/ttyACM0:/zwaveusbstick:rwm  --net=host homeassistant/home-assistant
