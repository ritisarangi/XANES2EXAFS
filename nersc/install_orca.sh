#!/bin/bash
# Install ORCA 6.0.1 and the OpenMPI 4.1.6 it was built against, on a Perlmutter login node.
#
#   bash XANES2EXAFS/nersc/install_orca.sh <orca_6_0_1_linux_x86-64_shared_openmpi416.tar.xz> <NERSC project>
#
# The ORCA file has to be downloaded by the user from https://orcaforum.kofo.mpg.de (free academic
# registration; the licence does not allow copying another person's copy). Everything goes under
# $HOME/sw; the three settings the run needs are added to ~/.bashrc. Takes about 20 minutes.
set -e
TARBALL=${1:?give the ORCA 6.0.1 .tar.xz file}
PROJECT=${2:?give the NERSC project, e.g. m1234}
SW=$HOME/sw
mkdir -p "$SW"
cd "$SW"

echo "== unpacking ORCA"
tar -xf "$TARBALL"
ORCA_DIR=$(dirname "$(find "$SW" -maxdepth 3 -type f -name orca -perm -u+x | grep orca_6_0_1 | head -1)")
[ -x "$ORCA_DIR/orca" ] || { echo "orca binary not found after unpacking"; exit 1; }
echo "   ORCA in $ORCA_DIR"

MPI_DIR=$SW/openmpi-4.1.6
if [ ! -x "$MPI_DIR/bin/mpirun" ]; then
  echo "== building OpenMPI 4.1.6 (about 15 minutes; logs in $SW/openmpi-build.log)"
  [ -f openmpi-4.1.6.tar.gz ] || wget -q https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.6.tar.gz
  rm -rf openmpi-4.1.6-src && mkdir openmpi-4.1.6-src && tar -xzf openmpi-4.1.6.tar.gz -C openmpi-4.1.6-src --strip-components=1
  ( cd openmpi-4.1.6-src && CC=gcc CXX=g++ FC=gfortran ./configure --prefix="$MPI_DIR" --with-slurm \
      && make -j16 && make install ) > "$SW/openmpi-build.log" 2>&1 || { echo "OpenMPI build failed; see $SW/openmpi-build.log"; exit 1; }
fi
echo "   OpenMPI in $MPI_DIR"

if ! grep -q "XANES2EXAFS run settings" ~/.bashrc 2>/dev/null; then
  cat >> ~/.bashrc <<EOT
# XANES2EXAFS run settings
export ACCOUNT=$PROJECT
export ORCA_DIR=$ORCA_DIR
export MPI_DIR=$MPI_DIR
EOT
fi
echo "== done. Run:  source ~/.bashrc"
