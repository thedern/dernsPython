########################################################################
#
#  Darren 9/2/2016
#  Parses httpd.conf printing all settings to screen
#  as well as outfile.
#
#  Useage: `python parseHTTPConf.py <targe conf file> <outputfile>
#  Example: python parseHTTPConf.py httpd.conf outputfile_wcwebqa01.txt
#
########################################################################


print "\n"
print "This program will parse the entered httpd.conf file, stripping all comments, and write all parameters and settings to the output file \n"
print "press [Enter] to continue; press [Ctrl-C] to quit \n"
raw_input()


try:

        from sys import argv
        script, targetFile, resultFile = argv
        #print "argv[1] %s" % argv[1]

        def findPound(x,y):
                global counter

                #get fist word in list
                size = len(x)
                test = x[0]

                if size > 1:
                    #get second word in list and test to see if section header
                    test1 = x[1]
                    if test1 == 'Section':
                        #print formatted section header to output file
                        a = "\n ******* %s %s" % (x[1], x[2])
			print a
                        y.write("\n")
			y.write(a)

                #if first word in list is Virtual host, write blank lines for output file readability
                if test == "<VirtualHost":
			y.write("\n")
                        y.write("\n")

                #test if first character of first word is "#"
                if test[0] != "#":
                        counter += 1
                        #if the fist character of word[0] is not '#', reconstitute the string from the list for formatting purposes
                        regroup = ' '.join(x)
                        #print formatted settings to output file
                        z =  "\n setting %d: %s" % (counter, regroup)
                        print z
                        y.write(z)

        ##MAIN BODY##
        infile = open(argv[1])
        outfile = open(argv[2], 'w')
        outfile.truncate()
        outfile.write(argv[1])
        #set counter to 0 so it can be incremented in the function
        counter = 0

        for line in infile:
                words = line.rstrip()
                words = line.split()
                if len(words) > 0 and words[0] != '#':
                        #if line is not blank and first word is not "#" send to parsing function with outfile handle
                        findPound(words,outfile)
                continue

        outfile.close()

except:
        if len(argv) != 3:
                print "you messed up, useage is <scriptaname> <infilename> <outfilename>"

