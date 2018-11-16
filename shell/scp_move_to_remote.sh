#!/bin/bash

src_user=filesync
src_passwd=@123
src_root=/cmsp/filesync/gg

dst_user=filesync
dst_passwd=@123
dst_ip=10.110.13.188
dst_root=/home/filesync/tt

cd $src_root
flist=`ls *.xml`
sshpass -p $dst_passwd scp $flist $dst_user@$dst_ip:$dst_root
for file in $flist
do
	check=$(sshpass -p $dst_passwd ssh $dst_user@$dst_ip "ls -l $dst_root/$file"|wc -l)
	if (($check == 1))
	then
		echo "move $file success" 
		rm -f $file
	fi
done
