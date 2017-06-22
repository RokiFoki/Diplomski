import time
import codecs
import glob

results = []

for file_name in glob.glob("tmp/users/results/*_real.txt"):
	with open(file_name, "r") as f:
		grades = [float(line.strip().split(":")[1]) for line in f.readlines()]

		points = 0.0
		last = -1.0
		for grade in grades:
			if last < grade:
				points += 1
			elif last > grade:
				points -= 1

			last = grade

		results += [(points, grades, file_name)]


for result in sorted(results):
	print(result)
