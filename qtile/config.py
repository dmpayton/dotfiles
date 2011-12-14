#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libqtile.manager import Group, Key, Screen
from libqtile.command import lazy
from libqtile import hook, layout, bar, widget

MOD = 'mod4'
FONT_SIZE = 12
BAR_SIZE = 24

keys = [
    ## Layout, group, and screen modifiers
    Key([MOD], 'j', lazy.layout.up()),
    Key([MOD], 'k', lazy.layout.down()),
    Key([MOD, 'shift'], 'j', lazy.layout.shuffle_up()),
    Key([MOD, 'shift'], 'k', lazy.layout.shuffle_down()),
    Key([MOD, 'shift'], 'g', lazy.layout.grow()),
    Key([MOD, 'shift'], 's', lazy.layout.shrink()),
    Key([MOD, 'shift'], 'n', lazy.layout.normalize()),
    Key([MOD, 'shift'], 'm', lazy.layout.maximize()),
    Key([MOD, 'shift'], 'space', lazy.layout.flip()),

    Key([MOD], 'space', lazy.layout.next()),
    Key([MOD], 'Tab', lazy.nextlayout()),

    Key([MOD, 'shift'], 'space', lazy.layout.rotate()),
    Key([MOD, 'shift'], 'Return', lazy.layout.toggle_split()),

    Key([MOD], 'Left', lazy.group.prevgroup()),
    Key([MOD], 'Right', lazy.group.nextgroup()),

    #Key([MOD], 'h', lazy.to_screen(1)), # left
    #Key([MOD], 'l', lazy.to_screen(0)), # right

    ## Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -q -c 0 sset Master 5dB+')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -q -c 0 sset Master 5dB-')),
    Key([], 'XF86AudioMute', lazy.spawn('amixer -q -c 0 sset Master toggle')),

    ## TODO: What does the printscreen button map to?
    Key([MOD], 'p', lazy.spawn('/usr/bin/gnome-screenshot')),

    ## TODO: hotkey to toggle trackpad
    ## xinput set-prop 15 "Device Enabled" 0
    ## xinput set-prop 15 "Device Enabled" 1

    ## Application launchers
    Key([MOD], 'n', lazy.spawn('/usr/bin/google-chrome')),
    Key([MOD], 'm', lazy.spawn('/usr/bin/audacious')),
    Key([MOD], 'e', lazy.spawn('/usr/bin/nautilus --no-desktop')),
    Key([MOD], 'Return', lazy.spawn('/usr/bin/gnome-terminal')),

    Key([MOD], 'w', lazy.window.kill()),
    Key([MOD], 'r', lazy.spawncmd(prompt=':')),
    Key([MOD, 'control'], 'r', lazy.restart()),
    Key([MOD, 'control'], 'q', lazy.shutdown()),
    Key([MOD, 'control'], 'l', lazy.spawn('/usr/bin/gnome-screensaver-command --lock')),
    Key([MOD, 'control'], 's', lazy.spawn('/usr/bin/sudo /etc/acpi/sleep.sh')),
]

## Next, we specify group names, and use the group name list to generate an appropriate
## set of bindings for group switching.
groups = [Group(str(x)) for x in xrange(1, 10)]
for g in groups:
    keys.append(Key([MOD], g.name, lazy.group[g.name].toscreen()))
    keys.append(Key([MOD, 'shift'], g.name, lazy.window.togroup(g.name)))


layouts = (
    #layout.xmonad.MonadTall(),
    layout.Tile(ratio=0.5),
    layout.Max(),
    #layout.Stack(stacks=2),
    #layout.RatioTile(),
    #layout.RatioTile(fancy=True),
    #layout.RatioTile(ratio=.618),
    #layout.RatioTile(ratio=.618, fancy=True)
    )

floating_layout = layout.floating.Floating(float_rules=[{'wmclass': x} for x in (
    #'audacious',
    'Download',
    'dropbox',
    'file_progress',
    'file-roller',
    'gimp',
    'Komodo_confirm_repl',
    'Komodo_find2',
    'pidgin',
    'skype',
    'Update', # Komodo update window
    'Xephyr',
    )])

screens = [
    Screen(
        top=bar.Bar([
            widget.GroupBox(fontsize=FONT_SIZE, padding=2, borderwidth=3),
            widget.Prompt(fontsize=FONT_SIZE),
            widget.WindowName(fontsize=FONT_SIZE),

            widget.CPUGraph(line_width=1, graph_color='18BAEB', fill_color='1667EB.3', border_width=1, border_color='333333', width=75),
            widget.MemoryGraph(line_width=1, graph_color='00FE81', fill_color='00B25B.3', border_width=1, border_color='333333', width=75),
            widget.SwapGraph(line_width=1, graph_color='5E0101', fill_color='FF5656', border_width=1, border_color='333333', width=75),
            widget.Battery(fontsize=FONT_SIZE, format='{char}{percent:2.0%}', energy_now_file='charge_now', energy_full_file='charge_full', power_now_file='current_now', charge_char='↑ ', discharge_char='↓ '),

            widget.Systray(),
            #widget.Volume(theme_path='/usr/share/icons/Humanity/status/24/'),
            widget.YahooWeather(location='Escondido, CA', metric=False, format='E:{condition_text} {condition_temp}°', fontsize=FONT_SIZE),
            widget.YahooWeather(location='Solana Beach, CA', metric=False, format='SB:{condition_text} {condition_temp}°', fontsize=FONT_SIZE),
            #widget.YahooWeather(location='Fallbrook, CA', metric=False, format='F:{condition_text} {condition_temp}°', fontsize=FONT_SIZE),
            widget.Clock(fmt='%a %d %b %I:%M %p', fontsize=FONT_SIZE),
            ], BAR_SIZE),
    ),
    #Screen(
    #    top=bar.Bar([
    #        widget.GroupBox(fontsize=16),
    #        widget.WindowName(fontsize=16),
    #    ], 35)
    #)
]

@hook.subscribe.client_new
def dialogs(window):
    if window.window.get_wm_type() == 'dialog' \
        or window.window.get_wm_transient_for():
        window.floating = True
    klass = window.window.get_wm_class()
    if klass:
        #open('/home/derek/window-classes', 'a').write('\n%s' % klass[0])
        if klass[0] == 'google-chrome':
            window.togroup('1')
        if klass[0] == 'sublime':
            window.togroup('2')
