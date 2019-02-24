import subprocess
import shlex
import re
import json
from subprocess import Popen, PIPE

def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line

if __name__ == "__main__":

    pair = []
    with open('export.json') as json_file:
         export = json.load(json_file)

    for path in run("tail -f /var/log/quagga/r2.log"):
        #print path
	if "rcvd" in path:
	   #print path

	   if "UPDATE" in path:
	      asn=path.split()
	      #print asn[-1]
	      pair.append('AS'+asn[-1])
	   else:
	      prefix=path.split()
	      #print prefix[-1]
	      pair.append(prefix[-1])
	
	#print len(pair)
	if len(pair) == 2:
	   print (" ")
	   print ("===========================================================================")
	   print (" ")
	   print ("Receive ASN and Prefix for %s" %pair)
	   print (" ")
	   print ("===========================================================================")
	   print (" ")
	   #print pair
	   #print (pair[0])
	   #print (pair[1])

	   for p in export['roas']:
    	   if p['asn'] == pair[0] and p['prefix'] == pair[1]:
          	   	#print ('ASN: '+ p['asn'])
          	   	#print ('Prefix: ' + p['prefix'])
          		print ('ROA State: valid')
		   	   	print (" ")
		   		print ("===========================================================================")
		   		print (" ")
		   		print ("Action : None")
		   		print (" ")
		   		print ("===========================================================================")
		   		print (" ")
		   		print ("BGP Router Template")
		   		print (" ")
		   		print ("===========================================================================")
		   		print (" ")
		   		print (" ")
		   		print (" ")
		   		print ("===========================================================================")
		   		print (" ")
			else:
		   		continue

	   	with open("data.txt", "r") as fileHandler:
    	 	line = fileHandler.readline() 
  	   
		while line:
       		   #print(line.strip())
       		   line = fileHandler.readline()
       		   if pair[0] and pair[1] in line:
        	      	#print (line)		
          	   	print ('ROA State: Invalid')
		   		print (" ")
		   		print ("===========================================================================")
		   		print (" ")
		   		print ("Action : Change Local Preference")
		   		print (" ")
		   		print ("===========================================================================")
		   		print (" ")
		   		print ("BGP Router Template")
		   		print (" ")
		   		print ("===========================================================================")
		   		print ("!")
				print ("!")
		   		print ("ip prefix-list INVALID-ROAs permit %s" %pair[1])
				print ("!")
				print ("route-map CHANGE_LOCAL_PREF permit 10")
				print (" match ip address prefix-list INVALID-ROAs")
 				print (" set local-preference 200")
		   		print ("!")
				print ("!")
		   		print ("===========================================================================")
		   		print (" ")
		      	break
		   else:
		      	continue

	   print ('ROA State: Unknown')
	   print (" ")
	   print ("===========================================================================")
	   print (" ")
	   print ("Action : Block the Prefix")
	   print (" ")
	   print ("===========================================================================")
	   print (" ")
	   print ("BGP Router Template")
	   print (" ")
	   print ("===========================================================================")
	   print ("!")
	   print ("!")
	   print ("ip prefix-list DENY-UNKNOWN-ROAs deny %s" %pair[1])
	   print ("!")
	   print ("!")
	   print ("===========================================================================")
	   print (" ")


	   pair = []