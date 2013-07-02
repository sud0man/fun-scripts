#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import sys,os,re

###################################################################################################################
#print color
###################################################################################################################
def print_resgood(text) :
	print ('\033[0;32m' + text + '\033[1;m')

def print_info(text) :
	print ('\033[0;33m' + text + '\033[1;m')


###################################################################################################################
#raw_input color
###################################################################################################################
def raw_input_in(text) :
	res=raw_input ('\033[0;34m' + text + '\033[1;m')
	return res
	


TabCibles=[{
		"name":"Apple Credentials - login/password for locked session without autologon",
		"signature":"|grep -A 4 longname|grep -B 1 -A 2 managedUser",
		},
		{"name":"Apple Credentials - login/password for locked session with autologon",
		"signature":"|grep -B 2 -A 2 'buildin:authenticate,privileged' | grep admin -A 5 | grep UseeTags -B 1",
		},
		{"name":"Apple Credentials - login for locked session after startup",
		"signature":"|sed -ne 's_^.*<string>/Users/\\([^/]\\{1,20\}\\).*$_\\1_p'|sort -u",
		},		
		{"name":"Keychain login - password",
		"signature":"| grep -i 'login.keychain' -A 5 |grep -i 'tries' -A 4 | grep -i 'password' -A 1",
		},
		#{"name":"OpenVPN - passwords of private key",
		#"signature":"| A FAIRE"
		#},
		#{"name":"7Zip - passwords of encrypted files",
		#"signature":"| A FAIRE"
		#},
		{"name":"Mail - credentials",
		"signature":"|grep -A 10 'apple.mail.Account/hostname'"
		},
		{"name":"Mail - credentials (alternative)",
		"signature":"|grep -B 20 'ABMailRecent'"
		},
		{"name":"Mail - credentials (alternative 2)",
		"signature":"|grep -B 20 'ABMPerson'"
		},
		{"name":"Outlook client - domain credentials",
		"signature":"outlook"
		}
		
		 ]



def afficheMenu(cibles):
	i = 1
	print_info("Target :")
	for t in cibles:
		print_info(" %2d: %s" % (i, t["name"]))
		i+=1


def usage():
	print_info("Usage: " + sys.argv[0] + " <RAM File in STRINGS format>\n")
	afficheMenu(TabCibles)
	sys.exit(1)


def search_string(index) :
  print_info("Search credentials : " + TabCibles[index-1]["name"])
  
  if TabCibles[index-1]["signature"] == "outlook" :
  	slash2="\\\\\\"
  	quote='"'
  	domain=raw_input_in("WINDOWS DOMAIN : ")
  	print_info("Found usernames for " + domain + " domain:")
  	#res_domain_user=os.popen("cat " + filename + "|sed -ne 's_^.*(\\{1,20\\}[^/])'").read()
  	#print_resgood(res_domain_user)
  	username=raw_input_in("WINDOWS USERNAME : ")
  	webmail_server=raw_input_in("WEBMAIL SERVER (ex:webmail.domain.com) : ")
  	
  	slash="\\\\\\"
  	TabCibles[index-1]["signature"]="|grep -i \"" + domain + slash + username + "\" -A 2 | grep -i " + webmail_server + " -B 2 -A 2"
  
  print_info("----------------------------")
  res=os.popen('cat ' + filename + TabCibles[index-1]["signature"]).read()
  print_resgood(res)
  print_info("----------------------------")


if len(sys.argv) < 2:
	usage()
else : 
	afficheMenu(TabCibles)
	filename=sys.argv[1]
	index=raw_input_in("Choice (666 for all), q to quit : ")

if index == "q" : exit()

if index=="666" :
	file=open(sys.argv[1],'r')
	i = 1
	for t in TabCibles:
		search_string(i)
		i+=1	

else : 
  index=int(index.rstrip('\n\r'))
  search_string(index)
  exit()
