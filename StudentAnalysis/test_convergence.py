import time
from numpy.random import randint

for iteration in range(1000):

	n = randint(10, 21)
	m = randint(10, 21)

	#print("n", n, "m", m)

	R = randint(-1, 2, [n,m])

	T = [0.5 for i in range(m)]
	O = [0.5 for i in range(n)]
	
	T_L = [2 for i in range(m)]
	O_L = [2 for i in range(n)]

	k = 3
	def fp(x):
		return k**(1-2*x)

	def fr(x):
		return x*x
		
	def ft(x):
		return (x+1)/2
		
	def equal(a, b):
		for i, j in zip(a, b):
			if i - j > 1e-5:
				return False
		
		return True
		
	for l in range(10000):
		for i in range(len(O)):
			brojnik = nazivnik = 0
			for j in range(len(T)):
				brojnik += fr(R[i][j]) * ft(R[i][j]) * fp(T[j])**R[i][j]
				nazivnik += fr(R[i][j]) * fp(T[j])**R[i][j]
				
				#print(i, j, "|", brojnik, nazivnik, "|", fr(R[i][j]) , ft(R[i][j]) , fp(T[j])**R[i][j])
				
				
			O[i] = brojnik / nazivnik
			
		#print("O", O)
				
		for j in range(len(T)):
			brojnik = nazivnik = 0
			for i in range(len(O)):
				brojnik += fr(R[i][j]) * ft(R[i][j]) * fp(O[i])**R[i][j]
				nazivnik += fr(R[i][j]) * fp(O[i])**R[i][j]
				
				
				#print(i, j, brojnik, nazivnik)
				
				
			T[j] = brojnik / nazivnik
			
		#print("T", T)
		
		
		if equal(T_L, T) and equal(O_L, O):
			print(iteration, "Yes")
			break
		else:
			T_L, O_L = list(T), list(O)
	else:
		print(iteration, "No")
		print("R", R)
		print("n", n)
		print("m", m)
		exit()
		
	#print("\nO", O, "\nT", T)