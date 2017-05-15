"""
	script that analyses lessons and gives them weights. Usually used at same time with analyseUsers.
"""

import codecs
import time
import re 
import sys, os
from pprint import pprint

import os.path
import matplotlib.pyplot as plt

print("reading started - Lessons")
start_time = time.time() # save time
i = 0
j = 0

penalty_miliseconds = 2 * 1000
max_miliseconds = 180 * 1000
normal_miliseconds = 40 * 1000

display_graph = len(sys.argv) > 1 # graphs are displayed if there is at least one additional parameter to the script

users = {}
users_path = "tmp/users/users_AR.txt" # results will be stored on users_path location
if os.path.isfile(users_path): # if there are saved weights for the lessons, set them as initial weights
	with codecs.open(users_path, "r", "utf-8-sig") as fin:
		for line in fin:
			a, b = line.split(":")
			a, b = a, float(b)
			
			users[a] = b

	
s = set()
d = {}

"calculating function of dependecies"
k=3
def fp(x): return k**(1-2*x)
def fr(x): return x**2
def ft(x): return (x+1)/2.0

def score_lesson(lesson, score, user, percentage=1): # bitno, prije je bio if rijesio else nije...., sada je kad ne rijesi -1!!!!
	# ne moze se samo copy paste
	global d
	tmp = d.get(lesson, [0, 0])
	
	score = 1 if score == True else \
			-1 if score == False else \
			score 
	
	if user not in users: 
		print("{} not in user!".format(user))
		users[user] = 0.5
	
	tmp[0] += fr(score) * ft(score) * fp(users[user])**score * percentage
	tmp[1] += fr(score) * fp(users[user])**score
	
	d[lesson] = tmp


with codecs.open('logs_AR.txt', 'r', "utf-8-sig") as fin:
	for line in fin:
		i += 1	
		if time.time() - start_time > 10: 
			print("i", i)
			start_time = time.time()		
				
		m = re.search("\('([^']+)', ([0-9]+), '([^']+)', '([^']+)', datetime\.datetime\(([^\)]+)\), '([^']+)', ([0-9]+)\)", line)	

		try:			
			name, id, eventName, eventType, datetime, JSONParams, contextualInfoId = m.groups();
			
			name = name.strip()
				
		except:
			print("cant parse:")
			print(line)
			break
		
		try:		
			params = eval(JSONParams)
			if eventType == "AR.Shapes" and "answers" in params[0]:
				for question in params:
				
					lesson = question['task']
					answers = [answer for answer in question["answers"] if int(answer["elapsedSeconds"]) > 1000 or answer["correct"] == 'True']
					
					def cal_score(answers):
						global s, params
						try:
							# return first element thats correct, otherwise 'None'
							el = next((element for element in answers if element['correct'] == 'True'), None)
							
							if el is None:
								return -1, -1
							else:
								sovled = 1
								
								miliseconds = max(int(el["elapsedSeconds"]) - normal_miliseconds, 0)
								penalty = penalty_miliseconds * (len(answers) - 1)
								
								if miliseconds > 100000 and False:
									pprint(params)
									time.sleep(100)
								
								return sovled, 1 - min(miliseconds + penalty, max_miliseconds) / max_miliseconds								
							
						except Exception as e:
							print("Exception", e)
							return -1, -1
					
					sovled, score = cal_score(answers)
					
					score_lesson(lesson, sovled, name, score)
					
			elif eventType == "AR.Shapes" and "answers" not in params[0]:
				pprint(params)
				print()
				
		except Exception as e:
			print("PROBLEM OCCURED", i, e)
			print(line)
			
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)

			exit()
			
		
			
print(i, j)
print("reading finished")


with codecs.open('tmp/lessons/lessons_AR.txt', "w", 'utf-8-sig') as fout:
	for lesson in sorted(d.keys()):
		print(lesson, d[lesson][0], d[lesson][1], d[lesson][0]/ d[lesson][1])
		fout.write("{}:{}\n".format(lesson, d[lesson][0] / d[lesson][1]))
		
		
print("prining set (size: {})".format(len(s)))
for string in s:                            
	print(string)

if display_graph:
	img_name = "tmp/lessons/{}_AR.png".format(sys.argv[1]);

	plt.hist([ int(d[key][0]/d[key][1] * 100) for key in d])
	plt.savefig(img_name)
	print("saved {}".format(img_name))