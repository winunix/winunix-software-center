#!/bin/bash

echo 0
cd /usr/wx-center/modules/
ls -1d */ >/tmp/modules.wxcenter
cd -

while read MODULE; do
    if [ "$1/" == "$MODULE" ]; then
        source /usr/wx-center/modules/${MODULE}superuser.sh
        break
    fi
done </tmp/modules.wxcenter

if [ "$1" == "autoremove" ]; then
    apt autoremove -y 2>&1 >>/tmp/log$(date '+%Y%m%d.%H%M%S')
fi
