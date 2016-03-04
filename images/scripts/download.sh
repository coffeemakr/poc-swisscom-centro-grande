#!/bin/bash
#
# Download images from bluewin.ch
#
BASE="http://rmsdl.bluewin.ch/pirelli/"
function download {
	local filename="$1"
	local end=$2
	for (( c=0; c<=$end; c = c + 2 ))
	do
		minor=$(printf "%02d" $c)
		wget -c "$BASE$filename$minor.sig"
		wget -c "$BASE$filename$minor.rmt"
	done
}

download Vx226x1_610 0
download Vx226x1_612 4
download Vx226x1_614 6
