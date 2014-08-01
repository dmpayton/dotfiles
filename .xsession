#!/bin/sh
wmname LG3D
dbus-launch
/home/derek/.config/qtile/session-startup &
exec /usr/bin/qtile-session
#exec ck-launch-session /home/derek/dev/qtile/bin/qtile-session
