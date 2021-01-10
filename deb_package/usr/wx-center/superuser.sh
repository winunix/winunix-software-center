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
    # Autoremove
    apt autoremove -y 2>&1 >>/tmp/log$(date '+%Y%m%d.%H%M%S')
    # Enable Partner
    COMMENTED=$(cat /etc/apt/sources.list | grep "# deb http://archive.canonical.com/ubuntu focal partner" | wc -l)
    if [ "$COMMENTED" == "1" ]; then
        sed -i 's$# deb http://archive.canonical.com/ubuntu focal partner$deb http://archive.canonical.com/ubuntu focal partner$g' /etc/apt/sources.list
    fi
fi
