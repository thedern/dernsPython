
# Write code using find() and string slicing (see section 6.10) to extract
# the number at the end of the line below. Convert the extra#cted value to
# a floating point number and print it out.

# text = "X-DSPAM-Confidence:    0.8475";

str = 'X-DSPAM-Confidence: 0.8475'

# find the colon in the string
colo = str.find(':')
# print colo

# slice from one character past the colon to the end of the string
marked = str[colo + 1:]
# print marked

# strip leading white space
formatted = marked.lstrip()
# print formatted
type1 = type(formatted)
# print type1

# convert to floating point number from a string
final = float(formatted)
print final
type2 = type(final)
# print type2
