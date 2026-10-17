# XANES2EXAFS

Code for a Zn K-edge XANES/EXAFS dataset built from DFT on CSD Zn model complexes (owner: Riti Sarangi, SSRL). Calculation output lives on the clusters, not in git.

- Running the scan production on NERSC: follow `nersc/README.md` and use `nersc/go.sh` only.
- Running it on ALCF Aurora: follow `aurora/README.md` and use `aurora/go.sh` only.
- On S3DF the scripts default to `SITE=s3df`; cluster settings for each site are in `sites/`.
- Scripts must stay standard-library Python 3.6+ (the S3DF system python).
