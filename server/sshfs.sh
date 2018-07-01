#!/bin/bash

if [ ! -d "~/$DIRECTORY" ]; then
    mkdir ~/$DIRECTORY
fi
sshfs uberthought@35.232.250.6:. ~/$DIRECTORY
