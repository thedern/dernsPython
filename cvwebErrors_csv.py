
import os
import re
import time
import gzip
import datetime
import csv

dt = datetime.datetime.now().strftime("%m/%d/%y")

#capture script start time
start_time = time.time()

#if os.path.isfile('/optware/IBM/WebSphere/V7/AppServer/profiles/cve/logs/server1/SystemOut.log'):
filepath = '/backup/ecomm/sysadm/darren/test12/SystemOut_18.05.23_23.00.00.log.gz'

#initialize objects
counts = dict()
lst = list()
ticker = 0
total = 0

#dictionary funtion
def addDi(d, i):
	d[i] = d.get(i, 0) + 1
	return

#write to csv function
def csvWrite(outputWriter, key, val):
	outputWriter.writerow([key, val])
	return

#create CSV ouput file and writer object
outfile = open('logErrors.csv', 'w')
outputWriter = csv.writer(outfile)
outputWriter.writerow([dt])


"""
open log file and read it line-by-line instead of loading whole file into memory.
search for specific strings and pass to dictionary function
"""

with gzip.open(filepath, 'r') as f:
    for line in f:
	if line.startswith('[') and ' ERROR ' in line:
		#get the java class throwing the error
		words = line.split()
		addDi(counts, words[9])
		#format date, stripping leading '['
		logDate = (words[0][1:])
	elif line.startswith('[') and 'CMN0203E: Command not found' in line:
		addDi(counts, "CMN0203E Command not found")
	elif line.startswith('[') and 'TCPC0004W:' in line:
		addDi(counts, "TCPC0004W TCP EXCEEDED")
	elif line.startswith('[') and 'CMN0409E' and 'javax.transaction.RollbackException' in line:
		addDi(counts, "CMN0409E Rollback Exception")
"""
dump the dictionary to a list and sort it by most errros
as each key/value pair is written to the list, send to csv writer function
"""

for key, val in list(counts.items()):
	csvWrite(outputWriter, key, val)
	lst.append((val, key))

lst.sort(reverse = True)

#close csv file, processing complete.  Print on-screen results
outfile.close()
hashes = "#" * 45
print "\n", hashes, "\nERRORS BY COUNT for SystemOut.log\n", "Log Date:", logDate, "\n", hashes, "\n"
for val, key in lst:
	total +=val	
	print key," ---> ",val
	
print "\nTotal Errors:", total,"\n"

print ("EXECUTION TIME: \n --- %s seconds ---" % (time.time() - start_time))
