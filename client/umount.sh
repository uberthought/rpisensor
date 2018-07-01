#!/bin/bash

source ./data

if [ -d ~/$DIRECTORY ]; then
    fusermount -u ~/$DIRECTORY
fi
