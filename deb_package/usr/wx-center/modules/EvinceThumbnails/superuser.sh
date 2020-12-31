codeName=$(cat /etc/lsb-release | grep DISTRIB_CODENAME | cut -d'=' -f2)
armorFile="/etc/apparmor.d/usr.bin.evince"
hadWxFixed=$(cat $armorFile | grep "WinuniX")
echo 50
if [ "$hadWxFixed" == "" ]; then
    NUM=$(cat $armorFile | grep 'owner /tmp/evince-thumbnailer\*/{,\*\*} rw,' -n | cut -d':' -f1)
    sed -i $(($NUM + 1))"i\ \ # WinuniX added this line" $armorFile
    if [ "$codeName" == "bionic" ]; then
        sed -i $(($NUM + 2))"i\ \ owner /home/\*/.thumbnails/\*/\*.\* rw," $armorFile
    else
        sed -i $(($NUM + 2))"i\ \ owner /home/\*/.cache/thumbnails/\*/\*.\* rw," $armorFile
    fi
    apparmor_parser -r $armorFile
fi
echo 100
