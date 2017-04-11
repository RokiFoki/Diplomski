import codecs
import time
import re 
import sys

import os.path
import matplotlib.pyplot as plt

print("reading started - Lessons")
start_time = time.time()
i = 0
j = 0

display_graph = len(sys.argv) > 1

users = {}
if os.path.isfile("users.txt"):
	with codecs.open("users.txt", "r", "utf-8-sig") as fin:
		for line in fin:
			a, b = line.split(":")
			a, b = a, float(b)
			
			users[a] = b

def get_entries_element(splited_entries, name):
	n = len(splited_entries)
	
	grupa_index = splited_entries.index(name)
	grupa = splited_entries[n//2 + grupa_index]
	
	return grupa
	
s = set()
d = {}

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
				if "inputParams" in x["logDetails"]:
					isCollaborative = x["logDetails"]["inputParams"]["isCollaborative"]
					
					if not isCollaborative: # sve su kolaborativne
						return
					
					lesson = x["lesson"]					
					logEntries = x["logDetails"]["logEntries"]
									
					if isinstance(logEntries[0], dict): #498
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
					elif isinstance(logEntries[0], str): #1657
						j += 1
						
						split_logEntries = logEntries[0].split(";")
						
						grupa = get_entries_element(split_logEntries, "Grupa")
						split_grupa = [a.strip() for a in grupa.split(",")]
						user_index = split_grupa.index(name)
						
						problemFormula = get_entries_element(split_logEntries, "ProblemFormula")
						editorAnswer = get_entries_element(split_logEntries, "EditorAnswer")
						
						editorAnswer = "-100000" if editorAnswer == '' else editorAnswer # TOOOOOOOOOOOOOOOOOOODOOOOOOOOOOOOOOOO
						
						if "?" in problemFormula: 						
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

with codecs.open('lessons.txt', "w", 'utf-8-sig') as fout:
	for lesson in sorted(d.keys()):
		print(lesson, d[lesson][0], d[lesson][1], d[lesson][0]/ d[lesson][1])
		fout.write("{}:{}\n".format(lesson, d[lesson][0] / d[lesson][1]))
		
		
print("prining set (size: {})".format(len(s)))
for string in s:
	print(string)

if display_graph:
	plt.hist([ int(d[key][0]/d[key][1] * 100) for key in d])
	plt.show()