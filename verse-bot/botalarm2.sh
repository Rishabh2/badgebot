#!/bin/bash
# Checks if bananahammerbot is active and re-activates if not

running=$(ps -eaf | grep banana | grep python)
[[ $running =~ root[[:space:]]*([0-9]*)[[:space:]]*.* ]] && kill ${BASH_REMATCH[1]}
python3 ~/verse-bot/bananahammerbot.py >> ~/verse-bot/log2 2>&1
