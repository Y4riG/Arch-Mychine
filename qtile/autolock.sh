xidlehook \
--not-when-fullscreen \
--timer 180 \
    "brightnessctl -s & brightnessctl s 10%" \
    "brightnessctl -r" \
--timer 5 \
    "systemctl suspend" \
    "brightnessctl -r"
