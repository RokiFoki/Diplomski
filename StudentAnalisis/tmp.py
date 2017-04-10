def calculate_fitness(test):
	a, b = 0, 0
	
	for t in test:
	
		if t[1]:
			b += 1 * t[0]
			a += 1 * t[0]
		else:
			b += 1 / t[0]
			a += 0
	
	print(a, b)
	return a / b

test1 = [
	[1, 1],
	[1, 1],
	[1, 1],
	[1, 1],
	[1, 1],
]
print("{}, {}".format("test1", calculate_fitness(test1)))

test2 = [	
	[1, 1],
	[1, 1],
	[1, 1],
	[1, 1],
	[2, 1],
]
print("{}, {}".format("test2", calculate_fitness(test2)))

test3 = [	
	[1, 1],
	[1, 1],
	[1, 1],
	[1, 1],
	[2, 0],
]
print("{}, {}".format("test3", calculate_fitness(test3)))

test4 = [	
	[1, 1],
	[1, 1],
	[1, 1],
	[1, 0],
	[2, 1],
]
print("{}, {}".format("test4", calculate_fitness(test4)))

test5 = [	
	[1, 1],
	[2, 1],
	[2, 1],
	[2, 1],
	[2, 1],
]
print("{}, {}".format("test5", calculate_fitness(test5)))

test6 = [	
	[1, 0],
	[2, 1],
	[2, 1],
	[2, 1],
	[2, 1],
]
print("{}, {}".format("test6", calculate_fitness(test6)))
# riješio teški ali pogriješio nešto banalno


test7 = [	
	[1, 1],
	[2, 0],
	[2, 1],
	[2, 1],
	[2, 1],
]
print("{}, {}".format("test7", calculate_fitness(test7)))





#N, N; 0, 0.5; N,N+0.5
#N-1, N; 2, 2; N+1, N+2