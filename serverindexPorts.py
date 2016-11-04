
import xml.etree.ElementTree as ET
from sys import argv

fhandle = open('/tmp/was_server_ports.txt', 'w')

"""
as wasuser; wasuser2, wasuser3
usage: python ./serverIndexPorts.py <full path to the target serverindex.xml>

This script is written to specifically take the WAS serverindex.xml
and parse the xml root and xml child nodes, 'serverEntries', 'specialEndpoints'
,and 'endPoint' retuning the endpoint names and ports.

"""

try:

    script, input_file = argv
    # formatting
    f1 = '\n'
    f2 = '__'
    f3 = '\n \n'

    # create tree from xml
    tree = ET.parse(input_file)
    root = tree.getroot()

    # create dictionary of root attributes
    test0 = root.attrib
    x = ('\n ********** %s ********** \n \n') % (test0['hostName'])
    print x
    fhandle.write(x)

    # Iterate through child, 'serverEntries' and create attribute dictionary
    for serverEntries in root.iter('serverEntries'):
        test1 = serverEntries.attrib
        print "Application Server Name: ", test1['serverName']
        x = "Application Server Name: %s \n" % (test1['serverName'])
        fhandle.write(x)

        # Iterate through child, 'specialEndpoints' and create attribute
        # dictionary
        for specialEndpoints in serverEntries.iter('specialEndpoints'):
            test2 = specialEndpoints.attrib

            # Iterate through child, 'endPoint' and create attribute dictionary
            for endPoint in specialEndpoints.iter('endPoint'):
                test3 = endPoint.attrib
                print test2['endPointName'], ':', test3['port']
                y = "%s : %s \n" % (test2['endPointName'], test3['port'])
                fhandle.write(y)

        # formatting
        print f1
        print f2 * 50
        print f1

        fhandle.write(f3)

except:
    print "usage: 'program_name' 'path to serverindex.xml'"

fhandle.close()
