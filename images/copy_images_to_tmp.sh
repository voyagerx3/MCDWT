set -x
let i=0
for f in *.png
do
    _i_=$(printf "%03d" $i)
    cp $_i_.png /tmp/scale_0_$_i_.png
    ((i++))
done
set +x
