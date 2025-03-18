#!/bin/bash
#   ___ _____ ___ _     _____   ____  _             _    
#  / _ \_   _|_ _| |   | ____| / ___|| |_ __ _ _ __| |_  
# | | | || |  | || |   |  _|   \___ \| __/ _` | '__| __| 
# | |_| || |  | || |___| |___   ___) | || (_| | |  | |_  
#  \__\_\|_| |___|_____|_____| |____/ \__\__,_|_|   \__| 
#                                                        
# ----------------------------------------------------- 


#Xinput
xinput set-prop 10 348 1
xinput set-prop 10 319 1
xinput set-prop 10 328 1

# Keyboard layout
setxkbmap us

# Load picom
picom &

# Setup Wallpaper 
feh --bg-scale ~/wallpaper/best.jpg

#polybar
bash ~/.config/polybar/launch.sh

#lock after x time
bash ~/.config/qtile/autolock.sh

#clipboard
copyq