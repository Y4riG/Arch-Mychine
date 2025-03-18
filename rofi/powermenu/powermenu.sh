#!/usr/bin/env bash
#  ____                                                    
# |  _ \ _____      _____ _ __ _ __ ___   ___ _ __  _   _  
# | |_) / _ \ \ /\ / / _ \ '__| '_ ` _ \ / _ \ '_ \| | | | 
# |  __/ (_) \ V  V /  __/ |  | | | | | |  __/ | | | |_| | 
# |_|   \___/ \_/\_/ \___|_|  |_| |_| |_|\___|_| |_|\__,_| 
#                                                          
#  
# ----------------------------------------------------- 

# Current Theme
dir="$HOME/.config/rofi/powermenu/"
theme='style'

# CMDs
uptime="`uptime -p | sed -e 's/up //g'`"
host=`hostname`

# Options
shutdown=''
reboot=''
lock=''
suspend=''
logout=''

# Rofi CMD
rofi_cmd() {
	rofi -dmenu \
		-p "Archlinux Mychine" \
		-mesg "Uptime: $uptime" \
		-theme ${dir}/${theme}.rasi
}

# Pass variables to rofi dmenu
run_rofi() {
	echo -e "$shutdown\n$logout\n$reboot\n$lock\n$suspend" | rofi_cmd
}

# Actions
chosen="$(run_rofi)"
case ${chosen} in
    $shutdown)
		systemctl poweroff ;;
	$logout)
		qtile cmd-obj -o cmd -f shutdown ;;
    $reboot)
		systemctl reboot ;;
    $lock)
		qtile cmd-obj -o cmd -f shutdown ;;
    $suspend)
		systemctl suspend
esac


