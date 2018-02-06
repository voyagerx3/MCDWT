set -x
let i=0
for f in *.png
do
    _i_=$(printf "%03d" $i)
    ./add_32768_128.py $_i_.png /tmp/scale_0_L$_i_.png
    ((i++))
done
set +x
