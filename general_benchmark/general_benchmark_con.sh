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

# install dependence and build UnixBench
dnf install -y -q make gcc perl git
git clone https://github.com/kdlucas/byte-unixbench.git
cp -r byte-unixbench/UnixBench .
rm -rf byte-unixbench
cd UnixBench || exit 4
make

# instal perf
dnf install -y -q perf

# execute UnixBench
perf stat -o "perf.csv" -x -- ./Run
mv perf.csv ../perf1.csv

# execute UnixBench
perf stat -o "perf.csv" -x -- ./Run
mv perf.csv ../perf2.csv

# store UnixBench results and delete rest
cp results/* ..
cd .. || exit 5
rm -rf UnixBench


# save results to S3
cd ~ || exit 6
aws s3 sync "$instance_name" "s3://$s3name/results/2-general_benchmark_con/$instance_name"

# shutdown
shutdown -h now || shutdown
