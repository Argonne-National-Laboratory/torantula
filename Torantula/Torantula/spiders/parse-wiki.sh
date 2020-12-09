#!/bin/bash
#This script takes in an unformatted list of directory headings, onion sites, etc, and extracts the onion site URLs
cat hiddenwiki.txt | grep onion | /usr/bin/tr -s ' ' | cut -d" " -f1

