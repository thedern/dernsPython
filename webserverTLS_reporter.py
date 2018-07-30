#!/usr/bin/python

#RUNS AGAINST WEB SERVER AND DUMPS ALL SSL CONFIGS FOR ALL VHOSTS

import subprocess
import csv
import socket
import os

#get hostname and create filenames
hostName = socket.gethostname()
csvFile = hostName + ".csv"
outFile = hostName + ".txt"

#create csv file and filewriter object
csvHandle = open(csvFile, 'w')
outputWriter = csv.writer(csvHandle)

#dump ssl configs per web server virtual host
wHandle = open(outFile,'w')
if os.path.isfile("/optware/IBM/HTTPServer/V8/bin/apachectl.WCS") == True:
	cmd1 = ["/optware/IBM/HTTPServer/V8/bin/apachectl.WCS","-t","-DDUMP_SSL_CONFIG"]

elif os.path.isfile("/optware/IBM/SIF71/HTTPServer/bin/apachectl") == True:
	cmd1 = ["/optware/IBM/SIF71/HTTPServer/bin/apachectl","-t","-DDUMP_SSL_CONFIG"]

else:
	cmd1 = ["/optware/IBM/HTTPServer/V8/bin/apachectl","-t","-DDUMP_SSL_CONFIG"]

#execute dump command on host
subprocess.call(cmd1, stdout=wHandle)
wHandle.close()

#create csv file from dump command output
#note the csv writer requires a list object
rHandle = open(outFile, 'r')
for line in rHandle:
	line = line.rstrip()
        line = line.split(':')
	#filter unwanted parameters
	if line[0] == "FIPS enabled" or line[0] == "Keyfile" or line[0] == "":	
		continue
	elif line[0] == "SSL server defined at":
		#addtional formatting for each vhost block
		outputWriter.writerow([])
		outputWriter.writerow(['Virtual Host Block'])
		#write data
		outputWriter.writerow(line)
	elif line[0] == "Server name":
                #wite list indexes 0, 1 to csv, omitting other indexes
                outputWriter.writerow(line[:2])
	else:
		outputWriter.writerow(line)

rHandle.close()
#remove the text file
subprocess.call(['rm', outFile])


