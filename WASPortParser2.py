
import xml.etree.ElementTree as ET
from sys import argv

fhandle = open('WAS.txt', 'w')
try:

    #script, input_file = argv
    #formatting
    x1 = '\n'
    x2 = '\n \n'
    x3 = '__'
    x4 = '**'

    #create tree from xml
    tree = ET.parse('serverindex.xml')
    #tree = ET.parse(input_file)
    root = tree.getroot()

    #create dictionary of root attributes
    test0 = root.attrib
    print x2, x4 * 5, test0['hostName'], x4 * 5
    print x1

    #Iterate through child, 'serverEntries' and create attribute dictionary
    for serverEntries in root.iter('serverEntries'):
        test1 = serverEntries.attrib
        print "Application Server Name: ", test1['serverName']
        x = "Application Server Name: %s \n" % (test1['serverName'])
        fhandle.write(x)

        #Iterate through child, 'specialEndpoints' and create attribute dictionary
        for specialEndpoints in serverEntries.iter('specialEndpoints'):
            test2 = specialEndpoints.attrib 

            #Iterate through child, 'endPoint' and create attribute dictionary
            for endPoint in specialEndpoints.iter('endPoint'):
                test3 = endPoint.attrib
                print test2['endPointName'], ':', test3['port']
                y = "%s : %s \n" % (test2['endPointName'], test3['port'])
                fhandle.write(y)   

        #formatting
        print x1
        print x3 * 50 
        print x1
       
        fhandle.write(x2)

except:
    print "usage: 'program_name' 'path to serverindex.xml'"
