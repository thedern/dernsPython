# Takes a list of hosts via text file and produces the IP addresses
import socket
from sys import argv

script, hostlistFile, hostIPlistFile = argv

if len(argv) == 0:
    # Print useage
    print "useage is scriptname inputfile outputfile"
    exit()
else:
    pass

infile = open(hostlistFile)
outfile = open(hostIPlistFile, 'w')
# truncate to nsure we are creating a fresh file
outfile.truncate()

# create global dictionary
hostIP = dict()


def getIP(hostname):
    global hostIP
    try:
        ipaddr = socket.gethostbyname(hostname)
        # update global dictionary
        hostIP[hostname] = [ipaddr]
    except:
        # clause for typos or non-existant hosts
        print "there is no host ", hostname

for line in infile:
    line = line.rstrip()
    # creates list in the event the infile line has more than hostname
    word = line.split()
    # skips blank lines and passed hostame to getIP
    if len(word) > 0:
        # pass hostname to getIP function
        getIP(word[0])

# write completed dictionary to outfile
# obtain keys from dictionary
keez = hostIP.keys()

# iterate through keys list and print a formatted key/value pair
for i in keez:
    z = "\n %s \t %s" % (i, hostIP[i])
    print z
    outfile.write(z)
