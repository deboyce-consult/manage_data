APS=/Volumes/hd14tb/aps-data/aps-2019-08

# files=`ls $APS/ge?/*_s8_box_ff_000105*.bz2`
files=`ls $APS/ge?/*_s{13,14,15,16}_line*.bz2`
for f in $files; do
    echo uncompressing $f
    bunzip2 $f
    y=${f%.*}
    echo linking uncompressed file: $y
    ln -s $y
done
