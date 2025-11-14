#!/usr/bin/env python3
import subprocess
import datetime

# -----------------------------------------------------------
# THEME COLORS
# -----------------------------------------------------------

theme = {
    'foreground': '#44D6E3',
    'background': '#0F1B37',
    'alt_background': '#070d1b',
    'disabled': '#982D63',
    'accent': '#E31677',
    'urgent': '#F2C03B',
}

MONTH_COLOR = theme['urgent']
TODAY_COLOR = theme['urgent']
WEEKEND_COLOR = theme['accent']
WEEKDAY_COLOR = theme['foreground']

MONO_FONT = 'Fira Code 16'

# -----------------------------------------------------------
# GET CAL OUTPUT
# -----------------------------------------------------------

cal_raw = subprocess.check_output(['cal'], text=True)
lines = cal_raw.splitlines()

if not lines:
    raise SystemExit(0)

title = lines[0].strip()
grid_lines = lines[1:]

today = datetime.date.today().day

# -----------------------------------------------------------
# FORMAT CALENDAR GRID
# -----------------------------------------------------------

def format_line(line, is_header):
    # 20 char calendar width, fixed columns
    line = line.rstrip('\n').ljust(20)
    cells = [line[i*3:(i+1)*3] for i in range(7)]
    out = []

    for col, cell in enumerate(cells):
        is_weekend = col in (0, 6)
        color = WEEKEND_COLOR if is_weekend else WEEKDAY_COLOR

        raw = cell.strip()

        # empty cell
        if not raw:
            # out.append(f'<span background="{background}">{cell}</span>')
            out.append(cell)
            continue

        # HEADER (Su Mo Tu ...)
        if is_header:
            out.append(
                f'<span foreground="{color}"><b>{cell}</b></span>'
            )
            continue

        # DAY NUMBERS
        if raw.isdigit():
            day = int(raw)

            # Today highlight
            if day == today:
                out.append(
                    f'<b><span foreground="{TODAY_COLOR}">{cell}</span></b>'
                )
            else:
                out.append(
                    f'<span foreground="{color}">{cell}</span>'
                )

        else:
            out.append(cell)

    return ''.join(out).rstrip()

# Build the formatted calendar body
formatted_lines = [
    format_line(line, is_header=(i == 0))
    for i, line in enumerate(grid_lines)
]

body = '\n'.join(formatted_lines)
body = f'<span font_desc="{MONO_FONT}">{body}</span>'

title = f'<span foreground="{MONTH_COLOR}"><big><b>{title}</b></big></span>'

subprocess.run([
    'notify-send',
    '-a', 'qtile-cal',
    '-t', '10000',
    '',
    f'{title}\n{body}',
])
