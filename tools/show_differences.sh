#|/usr/bin/env bash
image1=$1 image2=$2 differences=$3
composite $image1 $image2 -compose difference tmp.png
convert tmp.png -auto-level $differences

