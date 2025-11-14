#!/bin/sh
wmname LG3D
dbus-launch
/home/derek/.config/qtile/autostart &
exec qtile start
