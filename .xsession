#!/bin/sh
wmname LG3D
dbus-launch
~/.config/qtile/session-startup &
exec ck-launch-session /usr/local/bin/qtile-session
