#!/bin/bash

#This script isn't complete but pulls all base onion links from hidden wiki and extracts the Onion URIs

curl https://thehiddenwiki.org | egrep -o '(http).*(onion).(")' | sed -e s/"\""/""/g
