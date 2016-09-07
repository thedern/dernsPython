try:
        from sys import argv
        script, targetFile, resultFile = argv
        #print "argv[1] %s" % argv[1]

        def findPound(x,y):
                global counter
                #get fist word in list
                test = x[0]
                #test if first character of first word is "#"
                if test[0] != "#":
                        counter += 1
                        #reconstitute a string from the list for formatting purposes
                        regroup = ' '.join(x)
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

