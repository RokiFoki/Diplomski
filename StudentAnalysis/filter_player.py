"""
	script that analyses users and gives them weights. Usually used at same time with analyseLessons.
"""

import codecs
import time
import re 
import sys
from pprint import pprint

import os.path

print("reading started")
start_time = time.time() # save time
i = 0
j = 0

"""
penalty_miliseconds = 2 * 1000
max_miliseconds = 120 * 1000
normal_miliseconds = 40 * 1000

display_graph = len(sys.argv) > 1 # graphs are displayed if there is at least one additional parameter to the script

lessons = {}
lessons_path = "tmp/lessons/lessons_AR.txt" # location of lesson weights
if os.path.isfile(lessons_path): # if there are saved weights for the lessons use them
	with codecs.open(lessons_path, "r", "utf-8-sig") as fin:
		for line in fin:
			a, b = line.split(":")
			a, b = a, float(b)
			
			lessons[a] = b
		
"""
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
	
with codecs.open('logs_player.txt', 'r', "utf-8-sig") as fin:
	with codecs.open('logs_player_filtered.txt', 'w', "utf-8-sig") as fout:
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
				
				lesson = params["lesson"]
				if isinstance(params["logDetails"], list):
					continue
						
							
				elif(isinstance(params["logDetails"], dict)):
					logDetails = params["logDetails"]
					if "inputParams" in logDetails:
						
						if "isCollaborative" in logDetails["inputParams"] and logDetails["inputParams"]["isCollaborative"]: continue
											
						if "logEntries" in logDetails:
							for logEntry in  logDetails["logEntries"]:
								if "problem" in logEntry:
									if "confirmSolution" not in logEntry["problem"] and "needToDiscuss" not in logEntry["problem"] and "waitingForChecker" not in logEntry["problem"]:
										fout.write(line)
										j+=1
						else:
							fout.write(line)
							j+=1
					
				
					
			except Exception as e:
				import traceback
				print("PROBLEM OCCURED", i, e)
				print(line)
				
				traceback.print_exc()
				exit()
				with codecs.open('tmp.txt', 'w', "utf-8-sig") as fout:
					fout.write(JSONParams+"\n")
					
				break
				
		
			
print(i, j, k)
print("reading finished")

print("prining set (size: {})".format(len(s)))
for string in sorted(s):
	print(string)
