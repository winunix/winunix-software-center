if [ ! -f /usr/wx-center/modules/Chrome/google-chrome-stable.deb ]; then
   wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -O /usr/wx-center/modules/Chrome/google-chrome-stable.deb
fi
apt install /usr/wx-center/modules/Chrome/*.deb -y 2>&1 >>/tmp/log$(date '+%Y%m%d.%H%M%S')
