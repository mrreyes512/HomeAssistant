#!/bin/bash

NAME="home-assistant"

########## header(text, colour) - echo text in colour, if colour is not set use red
#
# 0 - Black, 1 - Red, 2 - Green, 3 - Yellow, 4 - Blue, 5 - Magenta,
# 6 - Cyan,  7 - White
#
##########

header() {
  if [ -z "$2" ]; then
    echo -e "$(tput setaf 1)$1$(tput sgr 0)"
  else
    echo -e "$(tput setaf $2)$1$(tput sgr 0)"
  fi
}

##########

DOCKER=`which docker-compose`

header "Bringing Up Home Assistant Container" 6
header "--------------------------------" 6
printf "\n"
if which docker >/dev/null; then
  header "Found Docker" 6
  DOCKER=`which docker-compose`
else
  header "Docker not found. Exiting..." 1
  exit 1
fi

header "Starting docker container..." 6

if $DOCKER up -d; then
  header "started docker container." 2
else
  header "Failed to start docker container." 1
  exit 1
fi

exit 0