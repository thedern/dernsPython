
output = ""
result_decimal = []

def find_remainder1(num):
	global output
	remainder = num % 1
	if remainder == num:
		output += "0"
		output += '.'
	else:
		output += "1"
		output += '.'
		
		
def find_remainder2(num):
	global output
	remainder = num % 2
	if remainder == num:
		output += "0"
		find_remainder1(remainder)
	else:
		output += "1"
		find_remainder1(remainder)
		
def find_remainder4(num):
	global output
	remainder = num % 4
	if remainder == num:
		output += "0"
		find_remainder2(remainder)
	else:
		output += "1"
		find_remainder2(remainder)
		
def find_remainder8(num):
	global output
	remainder = num % 8
	if remainder == num:
		output += "0"
		find_remainder4(remainder)
	else:
		output += "1"
		find_remainder4(remainder)
		
def find_remainder16(num):
	global output
	remainder = num % 16
	if remainder == num:
		output += "0"
		find_remainder8(remainder)
	else:
		output += "1"
		find_remainder8(remainder)
		
def find_remainder32(num):
	global output
	remainder = num % 32
	if remainder == num:
		output += "0"
		find_remainder16(remainder)
	else:
		output += "1"
		find_remainder16(remainder)
		
def find_remainder64(num):
	global output
	remainder = num % 64
	if remainder == num:
		output += "0"
		find_remainder32(remainder)
	else:
		output += "1"
		find_remainder32(remainder)
	
def find_remainder128(num):
	global output
	remainder = num % 128
	if remainder == num:
		output += "0"
		find_remainder64(remainder)
	else:
		output += "1"
		find_remainder64(remainder)
		
		
def map_to_decimal(lst):
    output = 0
    global result_decimal
    
    if lst[0] == '1':
        output += 128
        
    if lst[1] == '1':
        output += 64
        
    if lst[2] == '1':
        output += 32
        
    if lst[3] == '1':
        output += 16
        
    if lst[4] == '1':
        output += 8
        
    if lst[5] == '1':
        output += 4
        
    if lst[6] == '1':
        output += 2
        
    if lst[7] == '1':
        output += 1

    result_decimal.append(output)

def create_bits(item):
    lst = []
    
    for bit in item:
        lst.append(bit)
    map_to_decimal(lst)


#prompt user input
print """This program converts binary IP addresses to decimal, or \n
decimal IP addresses to binary.  Press Enter to continue. """

raw_input()

selection = raw_input("Enter 1 for decimal to binary conversion, \n enter 2 for binary to decimal conversion: ")

if selection == "1":
    decimal = raw_input("Enter decimal IP: ")
	#create list of octets
	octets = decimal.split('.')
	#list comprehension to convert str to int
	octets = [int(i) for i in octets]
	#pass octects into mod division functions
	for i in octets:
		find_remainder128(i)
	#format output
	print "Your binary conversion is: %s" % (output.rstrip('.'))
else:
    binary = raw_input("Enter binary IP: \n for example:  11100000.10000000.00011000.00000100"
    octet = binary.split('.')
    for item in octet:
        create_bits(item)

    print result_decimal



	
