"""
	script that analyses lessons and gives them weights. Usually used at same time with analyseUsers.
"""

import codecs
import time
import re 
import sys

import os.path
import matplotlib.pyplot as plt

print("reading started - Lessons")
start_time = time.time() # save time
i = 0
j = 0

display_graph = len(sys.argv) > 1 # graphs are displayed if there is at least one additional parameter to the script

users = {}
users_path = "tmp/users/users.txt" # results will be stored on users_path location
if os.path.isfile(users_path): # if there are saved weights for the lessons, set them as initial weights
	with codecs.open(users_path, "r", "utf-8-sig") as fin:
		for line in fin:
			a, b = line.split(":")
			a, b = a, float(b)
			
			users[a] = b

def get_entries_element(splited_entries, name):
	"""
		helper function that gets value from 
		['name1', 'name2', 'name3', 'value1', 'value2', 'value3'] for the specified name
	"""
	n = len(splited_entries)
	
	grupa_index = splited_entries.index(name)
	grupa = splited_entries[n//2 + grupa_index]
	
	return grupa
	
s = set()
d = {}

"calculating function of dependecies"
k = 3

A = 1*k
B = 1
C = 1/k

a = 2*A - 4*B + 2*C
b = -A + 4*B -3*C
c = C

print("a", a, "b", b, "c", c)

def f(x): return a * x**2 + b*x + c

def score_lesson(lesson, score, user):
	global d
	tmp = d.get(lesson, [0, 0])
	
	if user not in users: 
		print("{} not in users!".format(user))
		users[user] = 0.5
	
	if score:
		tmp[1] += 1 / f(users[user])
		tmp[0] += 1 / f(users[user])
	else:
		tmp[1] += 1 * f(users[user])
		tmp[0] += 0
		
	d[lesson] = tmp

with codecs.open('logs.txt', 'r', "utf-8-sig") as fin:
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
			
			def wrapper(x): 
				global j
				if "inputParams" in x["logDetails"]: # collaborative logs have inputParams
					isCollaborative = x["logDetails"]["inputParams"]["isCollaborative"]
					
					if not isCollaborative: # sve su kolaborativne
						return
					
					lesson = x["lesson"]					
					logEntries = x["logDetails"]["logEntries"]
									
					if isinstance(logEntries[0], dict): #there are 498 of them -> big logs
						j+=1
						for logEntrie in logEntries:
							problem = logEntrie["problem"]
							
							if "correct" in problem and problem["correct"] is not None:
								score_lesson(lesson, problem["correct"], name)
							else:
								if "fourthPart" in problem:
									string = problem["firstPart"]+problem["secondPart"]+problem["thirdPart"]+"="+problem["fourthPart"]
								else:
									string = problem["firstPart"]+problem["secondPart"]+problem["thirdPart"]
							
								first, second = string.replace(":", "/").replace("·", "*").split("=")
								
								try:
									first = eval(first)
									second = eval(second)
									
									score_lesson(lesson, first == second, name)
								except:
									print(problem, problem["correct"] if "correct" in problem else  "??")
									print(string)
									print()
									
									score_lesson(lesson, False, name)
					elif isinstance(logEntries[0], str): #there are 1657 of them, small logs
						j += 1
						
						split_logEntries = logEntries[0].split(";")
						
						grupa = get_entries_element(split_logEntries, "Grupa")
						split_grupa = [a.strip() for a in grupa.split(",")]
						user_index = split_grupa.index(name)
						
						problemFormula = get_entries_element(split_logEntries, "ProblemFormula")
						editorAnswer = get_entries_element(split_logEntries, "EditorAnswer")
						
						# if editorAnswer is empty set it as some random number
						editorAnswer = "-100000" if editorAnswer == '' else editorAnswer 
						
						if "?" in problemFormula: 	# some problems look like 1 + ? = 3					
							solvedProblem = problemFormula.replace('?', editorAnswer)
							first, second = solvedProblem.split("=")
															
							first = eval(first.replace('·', '*').replace(':', '/'))
							second = eval(second)
							
							score_lesson(lesson, first == second, name)
						else:
							authorAnswer = get_entries_element(split_logEntries, "AuthorAnswer")
							
							score_lesson(lesson, authorAnswer+"="+editorAnswer == problemFormula, name)
						
					else:
						# nikad se ne dogodi
						print(logEntries)
				else:
					# ima ih 2
					# data
					pass
					# TOOOOOOOOOOOOOOOOOOODOOOOOOOOOOOOOOOO
			wrapper(params)
				
		except Exception as e:
			print("PROBLEM OCCURED", i, e)
			print(line)
			exit()
			with codecs.open('tmp.txt', 'w', "utf-8-sig") as fout:
				fout.write(JSONParams+"\n")
				
			break
			
		
			
print(i, j)
print("reading finished")

""" možda ne trbia?
#IMPORTANT
# do ovdje je lagan zadatak s 
for key in d:
	tmp = d[key]
	tmp[0] = tmp[1] - tmp[0]
	d[key] = tmp
#IMPORTANT
"""

with codecs.open('tmp/lessons/lessons.txt', "w", 'utf-8-sig') as fout:
	for lesson in sorted(d.keys()):
		print(lesson, d[lesson][0], d[lesson][1], d[lesson][0]/ d[lesson][1])
		fout.write("{}:{}\n".format(lesson, d[lesson][0] / d[lesson][1]))
		
		
print("prining set (size: {})".format(len(s)))
for string in s:                            
	print(string)

if display_graph:
	img_name = "tmp/lessons/{}.png".format(sys.argv[1]);

	plt.hist([ int(d[key][0]/d[key][1] * 100) for key in d])
	plt.savefig(img_name)
	print("saved {}".format(img_name))