import sys
import os

POWER_METER_LENGTH = 10

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

def tmux_color(color_name):
    return "#[fg=" + color_name + "]"

def draw_power_meter(time_str, power_level, power_tick, power_tick_minor, power_meter_color):
    major_ticks = POWER_METER_LENGTH * power_level
    major_ticks_draw = int(major_ticks)
    empty_ticks = POWER_METER_LENGTH - major_ticks_draw - 1

    if major_ticks % 1 > 0.5:
        power_tick_minor = power_tick

    power_meter = power_tick * major_ticks_draw
    power_meter += power_tick_minor
    power_meter += " " * empty_ticks
    print "%s [%s%s%s]" % (time_str, power_meter_color, power_meter, tmux_color('default'))

# time string from positive float hours
def get_time_str(hours_float):
    hours_fpart = hours_float % 1
    return "%d:%02d" % (int(hours_float), int(hours_fpart * 60))

try:
    if power_status == "Full":
        on_ac = " AC "
        padding = "=" * ((POWER_METER_LENGTH - len(on_ac))/ 2)
        print "[%s%s%s]" % (padding, on_ac, padding)
        sys.exit(0)

    power_remain = energy_now / energy_full

    if power_status == "Charging":
        hours_remain = (energy_full - energy_now) / power_now
        draw_power_meter("-" + get_time_str(hours_remain), power_remain, ">", "-", tmux_color('blue'))
    elif power_status == "Discharging":
        hours_remain = energy_now / power_now
        if power_remain < 0.1:
            power_meter_color = 'magenta'
        elif power_remain < 0.25:
            power_meter_color = 'red'
        elif power_remain < 0.5:
            power_meter_color = 'yellow'
        else:
            power_meter_color = 'green'
        draw_power_meter(get_time_str(hours_remain), power_remain, "=", "-", tmux_color(power_meter_color))
    else:
        print "[Unknown Power State]"

except Exception as e:
    print "xx:xx [%s]" % ("x" * POWER_METER_LENGTH)
    print e
