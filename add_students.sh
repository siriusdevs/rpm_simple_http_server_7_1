#!/bin/bash
for student in `cat 7_1`
do
json=`printf '{"name":"%s"}' $student`
curl -X POST -d $json 127.0.0.1:8001/7_1
done