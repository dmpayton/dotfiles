# Color Theme

from libqtile.utils import guess_terminal

from themes import cyberpunk as theme

# Borrowed from @lactua
# https://github.com/lactua/dotfiles/tree/master/source/.config/qtile

#
# General
#

mod = "mod4"
autostart_file = '~/.config/qtile/autostart.sh'
wallpaper_file = '~/Pictures/retrowave-mountains.jpg'
wallpaper_mode = 'fill'

cmd_terminal = guess_terminal()
cmd_file_manager = 'thunar'
cmd_launcher = 'ulauncher'
cmd_screenshot = 'xfce4-screenshooter'
cmd_lock = 'xfce4-screensaver-command --lock'


#
# Layouts
#

layouts_margin = 20
layouts_border_width = 1
layouts_border_color = theme['accent']
layouts_border_focus_color = theme['foreground']
layouts_border_on_single = True


#
# Top bar
#

bar_top_margin = 0
bar_bottom_margin = 21
bar_left_margin = 0
bar_right_margin = 0
bar_size = 48
bar_background_color = theme['background']
bar_foreground_color = theme['foreground']
bar_border_color = theme['disabled']
bar_background_opacity = 1.0
bar_global_opacity = 1.0
bar_font = 'Play'
bar_font_size = 22


#
# Widgets
#

widget_background_y_padding = 5
widget_background_x_padding = 0
widget_background_color = theme['alt_background']
widget_background_opacity = 1.0
widget_background_radius = 19
widget_padding = 10
