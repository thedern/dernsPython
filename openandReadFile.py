
#Write a program that prompts for a file name, then opens that file and reads through the file, and print the contents of the file i#n upper case. Use the file words.txt to produce the output below.

# Use words.txt as the file name
#fname = raw_input("Enter file name: ")
#fh = open(fname)


#Note str.capitalize() only caps the first letter in the string.  str.upper() caps the whole string.

test = raw_input('please enter file name ')
fhand = open(test)
    
count = 0

for line in fhand:
        line = line.rstrip()
        print line.upper()

