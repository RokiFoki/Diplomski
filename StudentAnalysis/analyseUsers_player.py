"""
	script that analyses users and gives them weights. Usually used at same time with analyseLessons.
"""

import codecs
import time
import re 
import sys
from pprint import pprint

import os.path
import matplotlib.pyplot as plt

from utils import get_file_name_from_dates
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="?????.")

parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')
parser.add_argument('-i', help="image file name (no extension)", type=str, metavar="IMG")
parser.add_argument('-r', help="results file name (no extension)", type=str, default="users.txt", metavar="rFile")
parser.add_argument('-d', help="lesson info file name (no extension)", type=str, default="lessons.txt", metavar="dFile")

args = parser.parse_args()
dates = args.date


print("reading started - Users")
start_time = time.time() # save time
i = 0
j = 0

"""
penalty_miliseconds = 2 * 1000
max_miliseconds = 120 * 1000
normal_miliseconds = 40 * 1000

"""

lessons = {}
lessons_path = "tmp/lessons/{}_player.txt".format(args.d) # location of lesson weights
if os.path.isfile(lessons_path): # if there are saved weights for the lessons use them
	with codecs.open(lessons_path, "r", "utf-8-sig") as fin:
		for line in fin:
			a, b = line.split(":")
			a, b = a, float(b)
			
			lessons[a] = b
		

s = set()
d = {}

"calculating function of dependecies"


k=3
def fp(x): return k**(1-2*x)
def fr(x): return x**2
def ft(x): return (x+1)/2.0

def score_user(user, score, lesson, percentage=1): # bitno, prije je bio if rijesio else nije...., sada je kad ne rijesi -1!!!!
	# ne moze se samo copy paste
	global d
	tmp = d.get(user, [0, 0])
	
	score = 1 if score == True else \
			-1 if score == False else \
			score 
	
	if lesson not in lessons: 
		print("{} not in lessons!".format(lesson))
		lessons[lesson] = 0.5
	
	tmp[0] += fr(score) * ft(score) * fp(lessons[lesson])**score * percentage
	tmp[1] += fr(score) * fp(lessons[lesson])**score
	
	d[user] = tmp
	
	
dict_student_problem = {}
with codecs.open(get_file_name_from_dates('logs_player_filtered', dates), 'r', "utf-8-sig") as fin:
	for line in fin:
		i += 1	
		if time.time() - start_time > 10: 
			print("i", i)
			start_time = time.time()		
								

		m = re.search("\('([^']+)', ([0-9]+), '([^']+)', '([^']+)', datetime\.datetime\(([^\)]+)\), '([^']+)', ([0-9]+)\)", line)	

		try:			
			name, id, eventName, eventType, datetime, JSONParams, contextualInfoId = m.groups();
			
			name = name.strip()
			
			year, month, day, *rest = [int(item) for item in datetime.split(', ')]
			
			datetime = "{} {} {}".format(year, month, day)
			
			key = "{},{}".format(name, datetime)
			
		except:
			import traceback
			print("cant parse:")
			print(line)
			traceback.print_exc()
			exit()
		
		try:	
			params = eval(JSONParams)
			
			lesson = params["lesson"]
			key = "{},{},{}".format(name, lesson, datetime)

			def store_log(log):
				global dict_student_problem, key

				problems = dict_student_problem.get(key, set())
				problems.add(str(log))
				dict_student_problem[key] = problems

			def collect():
				global j, k
				params = eval(JSONParams)

				lesson = params["lesson"]
				if isinstance(params["logDetails"], list):
					for answer in params["logDetails"]:
						if "correct" in answer:
							store_log(answer)
						elif "problem" in answer:
							problem = answer["problem"]
							if "correct" in problem:
								store_log(problem)
						
							
				elif(isinstance(params["logDetails"], dict)):					
					logDetails = params["logDetails"]
					if "inputParams" in logDetails:						
						if "isCollaborative" in logDetails["inputParams"] and logDetails["inputParams"]["isCollaborative"]:
							return
											
						if "logEntries" in logDetails:
							for logEntry in logDetails["logEntries"]:
								if(isinstance(logEntry, list)):
									for entry in logEntry:
										if "answers" in entry:
											for answer in entry["answers"]:
												if "correct" in answer:
													store_log(answer)
								else:
									if "problem" in logEntry:
										problem = logEntry["problem"]
										if "correct" in problem:
											store_log(problem)

									elif "answers" in logEntry:
										answers = logEntry["answers"]
										if isinstance(answers, list):
											for answer in answers:
												if "correct" in answer:
													store_log(answer)


						elif "logEntry" in logDetails:
							logEntry = logDetails["logEntry"]
							if "problem" in logEntry:
								problem = logEntry["problem"]
								if "correct" in problem:
									store_log(problem)
								
					else:
						if "data" in logDetails:
							data = logDetails["data"]
							if "partial_logEntries" in data:
								partial_logEntries = data["partial_logEntries"]
								if(isinstance(partial_logEntries, list)):
									for entry in partial_logEntries:
										if "problem" in entry:
											problem = entry["problem"]
											if "correct" in problem:
												store_log(problem)
											else:
												pass
												# first, second third part

						elif "gameLog" in logDetails:
							gameLog = logDetails["gameLog"]
							if "logEntries" in gameLog:
								logEntries = gameLog["logEntries"]
								if isinstance(logEntries, list):
									for logEntry in logEntries:
										if "correct" in logEntry:
											store_log(logEntry)
							else:
								if isinstance(gameLog, list):
									for entry in gameLog:
										if "correct" in entry:
											store_log(entry)			

			collect()		
				
		except Exception as e:
			import traceback
			print("PROBLEM OCCURED", i, e)
			print(line)
			
			traceback.print_exc()
			exit(1)
				
		
			
print(i, j, k)
print("reading finished")

for string in sorted(s):
	print(string)

print(len(dict_student_problem.keys()))
for key in dict_student_problem:
	name, lesson, date = key.split(',')
	for problem in dict_student_problem[key]:
		problem = eval(problem)
		if problem["correct"] != True and problem["correct"] != False:
			print(problem)
		else:
			score_user(name, problem["correct"], lesson)
	
	
with codecs.open('tmp/users/{}_player.txt'.format(args.r), "w", 'utf-8-sig') as fout:
	for user in sorted(d.keys()):
		print(user, d[user][0], d[user][1], d[user][0]/ d[user][1])
		fout.write("{}:{}\n".format(user, d[user][0] / d[user][1]))

		
if args.i:
	img_name = "tmp/users/{}_player.png".format(args.i);

	plt.hist([ int(d[key][0]/d[key][1] * 100) for key in d])
	plt.savefig(img_name)
	print("saved {}".format(img_name))
