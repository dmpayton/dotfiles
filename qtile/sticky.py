from libqtile import hook, qtile
from libqtile.lazy import lazy

# https://www.reddit.com/r/qtile/comments/ynxnvd/how_to_make_sticky_window/

sticky_windows = []

@lazy.function
def toggle_sticky_windows(qtile, window=None):
    if window is None:
        window = qtile.current_screen.group.current_window
    if window in sticky_windows:
        sticky_windows.remove(window)
    else:
        sticky_windows.append(window)
    return window


@hook.subscribe.setgroup
def move_sticky_windows():
    for window in sticky_windows:
        window.togroup()
    return


@hook.subscribe.client_killed
def remove_sticky_windows(window):
    if window in sticky_windows:
        sticky_windows.remove(window)


@hook.subscribe.client_managed
def auto_sticky_windows(window):
   info = window.info()
   if (info['wm_class'] == ['Toolkit', 'firefox'] and info['name'] == 'Picture-in-Picture'):
       sticky_windows.append(window)
