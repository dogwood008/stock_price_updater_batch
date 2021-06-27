#!/bin/sh

PATH_TO_PRICES_CSV=kabu.plus/csv/japan-all-stock-prices/daily/
SRC=${MOUNTPOINT}/${PATH_TO_PRICES_CSV}

echo src: ${SRC}
echo dist: ${DIST}
echo dry-run: ${DRYRUN}

rm /var/run/mount.davfs/mnt-kabuplus.pid

# DON'T RUN OVER THE THRESHOLD LIMIT!
rsync \
  ${DRYRUN} \
  --archive \
  --human-readable \
  --verbose \
  --max-size=10M \
  --bwlimit=2048 \
  ${SRC} \
  ${DIST}

rm /var/run/mount.davfs/mnt-kabuplus.pid
time python main.py