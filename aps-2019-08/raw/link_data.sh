APS=/Volumes/hd14tb/aps-data/aps-2019-08

files=`ls $APS/ge?/*_s{3,4}_box*.bz2`
for f in $files; do
    echo uncompressing $f
    bunzip2 $f
    y=${f%.*}
    echo linking uncompressed file: $y
    ln -s $y
done
