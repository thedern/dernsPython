
import re
fhandle = open('mbox-short.txt')

for line in fhandle:
    line = line.rstrip()
    if re.search('^From:.+@', line):
        print line

# reset file pointer to top of file
fhandle.seek(0)
for line in fhandle:
    line = line.rstrip()
    """
    begins with X and zero or more non-white space characters followed by a
    colon, then a space, followed by 0-9 followed be a decimal point '.' then
    one or more characters Lastly, return only the part after the space as
    indicated by the parentheses(). this 'return only' is a feature of the
    findall method.
    """
    # returns a list
    x = re.findall('^X\S*: ([0-9.]+)', line)
    if len(x) > 0:
        print x
