#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.manager import Drag, Click, Group, Key, Screen
from libqtile.widget import crashme

##-> Commands to spawn
class Commands(object):
    dmenu = 'dmenu_run -i -b -p ">>>" -fn "Open Sans-10" -nb "#000" -nf "#fff" -sb "#15181a" -sf "#fff"'
    lock_screen = 'gnome-screensaver-command -l'
    screenshot = 'scrot screenshot.png'
    trackpad_toggle = "synclient TouchpadOff=$(synclient -l | grep -c 'TouchpadOff.*=.*0')"
    volume_up = 'amixer -q -c 0 sset Master 5dB+'
    volume_down = 'amixer -q -c 0 sset Master 5dB-'
    volume_toggle = 'amixer -q -c 0 sset Master toggle'
    logout = 'gnome-session-quit --logout --no-prompt'
    shutdown = 'gnome-session-quit --power-off'


##-> Theme + widget options
class Theme(object):
    bar = {
        'size': 24,
        'background': '15181a',
        }
    widget = {
        'font': 'Open Sans',
        'fontsize': 11,
        'background': bar['background'],
        'foreground': 'eeeeee',
        }
    graph = {
        'background': '000000',
        'border_width': 0,
        'border_color': '000000',
        'line_width': 1,
        'margin_x': 0,
        'margin_y': 0,
        'width': 50,
        }

    groupbox = widget.copy()
    groupbox.update({
        'padding': 2,
        'borderwidth': 3,
        })

    sep = {
        'background': bar['background'],
        'foreground': '444444',
        'height_percent': 75,
        }

    systray = widget.copy()
    systray.update({
        'icon_size': 16,
        'padding': 3,
        })

    battery = widget.copy()
    #battery.update({
    #    'energy_now_file': 'charge_now',
    #    'energy_full_file': 'charge_full',
    #    'power_now_file': 'current_now',
    #    })

    battery_text = battery.copy()
    battery_text.update({
        'charge_char': '↑ ',
        'discharge_char': '↓ ',
        'format': '{char}{hour:d}:{min:02d}',
        })

    weather = widget.copy()
    weather.update({
        'update_interval': 60,
        'metric': False,
        'format': '{condition_text} {condition_temp}°',
        })


##-> Keybindings
MOD = 'mod4'
keys = [
    ## Window Manager Controls
    Key([MOD, 'control'], 'r', lazy.restart()),
    Key([MOD, 'control'], 'q', lazy.shutdown()),
    #Key([MOD, 'control'], 'q', lazy.spawn(Commands.logout)),

    ## Window Controls
    Key([MOD], 'w', lazy.window.kill()),
    Key([MOD], 'Left', lazy.group.prevgroup()),
    Key([MOD], 'Right', lazy.group.nextgroup()),

    ## Volume Controls
    #Key([], 'XF86AudioRaiseVolume', lazy.spawn(Commands.volume_up)),
    #Key([], 'XF86AudioLowerVolume', lazy.spawn(Commands.volume_down)),
    #Key([], 'XF86AudioMute', lazy.spawn(Commands.volume_toggle)),

    ## Application Launchers
    #Key([MOD], 'r', lazy.spawncmd(prompt=':')),
    Key([MOD], 'space', lazy.spawn(Commands.dmenu)),
    Key([MOD], 'n', lazy.spawn('google-chrome')),
    Key([MOD], 'e', lazy.spawn('nautilus --no-desktop')),
    Key([MOD], 'Return', lazy.spawn('gnome-terminal')),

    ## Layout, group, and screen modifiers
    #Key([MOD], 'j', lazy.layout.up()),
    #Key([MOD], 'k', lazy.layout.down()),
    #Key([MOD, 'shift'], 'j', lazy.layout.shuffle_up()),
    #Key([MOD, 'shift'], 'k', lazy.layout.shuffle_down()),
    #Key([MOD, 'shift'], 'g', lazy.layout.grow()),
    #Key([MOD, 'shift'], 's', lazy.layout.shrink()),
    #Key([MOD, 'shift'], 'n', lazy.layout.normalize()),
    #Key([MOD, 'shift'], 'm', lazy.layout.maximize()),
    #Key([MOD, 'shift'], 'space', lazy.layout.flip()),

    #Key([MOD], 'space', lazy.layout.next()),
    #Key([MOD], 'Tab', lazy.nextlayout()),

    #Key([MOD, 'shift'], 'space', lazy.layout.rotate()),
    #Key([MOD, 'shift'], 'Return', lazy.layout.toggle_split()),

    #Key([MOD], 'h', lazy.to_screen(1)), # left
    #Key([MOD], 'l', lazy.to_screen(0)), # right

    ## TODO: What does the printscreen button map to?
    Key([MOD], 'p', lazy.spawn(Commands.screenshot)),

    ## TODO: hotkey to toggle trackpad
    ## xinput list # get the ID for "Synaptics TouchPad"
    ## xinput set-prop <id> "Device Enabled" 0
    ## xinput set-prop <id> "Device Enabled" 1
    Key([], 'XF86TouchpadToggle', lazy.spawn(Commands.trackpad_toggle)),

    Key([MOD, 'control'], 'l', lazy.spawn(Commands.lock_screen)),
    #Key([MOD, 'control'], 's', lazy.spawn('/usr/bin/gksudo /etc/acpi/sleep.sh')),
]


