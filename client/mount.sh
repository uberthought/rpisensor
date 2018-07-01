#!/bin/bash

source ./data

if [ ! -d ~/$DIRECTORY ]; then
    mkdir ~/$DIRECTORY
fi
sshfs pi@$ADDRESS:. ~/$DIRECTORY
