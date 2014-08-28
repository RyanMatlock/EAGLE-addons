#!/bin/bash
while IFS=, read name _ hex
do
    convert -size 200x200 xc:white -fill $hex -draw "rectangle 0,0 200,200" \
        swatches/$name.gif
done < $1
