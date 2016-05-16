#!/bin/bash
# build script
echo $(expr $(cat BUILD) + 1) > BUILD
./makebot.py & disown