import os
import re
import subprocess
import time

from libqtile import bar, hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

from qtile_extras import widget

from sticky import toggle_sticky_windows
from variables import *

#
# HOOKS & FUNCTIONS
#

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([
        os.path.expanduser(autostart_file)
    ])


@lazy.function
def adjust_brightness(qtile, direction):
    '''
        Adjust the brightness by 10% in 1% increments for a nice fade.
    '''
    amount = '+1%' if direction == 1 else '1%-'
    for x in range(10):
        for device in ['nvidia_0', 'intel_backlight']:
            subprocess.run(f'brightnessctl -d {device} set {amount}', shell=True)


#
# DEFAULTS
#

bar_defaults = dict(
    size=bar_size,
    background=bar_background_color + format(int(bar_background_opacity * 255), '02x'),
    border_color=bar_border_color,
    border_width=[0, 0, 1, 0],
    margin=[bar_top_margin, bar_right_margin, bar_bottom_margin - layouts_margin, bar_left_margin],
    opacity=bar_global_opacity
)

layout_defaults = dict(
    border_width=layouts_border_width,
    margin=layouts_margin,
    border_focus=layouts_border_focus_color,
    border_normal=layouts_border_color,
    border_on_single=layouts_border_on_single
)

screen_defaults = dict(
    wallpaper=os.path.expanduser(wallpaper_file),
    wallpaper_mode=wallpaper_mode,
)

widget_background = {
    'colour': widget_background_color + format(int(widget_background_opacity * 255), '02x'),
    'radius': widget_background_radius,
    'filled': True,
    'padding_y': widget_background_y_padding,
    'padding_x': widget_background_x_padding,
    'group': True,
}

widget_defaults = dict(
    font=bar_font,
    foreground=bar_foreground_color,
    fontsize=bar_font_size,
    padding=widget_padding,
)

extension_defaults = widget_defaults.copy()


class Widget(object):
    ''' Container for individual widget style options '''

    clock = dict(
        format='%a %d %b %I:%M %p',
        padding=15,
        decorations=[widget.decorations.RectDecoration(**widget_background)],
        mouse_callbacks={
            'Button1': lambda: os.system('notify-cal.py')
        },
    )

    graph = dict(
        background=bar_background_color,
        border_width=0,
        # border_color='#000000',
        line_width=2,
        margin_x=5,
        margin_y=10,
        type='linefill',
        width=75,
    )

    groupbox = dict(
        active=theme['foreground'],
        inactive=theme['accent'],

        this_screen_border=theme['accent'],
        this_current_screen_border=theme['accent'],
        other_screen_border=theme['disabled'],

        urgent_alert_method='line',
        urgent_text=theme['urgent'],
        urgent_border=theme['urgent'],

        highlight_method='line',
        highlight_color=theme['background'],
        # rounded=True,

        # margin=-1,
        # padding=50,
        borderwidth=3,
        disable_drag=True,
        invert_mouse_wheel=True,
    )

    sep = dict(
        foreground=theme['disabled'],
        height_percent=100,
        padding=10,
    )

    systray = dict(
        icon_size=20,
        padding=5,
    )

#
# KEYBINDINGS
#

keys = [
    # Window Manager Controls
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control', 'shift'], 'q', lazy.shutdown()),
    Key([mod, 'control'], 'q', lazy.spawn(cmd_lock)),

    # Window Controls
    Key([mod], 'w', lazy.window.kill()),
    Key([mod], 'f', lazy.window.toggle_floating()),

    # Move window stack in current layout
    Key([mod, 'shift'], 'Up', lazy.layout.shuffle_up()),
    Key([mod, 'shift'], 'Down', lazy.layout.shuffle_down()),

    # Switch groups
    Key([mod], 'Left', lazy.screen.prev_group()),
    Key([mod], 'Right', lazy.screen.next_group()),

    # Cycle layouts
    Key([mod], 'Up', lazy.next_layout()),
    Key([mod], 'Down', lazy.prev_layout()),

    # Change window focus
    Key([mod], 'Tab', lazy.layout.next()),
    Key([mod, 'shift'], 'Tab', lazy.layout.previous()),

    Key([mod, 'shift'], 's', toggle_sticky_windows()),

    # Switch focus to other screens
    Key([mod, 'shift'], 'Left', lazy.to_screen(0)),
    Key([mod, 'shift'], 'Right', lazy.to_screen(1)),

    # Screen Brightness
    Key([], 'XF86MonBrightnessUp', adjust_brightness(+1)),
    Key([], 'XF86MonBrightnessDown', adjust_brightness(-1)),

    # Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -q sset Master 5%+')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -q sset Master 5%-')),
    Key([], 'XF86AudioMute', lazy.spawn('amixer -q sset Master 1+ toggle')),

    # Toggle Trackpad
    Key([], 'XF86TouchpadToggle', lazy.spawn('xinput-toggle -r "TouchPad"')),

    # Application Launchers
    Key([mod], 'space', lazy.spawn(cmd_launcher)),
    Key([mod], 'e', lazy.spawn(cmd_file_manager)),
    Key([mod], 'Return', lazy.spawn(cmd_terminal)),
    Key([], 'Print', lazy.spawn(cmd_screenshot)),
]

