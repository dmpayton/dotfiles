#!/bin/sh
wmname LG3D
~/.config/qtile/session-startup &
exec ck-launch-session dbus-launch /usr/local/bin/qtile-session
