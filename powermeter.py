import sys
import os

if len(sys.argv) < 2:
    sys.exit("Usage: %s sys_battery_subdir" % sys.argv[0])

try:
    os.chdir('/sys/class/power_supply/%s/' % sys.argv[1])
except OSError:
    sys.exit(1)

with open('power_now', 'r') as f:
    power_now = float(f.read().strip())
with open('energy_now', 'r') as f:
    energy_now = float(f.read().strip())
with open('energy_full', 'r') as f:
    energy_full = float(f.read().strip())
with open('status', 'r') as f:
    power_status = f.read().strip()

tmux_colors = {}
tmux_colors['red'] = '#[fg=red]'
tmux_colors['yellow'] = '#[fg=yellow]'
tmux_colors['green'] = '#[fg=green]'
tmux_colors['blue'] = '#[fg=blue]'
tmux_colors['clear'] = '#[fg=default]'
power_meter_color = tmux_colors['green']

power_meter_length = 10

try:
    remaining = energy_now / energy_full

    if power_status == "Charging":
        power_tick = ">"
        sub_power_tick = ">"
        hours_remain = (energy_full - energy_now) / power_now
        power_meter_color = tmux_colors['blue']
        hours_remain_ipart = -int(hours_remain)
    else:
        power_tick = "="
        sub_power_tick = "-"
        hours_remain = energy_now / power_now
        if remaining < 0.5:
            power_meter_color = tmux_colors['yellow']
        if remaining < 0.25:
            power_meter_color = tmux_colors['red']
        hours_remain_ipart = int(hours_remain)

    hours_remain_fpart = hours_remain % 1
    minutes_of_last_hour = int(hours_remain_fpart * 60)

    power_ticks = int(power_meter_length * remaining)
    empty_ticks = power_meter_length - power_ticks
    if (power_meter_length * remaining) % 1 < 0.5:
        power_ticks -= 1
        sub_power_tick_insert = sub_power_tick
    else:
        sub_power_tick_insert = ''

    power_meter = power_tick * power_ticks
    power_meter += sub_power_tick_insert
    power_meter += " " * empty_ticks
    print "%d:%02d [%s%s%s]" % (hours_remain_ipart, minutes_of_last_hour, power_meter_color, power_meter, tmux_colors['clear'])

except Exception as e:
    print "xx:xx [%s]" % ("x" * power_meter_length)
    print e