#
# SCREENS
#

screens = [
    Screen(
        top=bar.Bar(widgets=[
            widget.GroupBox(**Widget.groupbox),
            widget.WindowName(padding=15, decorations=[widget.decorations.RectDecoration(**widget_background)]),

            widget.Spacer(length=5),

            widget.CPUGraph(graph_color='#FF5656', fill_color='#4B2A3F', **Widget.graph),
            widget.MemoryGraph(graph_color='#00FE81', fill_color='#0B544A', **Widget.graph),
            widget.SwapGraph(graph_color='#F2C03B', fill_color='#484438', **Widget.graph),
            widget.NetGraph(graph_color='#18BAEB', fill_color='#114364', interface='wlp0s20f3', **Widget.graph),

            widget.CurrentLayoutIcon(scale=.4),
            widget.StatusNotifier(),
            widget.Systray(**Widget.systray),

            widget.Spacer(length=5),

            widget.Clock(**Widget.clock),
        ], **bar_defaults),
        **screen_defaults
    ),
    Screen(
        top=bar.Bar(widgets=[
            widget.GroupBox(**Widget.groupbox),
            widget.WindowName(padding=15, decorations=[widget.decorations.RectDecoration(**widget_background)]),
            widget.CurrentLayoutIcon(scale=.4),
            widget.Clock(**Widget.clock),
        ], **bar_defaults),
        **screen_defaults
    )
]

#
# LAYOUTS
#

layouts = (
    layout.Tile(ratio=0.5, **layout_defaults),
    layout.Max(**layout_defaults),
    layout.RatioTile(**layout_defaults),
    layout.Matrix(**layout_defaults),
    layout.VerticalTile(**layout_defaults),
    # layout.MonadTall(**layout_defaults),
    # layout.Stack(**layout_defaults),
    # layout.Zoomy(**layout_defaults),
)

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules
    ],
    **layout_defaults
)


#
# GROUPS
#

group_setup = (
    ('', {  # fa-internet-explorer
        'layout': 'max',
        'matches': [Match(wm_class=re.compile(r"^(Navigator|firefox|Google\-chrome)$"))],
    }),
    ('', {  # fa-code
        'layout': 'max',
        'matches': [Match(wm_class=(
            'sublime_text', 'Sublime_text',
            'code', 'Code',
        ))],
    }),
    ('', {  # fa-terminal
        'matches': [Match(wm_class=[cmd_terminal])],
    }),
    ('', {  # fa-message-lines
        'layout': 'max',
        'matches': [Match(wm_class=(
            'discord', 'Discord',
            'slack', 'Slack',
            'signal', 'Signal',
            'microsoft teams - preview',
            'Microsoft Teams - Preview'
            'teams-for-linux',
            'Teams-for-linux'
        ))],
    }),
    ('', {  # fa-spotify
        'layout': 'max',
        'matches': [Match(wm_class=(
            'spotify', 'Spotify',
        ))],
    }),
    ('6', {}),  # fa-circle-6
    ('7', {}),  # fa-circle-7
    ('8', {}),  # fa-circle-8
    ('9', {}),  # fa-circle-9
)

groups = []
for idx, (label, config) in enumerate(group_setup):
    hotkey = str(idx + 1)
    config.setdefault('layout', 'tile')
    groups.append(Group(label, **config))

    # mod + hotkey = switch to group
    keys.append(Key([mod], hotkey, lazy.group[label].toscreen()))

    # mod + shift + hotkey = move focused window to group
    keys.append(Key([mod, 'shift'], hotkey, lazy.window.togroup(label)))

#
# MOUSE
#

mouse = (
    Drag([mod], 'Button1',
        lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag([mod], 'Button3',
        lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
)

bring_front_click = True
floats_kept_above = True
