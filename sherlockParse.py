
import string
fhandle = open('SherlockHolmes.txt')
wCounter = dict()
totalWords = 0

def wordCount(x):
    """ create histogram of words and count how many total words """
    global wCounter
    global totalWords
    for w in x:
        totalWords += 1
        wCounter[w] = wCounter.get(w,0) + 1
        
def reverseLookup(d, v):
    """ find the word or 'key' in dictionary that maches the value passed to the function 
        function takes dictionary and value as parameters and returns the key """

    for k in d:
        if d[k] == v:
            return k 

def wordsUsedTimes(d, y):
    """ counts how many times a word was used takes dictionary and a numeric value as parameters """ 
    counter = 0
    for k in d:
        if d[k] == y:
	    counter += 1
    return counter

#Read in book and start parsing it line by line
for line in fhandle:
    #remove whitespace, etc
    line = line.rstrip()
    #remove punctuation
    line = line.translate(None, string.punctuation)
    line = line.lower()
    x = len(line)
    if x > 0:
        words = line.split()
        #print words
        wordCount(words)

#get dictionary keys
keez = wCounter.keys()
keez.sort()
unique = len(keez)

#get dictionary values
vals = wCounter.values()
vals.sort()

highVal = vals[-1]
secondHighVal = vals[-2]
mostUsed = reverseLookup(wCounter, highVal)
secmostUsed = reverseLookup(wCounter, secondHighVal)

t = wordsUsedTimes(wCounter, 1)

print "total words ", totalWords
print "total unique words ", unique
print "the word %r was the most used at %d times" % (mostUsed, highVal) 
print "the word %r was the 2nd most used at %d times" % (secmostUsed, secondHighVal) 
print "the number of words used 1 time %r" % t
