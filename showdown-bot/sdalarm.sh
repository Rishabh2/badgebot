#!/bin/bash
# Checks if showdownbot is active and re-activates if not

running=$(ps -eaf | grep showdown)
if [[ $running != *"showdown.py"* ]]; then
  python3 ~/showdown-bot/showdown.py
fi
