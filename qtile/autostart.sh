#!/bin/sh
systemctl --user enable pipewire

sleep 2 &&

xfsettingsd &
dunst &
cbatticon --critical-level 3 --command-critical-level "systemctl suspend" &
nm-applet &
pamac-tray &
xfce4-screensaver &
volumeicon &
