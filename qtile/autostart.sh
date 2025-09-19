#!/bin/bash
#   ___ _____ ___ _     _____   ____  _             _    
#  / _ \_   _|_ _| |   | ____| / ___|| |_ __ _ _ __| |_  
# | | | || |  | || |   |  _|   \___ \| __/ _` | '__| __| 
# | |_| || |  | || |___| |___   ___) | || (_| | |  | |_  
#  \__\_\|_| |___|_____|_____| |____/ \__\__,_|_|   \__| 
#                                                        
# ----------------------------------------------------- 

#Xinput
xinput -set-prop "ELAN06FA:00 04F3:327E Touchpad" "libinput Natural Scrolling Enabled" 1
xinput -set-prop "ELAN06FA:00 04F3:327E Touchpad" "libinput Tapping Enabled" 1

# Keyboard layout
setxkbmap us

# Load picom
picom &

# Setup Wallpaper 
feh --bg-scale ~/wallpaper/best.jpg

#polybar
bash ~/.config/polybar/launch.sh

#clipboard
copyq

#lock after x time. Always at the bottom
bash ~/.config/qtile/autolock.sh

