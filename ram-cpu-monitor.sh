#!/bin/sh
loadavg=$(cat /proc/loadavg | awk '{print $1, $2, $3}')
ram=$(free | sed -n '2 p' | awk '{printf("%.0f%% (%.0f%%)", ($3-$6)/$2*100, $7/$2*100)}')
echo "$ram  $loadavg"
