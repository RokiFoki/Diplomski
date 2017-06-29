import time
import codecs
import glob
import numpy as np
from radar_graph import plot_chart_plot
from utils import get_value_from_file
import argparse
import os
import pymssql

parser = argparse.ArgumentParser(description="calculates, displays student profile and updates database with result")
parser.add_argument('names', metavar="name", help="name of the student", type=str, nargs="+")
parser.add_argument('-ip', help="IP address of the database", default="161.53.18.12", type=str)
parser.add_argument('-port', help="PORT of the database", default=1955, type=int)
parser.add_argument('-db', help="Database name", default="ExperientialSampling1", type=str)
parser.add_argument('-d', help='display graph localy', action='store_true')
parser.add_argument('-date', help='date in YYYYMMDD format', type=str, default=None, nargs="?")
				
args = parser.parse_args()

names = args.names
IP = args.ip+":"+str(args.port)
DBname = args.db
username = get_value_from_file('config.txt', 'username')
password = get_value_from_file('config.txt', 'password')

conn = pymssql.connect(server=IP, user=username, password=password, database=DBname) 
print("successfully connected to server (IP:{}, username:{} DBname:{})".format(IP, username, DBname))
cursor = conn.cursor()  

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

type_sql_collumns = {
	"collaborative": "collaborativescore",
	"AR": "ARscore",
	"competitive": "competitivescore"
}

type_fun = type

types = sorted(type_indicators.keys())

grades = []
for name in names:	
	student_grades = []
	for type in types:
		file_name = "tmp/users/results/{}{}_real.txt".format(name, type_indicators[type])
		if os.path.isfile(file_name):
			with open(file_name, "r") as f:
				grade = np.mean(np.array([float(line.strip().split(":")[1]) for line in f.readlines()]))
		else:
			grade = 0.0

		student_grades.append(grade)
		

	grades.append(student_grades)
		
	print(name, *student_grades)
	cursor.callproc("SaveUserProfile", (name, *[ float(grade) for grade in student_grades], args.date,))
	
	
	print("query executed") 
	
conn.commit()	
conn.close() 

if args.d:
	plot_chart_plot(
		grades,
		types,
		['b', 'r', 'g', 'm', 'y'],
		names
	)




