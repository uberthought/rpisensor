#!/bin/bash

if [ ! -d "$DIRECTORY" ]; then
    mkdir ~/client
fi
sshfs -p 2222 root@192.168.1.188:. ~/client
