#!/bin/bash

# Check if two arguments are provided
if [ $# -ne 2 ]; then
  echo "Usage: $0 <instance_name> <s3-name>"
  exit 1
fi

# Assign arguments to variables
instance_name=$1
s3name="$2"
# Create directory and change into it
cd ~ || exit 2
mkdir "$instance_name"
cd "$instance_name" || exit 3

# Store logging
exec > stdout.log 2> stderr.log

# CPU information`s
lscpu > lscpu.data

# get cash and CPU architecture information`s
dnf install -y -q hwloc
lstopo-no-graphics > lstopo.data

# get RAM information`s
dnf install -y -q dmidecode
dmidecode --type 17 >dmidecode.data

# get CPU ?--per-cache
dnf install -y -q perf
perf stat -d -o "perf.json" --per-thread -A -j &
sleep 30 && kill -INT $!
perf stat -o "perf2.json" -j -- sleep 10

# list hardware
dnf install -y -q lshw
lshw -json > lshw.json

# save results to S3
cd ~ || exit 4
aws s3 sync "$instance_name" "s3://$s3name/results/1-base-test/$instance_name"

# shutdown
shutdown -h now || shutdown
