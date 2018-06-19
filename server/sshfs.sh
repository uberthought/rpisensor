#!/bin/bash

source ./data

if [ ! -d "$DIRECTORY" ]; then
    mkdir ~/server
fi
sshfs uberthought@$ADDRESS:. ~/server
