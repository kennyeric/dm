#!/bin/bash

echo -e "\nThis is a program to find the file in special directory which include keyword!\n\n"

if [ "$1" == "" ]; then
   echo -e "Please input the keyword behind the $0\.\n\n"
    exit 0
fi

keyword=$1

dir=.
if [ "$2" != "" ]; then
    dir=$2
fi

test ! -d $dir && echo -e "The $dir is not exist in your system\.\n\n" && exit 0

count=0
filelist=`ls -R $dir 2> /dev/null | grep -v '^$'`
for filename in $filelist
do
    temp=`echo $filename | sed 's/:.*$//g'`
    if [ "$filename" != "$temp" ]; then
        curdir=$temp
        #echo "current dir = $curdir"
    else
        filetype=`file $curdir/$filename | grep "text"`
        if [ "$filetype" != "" ]; then
            temp=`grep $keyword $curdir/$filename 2> /dev/null`
            #echo $curdir/$filename
            if [ "$temp" != "" ]; then
                echo $curdir/$filename
                count=$(($count+1))
            fi
        fi
    fi
done

