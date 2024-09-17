APS=/Volumes/hd14tb/aps-data/aps-2019-08

files=`ls $APS/ge?/*.ge?`
n=`ls $files | wc -l`
echo ready to remove $n files ...
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || return 
echo removing files
time rm -f $files
