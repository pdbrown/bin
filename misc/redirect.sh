#!/bin/bash
 
# This script takes a path to an executable and starts it with its stdin connected to a fifo in `cwd`
# Stdout and stderr are written to files in `cwd` respectively
# After running this script, do a 'exec 3> __in' to keep the pipe open after the first command completes

IN=__in
OUT=__out
ERR=__err

if [ -z "$1" ]; then
	echo "Usage: $(basename $0) interpreter"
	exit 1
fi

if [ -e "$IN" ] || [ -e "$OUT" ] || [ -e "$ERR" ]; then
	read -p "Files $IN, $OUT, or $ERR already exist in $(pwd), delete them and continue? [Y] or n? "
	REPLY=${REPLY:-Y}
	REPLY=${REPLY^y}
        if [ "${REPLY:0:1}" != "Y" ]; then
		exit 2
	fi
	rm -f "$IN" "$OUT" "$ERR"
fi

mkfifo "$IN"
"$1" < "$IN" > "$OUT" 2> "$ERR" &
