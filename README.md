# Bachelor Thesis of Christian Schindler - Developer Guid

## Preparations for executing skript

- install and configure [AWS CLI](https://aws.amazon.com/cli/)
- Get data from S3 and store it in ./s3
  - From S3
      ```bash
      aws s3 sync s3://<AWS_BUCKET_NAME>/ s3
      ```
  - Data from archive
    - Setup [Git Large File Storage](https://git-lfs.github.com)
    - extract [s3.tar.gz](s3.tar.gz) 
    ```bash
      tar -xzvf s3.tar.gz
    ```
- Set the following environment variables:
    - `AWS_ACCESS_KEY_ID`
    - `AWS_SECRET_ACCESS_KEY`
    - `AWS_BUCKET_NAME`
    - `PROJECT_DIR`

## Base scripts

- create spot / normal EC2 instance with [aws.py](aws.py)
- create bar chart [plot.py](plot.py)

## Debug execution

- login in to instance
- Check the log of your user data script in:
    - /var/log/cloud-init-output.log

## Tests

### Base tests

Get basic information of systems

- [Results](base_test/data_parsing/instance_info.md)
- [:computer: Python Skript](base_test/main.py)
- [EC2 Bash Skript](base_test/base_test.sh)

### General benchmark

Execute [byte-unixbench](https://github.com/kdlucas/byte-unixbench)

- [Results](general_benchmark/data_parsing)
- [:computer: Python Skript](general_benchmark/main.py)
- [EC2 Bash Skript](general_benchmark/general_benchmark.sh)
- [EC2 Bash Skript Amazon Linux 2](general_benchmark/general_benchmark_a1.sh)
- [EC2 Bash Skript execute 2 times](general_benchmark/general_benchmark_con.sh)

### CPU frequency analyses

CPU frequency

- [Results](cpu_frequency/parse)
- [:computer: Python Skript](cpu_frequency/main.py)
- [EC2 Bash Skript](cpu_frequency/cpu_frequency.sh)
- [EC2 Python Skript](cpu_frequency/cpu_frequency.py)

### CPU frequency scaling

Frequency and Whetstone scaling depending on Threads

- [Results](scaling_benchmark/data_parsing)
- [:computer: Python Skript](scaling_benchmark/main.py)
- [EC2 Bash Skript](scaling_benchmark/scaling_benchmark.sh)
- [EC2 Python Skript](scaling_benchmark/scaling_benchmark.py)

### SIMD performance

Test with Mandelbrot Bench and [SIMD Library Evaluation](https://github.com/felix-ro/SIMD-Library-Evaluation.git)

- [Results](simd/parsing)
- [:computer: Python Skript](simd/main.py)
- [EC2 Bash Skript x86](simd/simd.sh)
- [EC2 Bash Skript ARM](simd/simd_arm.sh)
