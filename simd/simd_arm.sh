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

# setup
mkfs.ext4  /dev/nvme1n1
mkdir -p /mnt/nvme1n1
mount /dev/nvme1n1 /mnt/nvme1n1
cd /mnt/nvme1n1

dnf install -yq cmake make g++ gtest-devel git meson ninja-build python3-pip

# Google Benchmark
wget https://github.com/google/benchmark/archive/refs/tags/v1.8.3.tar.gz
tar -xvf v1.8.3.tar.gz
rm -f v1.8.3.tar.gz
mv  benchmark-1.8.3 benchmark
cd benchmark
cmake -E make_directory "build"
# Generate build system files with cmake, and download any dependencies.
cmake -E chdir "build" cmake -DBENCHMARK_DOWNLOAD_DEPENDENCIES=on -DCMAKE_BUILD_TYPE=Release ../
# or, starting with CMake 3.13, use a simpler form:
# cmake -DCMAKE_BUILD_TYPE=Release -S . -B "build"
# Build the library.
cmake --build "build" --config Release
cd build
make install

# Google Highway
cd /mnt/nvme1n1/
wget https://github.com/google/highway/archive/refs/tags/1.1.0.tar.gz
tar -xvf 1.1.0.tar.gz
rm -f 1.1.0.tar.gz
mv highway-1.1.0 highway
cd highway
mkdir -p build && cd build
cmake ..
make -j install

# Libsimdpp
cd /mnt/nvme1n1/
git clone https://github.com/p12tic/libsimdpp.git
cd libsimdpp
mkdir -p build && cd build
cmake ..
make install

# PureSimd sktip for ARM
cd /mnt/nvme1n1/
git clone https://github.com/eatingtomatoes/pure_simd.git
cd pure_simd
mkdir -p build && cd build
# setup virtual env
pip install virtualenv
python3 -m venv env
# activate virtual env
source env/bin/activate
pip install conan==1.64.0
echo '[requires]
benchmark/1.5.5
gtest/1.10.0

[generators]
cmake' > ../conanfile.txt
conan install .. --build=benchmark --build=gtest
cmake ..
make install

deactivate

# VC
cd /mnt/nvme1n1/
wget https://github.com/VcDevel/Vc/archive/refs/tags/1.4.4.tar.gz
tar -xvf 1.4.4.tar.gz
rm  -f 1.4.4.tar.gz
mv Vc-1.4.4 Vc
cd Vc
make install

# NSIMD
cd /mnt/nvme1n1/
wget https://github.com/agenium-scale/nsimd/archive/refs/tags/v3.0.1.tar.gz
tar -xvf v3.0.1.tar.gz
rm -f v3.0.1.tar.gz
mv nsimd-3.0.1 nsimd
cd nsimd
mkdir -p build && cd build
cmake ..
make install


# SIMD Everywhere skip ARM
cd /mnt/nvme1n1/
wget https://github.com/simd-everywhere/simde/archive/refs/tags/v0.8.0.tar.gz
tar -xvf v0.8.0.tar.gz
rm -f v0.8.0.tar.gz
mv simde-0.8.0 simde
cd simde
meson build
cd build
ninja install

# main porjecked
cd /mnt/nvme1n1/
git clone https://github.com/felix-ro/SIMD-Library-Evaluation.git
cd SIMD-Library-Evaluation
sed -i '15s/.*/#define BENCHMARK_REPETITIONS 100 /' mandelbrot/mandelbrotBenchmark.cpp


make NEON
mkdir ~/$instance_name/NEON
./mandelBench --benchmark_filter=Scalar > ~/$instance_name/NEON/scalar_100.log
./mandelBench --benchmark_filter=Highway > ~/$instance_name/NEON/highway_100.log

cp ~/$instance_name/NEON/scalar_100.log  ~/$instance_name/scalar_100.log
cp ~/$instance_name/NEON/highway_100.log ~/$instance_name/highway_100.log

make clean
make SVE
mkdir ~/$instance_name/SVE
./mandelBench --benchmark_filter=Scalar > ~/$instance_name/SVE/scalar_100.log
./mandelBench --benchmark_filter=Highway > ~/$instance_name/SVE/highway_100.log

# save results to S3
cd ~
aws s3 sync "$instance_name" "s3://$s3name/results/9-simd/$instance_name"

# shutdown
shutdown -h now || shutdown