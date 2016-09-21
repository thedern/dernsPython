
"""
Given a string, return a new string made of every other char starting with the first, so "Hello" yields "Hlo".

string_bits('Hello') 'Hlo'
string_bits('Hi') 'H'
string_bits('Heeololeo') 'Hello'
"""

def string_bits(str):
    n = len(str)
    x = 0
    new = ""
    while x < n:
		print str[x]
		x += 2
      #  print str[x]
	
string_bits('Hello')
	
