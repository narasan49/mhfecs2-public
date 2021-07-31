#!/bin/bash

PASS=nD6gnKFpAeXp
ID=narasan
HOST=m43.coreserver.jp

for file in `\find ./posteq/ -maxdepth 1 -type f`; do
    echo ${file}
    sshpass -p ${PASS} scp ${file} ${ID}@${HOST}:/virtual/narasan/mhfecs2/posteq/
done

for dire in `\find ./posteq/ -maxdepth 1 -mindepth 1 -type d`; do
    if ! [ `echo ${dire} | grep 'migrations'` ]; then
	echo ${dire}
	sshpass -p ${PASS} scp -r ${dire} ${ID}@${HOST}:/virtual/narasan/mhfecs2/posteq/
    fi
done

for file in `\find ./user/ -maxdepth 1 -type f`; do
    echo ${file}
    sshpass -p ${PASS} scp ${file} ${ID}@${HOST}:/virtual/narasan/mhfecs2/user/
done

for dire in `\find ./user/ -maxdepth 1 -mindepth 1 -type d`; do
    if ! [ `echo ${dire} | grep 'migrations'` ]; then
	echo ${dire}
	sshpass -p ${PASS} scp -r ${dire} ${ID}@${HOST}:/virtual/narasan/mhfecs2/user/
    fi
done

sshpass -p ${PASS} scp ./mhfecs2/urls.py ${ID}@${HOST}:/virtual/narasan/mhfecs2/mhfecs2/

sshpass -p ${PASS} scp -r ./static ${ID}@${HOST}:/virtual/narasan/mhfecs2/
