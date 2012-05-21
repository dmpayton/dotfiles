#!/bin/bash
export BROWSER=google-chrome
export DE=xfce

#/usr/bin/qiv -x ~/Wallpapers/wooden-noir_shd4n/wn_1440x900.png
/usr/bin/qiv -z ~/Wallpapers/vw-bus.png
/usr/bin/nm-applet &
/usr/bin/dropboxd &
/usr/bin/xscreensaver -no-splash &
/usr/bin/google-chrome &
/usr/local/bin/komodo &
xsetroot -cursor_name left_ptr
exec ck-launch-session dbus-launch qtile-session
#exec ck-launch-session dbus-launch openbox-session
