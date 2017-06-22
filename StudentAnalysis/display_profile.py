import time
import codecs
import glob
import numpy as np
from radar_graph import plot_chart_plot
import argparse
import os

parser = argparse.ArgumentParser(description="calculates and displays student profile")
parser.add_argument('names', metavar="name", help="name of the student", type=str, nargs="+")
				
args = parser.parse_args()

names = args.names

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

types = type_indicators.keys()

grades = []
for name in names:
	student_grades = []
	for type in type_indicators.keys():
		file_name = "tmp/users/results/{}{}_real.txt".format(name, type_indicators[type])
		if os.path.isfile(file_name):
			with open(file_name, "r") as f:
				grade = np.mean(np.array([float(line.strip().split(":")[1]) for line in f.readlines()]))
		else:
			grade = 0

		student_grades.append(grade)

	grades.append(student_grades)

plot_chart_plot(
	grades,
	types,
	['b', 'r', 'g', 'm', 'y'],
	names
)


