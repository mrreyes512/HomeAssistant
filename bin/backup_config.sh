#!/bin/bash

HADIRECTORY=/config
DATETIMESTAMP=$(date '+%Y%m%d%H%M%S')
BACKUPDIRECTORY=/backup
FILENAME=home-assistant-config
TAREXCLUDEFILE="/config/etc/backup_exclude.conf"
TAROPTIONS="--warning=no-file-changed --exclude-from=$TAREXCLUDEFILE -czf"
NOTOKEEP=10
TAR=/bin/tar

if [ -d "$HADIRECTORY" ]; then
  cd "$HADIRECTORY"
else
  echo "Home Assistant Directory does not exist"
  exit 1
  touch /backup/notexist.test
fi

if [ ! -d "$BACKUPDIRECTORY" ]; then
  mkdir -p "$BACKUPDIRECTORY"
fi
$TAR $TAROPTIONS ${BACKUPDIRECTORY}/${FILENAME}-${DATETIMESTAMP}.tgz .

cd $BACKUPDIRECTORY
ls -1tr | head -n -10 | xargs -d '\n' rm -f --

exit 0
