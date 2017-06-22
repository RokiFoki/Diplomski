import time
import codecs
import glob
import numpy as np
from radar_graph import plot_chart_plot

types_from_indicator = {
	"collaborative" : "collaborative",	
	"AR" : "AR",
	"player" : "competitive"
}

type_indicators = {
	"collaborative" : "",	
	"AR" : "_AR",
	"competitive" : "_player"
}

results = {}
avaiable_users = set()

for file_name in glob.glob("tmp/users/results/*_real.txt"):
	prefix_index = file_name.rfind("/")+1
	suffix_index = file_name.rfind("_real.txt")

	name, *type_indicator = file_name[prefix_index:suffix_index].split("_")

	type_indicator = type_indicator[0] if len(type_indicator) > 0 else "collaborative"
	type = types_from_indicator[type_indicator]
	
	if " " in name:
		if name not in results:
			results[name] = set()

		results[name].add(type)
		if len(results[name]) == 3:
			avaiable_users.add(name)


types = type_indicators.keys()
for name in avaiable_users:
	grades = []
	for type in type_indicators.keys():
		file_name = "tmp/users/results/{}{}_real.txt".format(name, type_indicators[type])
		with open(file_name, "r") as f:
			grade = np.mean(np.array([float(line.strip().split(":")[1]) for line in f.readlines()]))
		
		grades.append(grade)


	print(name)
	print(grades)
	print()

	plot_chart_plot(
		[grades],
		types,
		['b', 'r', 'g', 'm', 'y'],
		[name]
	)


