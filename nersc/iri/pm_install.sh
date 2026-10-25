#!/bin/bash
# Test install on Perlmutter (run as a compute job): ORCA 6.0.1 from the user's own archive and
# OpenMPI 4.1.6 built against the system gcc, all under $T/sw. Nothing outside $T is changed.
set -e
T=${T:-$PSCRATCH/zn_nersc_test}
SW=$T/sw; mkdir -p $SW; cd $SW
echo "== $(date '+%F %T') unpacking ORCA on $(hostname)"
[ -x $SW/orca_6_0_1_linux_x86-64_shared_openmpi416/orca ] || tar -xf $T/orca_6_0_1_linux_x86-64_shared_openmpi416.tar.xz
ORCA_DIR=$SW/orca_6_0_1_linux_x86-64_shared_openmpi416
[ -x $ORCA_DIR/orca ] || { echo "orca binary not found"; exit 1; }
echo "== $(date '+%F %T') building OpenMPI 4.1.6"
rm -rf ompi-src && mkdir ompi-src && tar -xzf $T/openmpi-4.1.6.tar.gz -C ompi-src --strip-components=1
( cd ompi-src && CC=gcc CXX=g++ FC=gfortran ./configure --prefix=$SW/openmpi-4.1.6 --without-slurm --without-tm --without-ofi --without-ucx --without-psm2 --with-hwloc=internal --with-libevent=internal --with-pmix=internal && make -j 128 && make install ) > $SW/openmpi-build.log 2>&1 || { echo "OpenMPI build failed"; tail -30 $SW/openmpi-build.log; exit 1; }
echo "== $(date '+%F %T') done: $(ls $SW/openmpi-4.1.6/bin/mpirun) ; gcc $(gcc -dumpversion)"