##-> Groups
group_setup = (
    ('1', {
        'layout': 'max',
        'apps': {'wm_class': ('Firefox', 'Google-chrome')},
        }),
    ('2', {
        'layout': 'max',
        'apps': {'wm_class': ('Komodo Edit',)},
        }),
    ('3', {}),
    ('4', {'layout': 'max',}),
    ('5', {
        'layout': 'max',
        'apps': {'wm_class': ('VirtualBox',)},
        }),
    ('6', {
        'layout': 'max',
        'apps': {'wm_class': ('audacious',)},
        }),
    ('7', {}),
    ('8', {}),
    ('9', {}),
)

groups = []
for idx, (name, config) in enumerate(group_setup):
    hotkey = str(idx + 1)
    groups.append(Group(name, layout=config.get('layout', 'tile')))
    keys.append(Key([MOD], hotkey, lazy.group[name].toscreen()))
    keys.append(Key([MOD, 'shift'], hotkey, lazy.window.togroup(name)))


##-> Mouse
#mouse = (
#    Drag([MOD], 'Button1', lazy.window.set_position_floating(), start=lazy.window.get_position()),
#    Drag([MOD], 'Button3', lazy.window.set_size_floating(), start=lazy.window.get_size()),
#    Click([MOD], 'Button2', lazy.window.bring_to_front())
#)


##-> Screens
screens = [
    Screen(
        top=bar.Bar(widgets=[
            widget.GroupBox(**Theme.groupbox),
            widget.WindowName(**Theme.widget),

            #crashme._CrashMe(),

            widget.CPUGraph(graph_color='18BAEB', fill_color='1667EB.3', **Theme.graph),
            widget.MemoryGraph(graph_color='00FE81', fill_color='00B25B.3', **Theme.graph),
            widget.SwapGraph(graph_color='5E0101', fill_color='FF5656', **Theme.graph),
            widget.NetGraph(graph_color='ffff00', fill_color='4d4d00', interface='wlan0',  **Theme.graph),

            widget.CurrentLayout(**Theme.widget),
            widget.Systray(**Theme.systray),
            #widget.Sep(**Theme.sep),
            widget.BatteryIcon(**Theme.battery),
            widget.Battery(**Theme.battery_text),
            #widget.Sep(**Theme.sep),
            widget.Volume(theme_path='/usr/share/icons/Humanity-Dark/status/24/', **Theme.widget),
            widget.YahooWeather(location='Fresno, CA', **Theme.weather),
            widget.Clock(fmt='%a %d %b %I:%M %p', **Theme.widget),
            ], **Theme.bar),
    ),
    Screen(
        top=bar.Bar([
            widget.GroupBox(**Theme.widget),
            widget.WindowName(**Theme.widget),
            widget.CurrentLayout(**Theme.widget),
        ], **Theme.bar),
    )
]


##-> Layouts
layouts = (
    layout.Tile(ratio=0.5),
    layout.Max(),
    )

##-> Floating windows
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
    #'skype',
    'Update', # Komodo update window
    'Xephyr',
    )])

@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True


##-> Run after Qtile init
def main(qtile):
    from grouper import AppGrouper, Match

    ## Send apps to specified groups on window creation
    AppGrouper(qtile, [{
        'group': name,
        'match': Match(**config['apps']),
        } for name, config in group_setup if 'apps' in config])
