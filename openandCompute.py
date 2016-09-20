
# Write a program that prompts for a file name, then opens that file and reads through the file, looking for lines of the form:
# X-DSPAM-Confidence:    0.8475
# Count these lines and extract the floating point values from each of the lines and compute the average of those values and produce an output as shown below.
# You can download the sample data at
# http://www.pythonlearn.com/code/mbox-short.txt when you are testing
# below enter mbox-short.txt as the file name.

# Note str.capitalize() only caps the first letter in the string.
# str.upper() caps the whole string.
# testing


while True:
    try:
        test = raw_input('please enter file name ')
        fhand = open(test)
        break

    except:
        print "the file named '%s' does not exist" % test
        continue

counter = 0
totnum = 0

for line in fhand:
    line = line.rstrip()  # strip the new line or white space off the end

    # use string's find method to look for the substring in quotes
    x = line.find('X-DSPAM-Confidence')

    if x == 0:  # if return code is '0', meaning a match perform the next commands

        y = line.find(' ')  # find the space in the substring
        # slice from 1 character after the space to the end of the string and
        # save
        num = line[y + 1:]
        fnum = float(num)  # convert to float
        # print "fnum is ", fnum
        totnum = totnum + fnum  # keep running total of sums
        # print "totmun + fnum is ", totnum
        counter = counter + 1  # keep running counter


print "total count is: ", counter
print "total number is: ", totnum

ave = totnum / counter
print "Average spam confidence:", ave  # take average
