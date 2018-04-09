#	Accepts an integer n
#	If n is even, divide by 2
#	If n is odd, multiply by 3 and add 1
#	The goal is to reach a number different from 1


n_g = None

def get_n(n):
	while n is None:
		try:
			n = int(input("Enter a number:  "))
		except ValueError:
			print("Not an integer value...")
	return n

def collatz_conjecture(n):
	maxValue = 0
	n_jumps = []
	length = len(n_jumps)
	while n != 1:

		if n % 2 == 0:
			new_n = n/2
			tense = "even"
			operation = "Divide by 2: "
		else:
			new_n = 3 * n + 1
			if int(new_n) > int(maxValue):
				maxValue = new_n
			tense = "odd"		
			operation = "Multiply by 3 and add 1: "
		n = new_n
		n_jumps.append(n)
		line_1 = 'Jump no. : {}     n = {}, which is {}'.format(length,n,tense)
		line_2 = '{} {}'.format(operation, int(new_n))
		print(line_1)
		print(line_2)
	else:
		return n_jumps, maxValue
	
number = get_n(n_g)

jump_list, highest_num = collatz_conjecture(number)

message = "The operation took {} jumps. The maximum value was {}".format(int(len(jump_list)), highest_num)
print(message)