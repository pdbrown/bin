#!/bin/sh
loadavg=$(awk '{print $1, $2, $3}' /proc/loadavg)
ram=$(free | awk '
NR == 2 {total=$2; used_with_cache=$3}
NR == 3 {used=$3}
END {printf("%.0f%% (%.0f%%)", used/total*100, used_with_cache/total*100)}')
echo "$ram  $loadavg"
