#!/bin/bash

src_user=filesync
src_passwd=@123
src_ip=10.110.13.186
src_root=/cmsp/filesync/gg

dst_user=filesync
dst_passwd=@123
dst_ip=10.110.13.188
dst_root=/home/filesync/tt

cd $dst_root

flist=$(sshpass -p $src_passwd ssh -o StrictHostKeyChecking=no $src_user@$src_ip "cd $src_root && ls *.xml")
echo $flist

for file in $flist
do
	sshpass -p $src_passwd scp $src_user@$src_ip:$src_root/$file .
	check=$(ls -l $file|wc -l)
	if (($check == 1))
	then
		echo "move $file success" 
		sshpass -p $src_passwd ssh $src_user@$src_ip  "rm -f $src_root/$file"
	fi
done
