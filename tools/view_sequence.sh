#!/usr/bin/env bash

sequence="/tmp/???_0_LL.png"

usage() {
    echo $0
    echo "Shows sequence of normalized images"
    echo "  [-i sequence to show ($sequence)]"
    echo "  [-? help]"
}

echo $0: parsing: $@

while getopts "i:?" opt; do
    case ${opt} in
        i)
            sequence="${OPTARG}"
            echo "input =" $sequence
            ;;
        ?)
            usage
            exit 0
            ;;
        \?)
            echo "Invalid option: -${OPTARG}" >&2
            usage
            exit 1
            ;;
        :)
            echo "Option -${OPTARG} requires an argument." >&2
            usage
            exit 1
            ;;
    esac
done

set -x

for i in (
rm -f /tmp/ycc2rgb.png
./ycc2rgb.py -i $image -o /tmp/ycc2rgb.png
display -normalize /tmp/ycc2rgb.png

set +x
