#   ___ _____ ___ _     _____    ____             __ _       
#  / _ \_   _|_ _| |   | ____|  / ___|___  _ __  / _(_) __ _ 
# | | | || |  | || |   |  _|   | |   / _ \| '_ \| |_| |/ _` |
# | |_| || |  | || |___| |___  | |__| (_) | | | |  _| | (_| |
#  \__\_\|_| |___|_____|_____|  \____\___/|_| |_|_| |_|\__, |
#                                                      |___/ 


import os
import re
import socket
import subprocess
import psutil
import json
from libqtile import hook
from libqtile import qtile
from typing import List  
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Backlight
from libqtile.widget.image import Image
from libqtile.dgroups import simple_key_binder
from pathlib import Path
from libqtile.log_utils import logger

#from qtile_extras import widget
#from qtile_extras.widget.decorations import RectDecoration
#from qtile_extras.widget.decorations import PowerLineDecoration


# home
home = str(Path.home())


# default apps
terminal = "kitty"
browser = "opera"       

# --------------------------------------------------------
# Keybindings
# --------------------------------------------------------

mod = "mod4" # SUPER KEY

def go_to_group(qtile, index):
    qtile.current_group.use_layout(index)

keys = [

    # Focus
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window around"),
    
    # Move
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Size
    Key([mod, "control"], "Left", lazy.layout.shrink(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow(), desc="Grow window to the right"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    #colums_layout
    Key([mod, "control"], "Down", lazy.layout.grow_down()),
    Key([mod, "control"], "Up", lazy.layout.grow_up()),
    Key([mod, "control"], "Left", lazy.layout.grow_left()),
    Key([mod, "control"], "Right", lazy.layout.grow_right()),
    Key([mod, "control"], "c", lazy.layout.swap_column_right()),

    # Floating
    Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),
    
    # Split
    #Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Toggle Layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "v", lazy.function(go_to_group, 1), desc="Go to Max Layout"),
    Key([mod], "c", lazy.function(go_to_group, 0), desc="Go to Normal Layout"),

    # Fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen()),

    #System
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod, "shift"], "backspace", lazy.spawn(home + "/.config/rofi/powermenu/powermenu.sh"), desc="Open Powermenu"),
    Key([mod, "control"], "Return", lazy.spawn("rofi -show drun -theme ~/.config/rofi/launcher/style.rasi"), desc="Open AppMenu"),
    Key([mod, 'control'], "k", lazy.spawn(home + "/.config/polybar/launch.sh"), desc="Reload polybar"),

    # Apps
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show drun -theme ~/.config/rofi/launcher/style.rasi")),
    Key([mod], "b", lazy.spawn(browser), desc="Launch Browser"),
    Key([mod, 'shift'], "b", lazy.spawn('firefox'), desc="Launch second Browser"),
    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([mod, "control"], "w", lazy.spawn(home + "/.config/rofi/Wallpapers/wallpaper.sh select"), desc="Select Theme and Wallpaper"),
    Key([mod], "x", lazy.spawn("copyq menu")),
    Key([mod], "l", lazy.spawn(home + "/.config/qtile/lock.sh")),
    Key([], "XF86Calculator", lazy.spawn("gnome-calculator")),
    Key([mod, 'shift'], "c", lazy.spawn('code ' + home + "/.config/qtile/config.py"), desc="Launch config"),

    # Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn("amixer -c 0 sset Master 2+ unmute")),
    Key([], 'XF86AudioLowerVolume', lazy.spawn("amixer -c 0 sset Master 2- unmute")),
    Key([], 'XF86AudioMute', lazy.spawn("amixer -q set Master toggle")), 
    Key([], 'XF86AudioNext', lazy.spawn("playerctl next")),
    Key([], 'XF86AudioPrev', lazy.spawn("playerctl previous")), 
    Key([], 'XF86AudioPlay', lazy.spawn("playerctl play")), 
    Key([], 'XF86AudioStop', lazy.spawn("playerctl pause")), 
    
    #brighness
    Key([], 'XF86MonBrightnessUp', lazy.spawn("brightnessctl s 5%+")),
    Key([], 'XF86MonBrightnessDown', lazy.spawn("brightnessctl s 5%-")),
    Key(["control"], 'XF86MonBrightnessUp', lazy.spawn("brightnessctl s 1%+")),
    Key(["control"], 'XF86MonBrightnessDown', lazy.spawn("brightnessctl s 1%-")),
]

# --------------------------------------------------------
# Groups
# --------------------------------------------------------

groups = [
    Group("1", layout='columns'),
    Group("2", layout='columns'),
    Group("3", layout='columns'),
    Group("4", layout='columns'),
    Group("5", layout='columns'),
]


dgroups_key_binder = simple_key_binder(mod)

# --------------------------------------------------------
# Setup Layout Theme
# --------------------------------------------------------

Clayout_theme = { 
    "border_width": 2,
    "margin": 7,
    #"border_focus": Color2,
    "border_focus": "#3e9396",
    "border_normal": "#2b1e30"
    #"border_normal": "FFFFFF",
     #"single_border_width": 3
}

layout_theme = { 
    "border_width": 1,
    "margin": 7,
    #"border_focus": Color2,
    "border_focus": "#be79db",
    "border_normal": "#2b1e30"
    #"border_normal": "FFFFFF",
     #"single_border_width": 3
}

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layouts = [
    layout.Columns(**Clayout_theme),
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]

# --------------------------------------------------------
# Screens
# --------------------------------------------------------

screens = [
    Screen(),
]

# --------------------------------------------------------
# Drag floating layouts
# --------------------------------------------------------

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Drag([mod, "control"], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod, "shift"], "Button1", lazy.window.keep_above()),
    Click([mod, "control"], "Button1", lazy.window.keep_below()),
]

# --------------------------------------------------------
# Define floating layouts
# --------------------------------------------------------

floating_layout = layout.Floating(
    border_width=0,
    border_focus="#000000",
    border_normal="FFFFFF",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        #Match(wm_class="loupe"),
        Match(wm_class="gnome-calculator"),
        Match(wm_class="gnome-calendar"),
        Match(wm_class="tk"),
        Match(wm_class="com-azefsw-audioconnect-desktop-app-MainKt"),
    ]
)

# --------------------------------------------------------
# General Setup
# --------------------------------------------------------

dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

wmname = "QTILE"


# HOOK startup
@hook.subscribe.startup_once
def autostart():
    autostartscript = "~/.config/qtile/autostart.sh"
    home = os.path.expanduser(autostartscript)
    subprocess.Popen([home])


