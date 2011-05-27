from libqtile.manager import Group, Key, Screen
from libqtile.command import lazy
from libqtile import hook, layout, bar, widget

mod = 'mod4'

keys = [
    ## Layout, group, and screen modifiers
    Key([mod], 'j', lazy.layout.up()),
    Key([mod], 'k', lazy.layout.down()),

    Key([mod, 'control'], 'j', lazy.layout.shuffle_up()),
    Key([mod, 'control'], 'k', lazy.layout.shuffle_down()),

    Key([mod], 'space', lazy.layout.next()),
    Key([mod], 'Tab', lazy.nextlayout()),

    Key([mod, 'shift'], 'space', lazy.layout.rotate()),
    Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),

    Key([mod], 'Left', lazy.group.prevgroup()),
    Key([mod], 'Right', lazy.group.nextgroup()),

    Key([mod], 'h', lazy.to_screen(1)), # left
    Key([mod], 'l', lazy.to_screen(0)), # right

    ## Application launchers
    Key([mod], 'n', lazy.spawn('/usr/bin/google-chrome')),
    Key([mod], 'm', lazy.spawn('/usr/bin/audacious')),
    Key([mod], 'e', lazy.spawn('/usr/bin/nautilus --no-desktop')),
    Key([mod], 'Return', lazy.spawn('/usr/bin/gnome-terminal')),
    Key([mod], 'y', lazy.spawn('/usr/local/bin/komodo')),

    Key([mod], 'w', lazy.window.kill()),
    Key([mod], 'r', lazy.spawncmd(prompt=':')),
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = [Group(str(x)) for x in xrange(1, 10)]
for g in groups:
    keys.append(Key([mod], g.name, lazy.group[g.name].toscreen()))
    keys.append(Key([mod, 'shift'], g.name, lazy.window.togroup(g.name)))


layouts = (layout.RatioTile(),)

screens = [
    Screen(
        top=bar.Bar([
            widget.GroupBox(fontsize=16),
            widget.Prompt(),
            widget.WindowName(fontsize=16),

            widget.TextBox('cpu', 'cpu', fontsize=16, graph_color='18BAEB', fill_color='1667EB.3'),
            widget.CPUGraph(line_width=1),
            widget.TextBox('mem', 'mem', fontsize=16, graph_color='18BAEB', fill_color='1667EB.3'),
            widget.MemoryGraph(line_width=1),
            widget.TextBox('swp', 'swp', fontsize=16, graph_color='18BAEB', fill_color='1667EB.3'),
            widget.SwapGraph(line_width=1),

            widget.Systray(),
            widget.Volume(theme_path='/usr/share/icons/Humanity/status/24/'),
            #widget.Weather(woeid='2400183', fontsize=16),
            widget.Clock(fmt='%I:%M %p', fontsize=16),
            ], 35),
    ),
    Screen(
        top=bar.Bar([
            widget.GroupBox(fontsize=16),
            widget.WindowName(fontsize=16),
        ], 35)
    )
]

@hook.subscribe.client_new
def dialogs(window):
    if window.window.get_wm_type() == 'dialog' \
        or window.window.get_wm_transient_for():
        window.floating = True
