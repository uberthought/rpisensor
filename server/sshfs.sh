#!/bin/bash

if [ ! -d "$DIRECTORY" ]; then
    mkdir ~/server
fi
sshfs uberthought@35.232.250.6:. ~/server
