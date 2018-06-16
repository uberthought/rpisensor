#!/bin/bash

source ./data

DIRECTORY="client"

if [ ! -d $DIRECTORY ]; then
    mkdir ~/$DIRECTORY
fi
sshfs pi@$ADDRESS:. ~/$DIRECTORY
