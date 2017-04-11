"""

0.5 	1 -> 1,1
0.5 	0 -> 0,1

0.25 	1 -> 1.5,1.5
0.25	0 -> 0,1/1.5 = 0.66

"""

"""

1 -> 2 		(A)
0.5 -> 1 	(B)
0 -> 0.5 	(C)

x -> 0.5 + x

f(x) = ax^2 + bx + c
____________________
f(0)	= (C) 	=> c = (C)
f(0.5) 	= (B) 	=> 0.25a + 0.5b + (C) = (B); 0.25a + 0.5b = (B) - (C); a + 2b = 4((B) - (C))
f(1)	= (A) 	=> a + b + (C) = (A); a + b = (A) - (C)

a + 2b = 4((B)-(C))
a + b = (A) - (C)

b = 4(B) - 4(C) - (A) + (C) = -(A) + 4(B) - 3(C)
a = (A) + (C) +(A) - 4(B) + 3(C) - = 2(A) - 4(B) + 2(C)

a = 4 + -4 - 1 = 1
b = -2 + 4 - 1.5 = 0.5
c = 0.5 
"""

# ovo samo mijenja skale
k = 3

A = 1*k
B = 1
C = 1/k

a = 2*A - 4*B + 2*C
b = -A + 4*B -3*C
c = C

print(a, b, c)

def f(x): return a * x**2 + b*x + c

def calculate_fitness(test):
	test = [[f(t[0]), t[1]] for t in test]

	a, b = 0, 0
	
	for t in test:
	
		if t[1]:
			b += 1 / t[0]
			a += 1 / t[0]
		else:
			b += 1 * t[0] # trebalo bi moći ići u 0!!!!!
			a += 0
	
	#print(a, b)
	return a / b

"""
test1 = [
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
]
print("{}, {}".format("test1", calculate_fitness(test1)))

test2 = [	
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.25, 1],
]
print("{}, {}".format("test2", calculate_fitness(test2)))

test3 = [	
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.25, 0],
]
print("{}, {}".format("test3", calculate_fitness(test3)))

test4 = [	
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 0],
	[0.25, 1],
]
print("{}, {}".format("test4", calculate_fitness(test4)))

test5 = [	
	[0.5, 1],
	[0.25, 1],
	[0.25, 1],
	[0.25, 1],
	[0.25, 1],
]
print("{}, {}".format("test5", calculate_fitness(test5)))

test6 = [	
	[0.5, 0],
	[0.25, 1],
	[0.25, 1],
	[0.25, 1],
	[0.25, 1],
]
print("{}, {}".format("test6", calculate_fitness(test6)))

test7 = [	
	[0.5, 1],
	[0.25, 0],
	[0.25, 1],
	[0.25, 1],
	[0.25, 1],
]
print("{}, {}".format("test7", calculate_fitness(test7)))

"""

test1 = [
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
]
print("{}, {}".format("test1", calculate_fitness(test1)))

test2 = [
	[0.5, 0],
	[0.5, 0],
	[0.5, 0],
	[0.5, 0],
	[0.5, 0],
]
print("{}, {}".format("test2", calculate_fitness(test2)))

test3 = [
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 0],
]
print("{}, {}".format("test3", calculate_fitness(test3)))

test4 = [	
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.75, 0],
]
print("{}, {}".format("test4", calculate_fitness(test4)))

test5 = [	
	[0.5, 1],
	[0.5, 1],
	[0.5, 1],
	[0.5, 0],
	[0.75, 1],
]
print("{}, {}".format("test5", calculate_fitness(test5)))


test6 = [	
	[0.5, 0],
	[0.75, 1],
	[0.75, 1],
	[0.75, 1],
	[0.75, 1],
]
print("{}, {}".format("test6", calculate_fitness(test6)))

test7 = [	
	[0.5, 1],
	[0.75, 0],
	[0.75, 1],
	[0.75, 1],
	[0.75, 1],
]
print("{}, {}".format("test7", calculate_fitness(test7)))