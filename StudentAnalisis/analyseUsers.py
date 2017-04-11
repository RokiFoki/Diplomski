import codecs
import time
import re 
import sys

import os.path
import matplotlib.pyplot as plt

print("reading started - Users")
start_time = time.time()
i = 0
j = 0
k = 0

display_graph = len(sys.argv) > 1

lessons = {}
lessons_path = "tmp/lessons/lessons.txt"
if os.path.isfile(lessons_path):
	with codecs.open(lessons_path, "r", "utf-8-sig") as fin:
		for line in fin:
			a, b = line.split(":")
			a, b = a, float(b)
			
			lessons[a] = b
		
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

def score_user(user, score, lesson):
	global d
	tmp = d.get(user, [0, 0])
	
	if lesson not in lessons: 
		print("{} not in lessons!".format(lesson))
		lessons[lesson] = 0.5
	
	if score:
		tmp[1] += 1 / f(lessons[lesson])
		tmp[0] += 1 / f(lessons[lesson])
	else:
		tmp[1] += 1 * f(lessons[lesson])
		tmp[0] += 0
	
	d[user] = tmp

	
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
				global j, k
				if "inputParams" in x["logDetails"]:
					isCollaborative = x["logDetails"]["inputParams"]["isCollaborative"]
					
					if not isCollaborative: # sve su kolaborativne
						return
					
					lesson = x["lesson"]					
					logEntries = x["logDetails"]["logEntries"]
				
					if isinstance(logEntries[0], dict): #498
						members = [a.strip() for a in x["logDetails"]["inputParams"]["groupMembers"]]
														
						user_index = members.index(name)
							
						if user_index != 1: return # TOOOOOOOOOOOOOOOOOOODOOOOOOOOOOOOOOOO
						j+=1
						
						for logEntrie in logEntries:
														
							#j += 1
							problem = logEntrie["problem"]
							
							if "correct" in problem and problem["correct"] is not None:
								score_user(name, problem["correct"], lesson)
							else:
								if "fourthPart" in problem:
									string = problem["firstPart"]+problem["secondPart"]+problem["thirdPart"]+"="+problem["fourthPart"]
								else:
									string = problem["firstPart"]+problem["secondPart"]+problem["thirdPart"]
							
								first, second = string.replace(":", "/").replace("·", "*").split("=")
								
								try:
									first = eval(first)
									second = eval(second)
									
									score_user(name, first == second, lesson)
								except:
									print(problem, problem["correct"] if "correct" in problem else  "??")
									print(string)
									print()
									
									score_user(name, False, lesson)
					elif isinstance(logEntries[0], str): #1657
						j += 1
						
						split_logEntries = logEntries[0].split(";")
						
						grupa = get_entries_element(split_logEntries, "Grupa")
						split_grupa = [a.strip() for a in grupa.split(",")]
						user_index = split_grupa.index(name)
						
						problemFormula = get_entries_element(split_logEntries, "ProblemFormula")
						editorAnswer = get_entries_element(split_logEntries, "EditorAnswer")
						
						editorAnswer = "-100000" if editorAnswer == '' else editorAnswer # TOOOOOOOOOOOOOOOOOOODOOOOOOOOOOOOOOOO
						
						checkerAnswer = get_entries_element(split_logEntries, "CheckerAnswer")
						
						if "?" in problemFormula: 						
							solvedProblem = problemFormula.replace('?', editorAnswer)
							first, second = solvedProblem.split("=")
															
							first = eval(first.replace('·', '*').replace(':', '/'))
							second = eval(second)
							
							if user_index == 0: #editor
								score_user(name, first == second, lesson)
							else: #checker ZERO TIMES!!!!!!!!!
								score_user(name, first == second if checkerAnswer=="Ok" else first != second, lesson)
						else:
							authorAnswer = get_entries_element(split_logEntries, "AuthorAnswer")
							
							first, second = problemFormula.split("=")
														
							if user_index == 0: # author zero times
								score_user(name, authorAnswer == first, lesson)
							elif user_index == 1: # editor 528 times
								good = True
								try:
									authorA = eval(authorAnswer)
								except:
									good = False;
								
								if good:
									try:
										score_user(name, authorA == eval(editorAnswer), lesson)
									except:
										score_user(name, False, lesson)
							else: # checker ZERO times
								k += 1
								good = (authorAnswer == first and editorAnswer == second)
								
								checkerGood = checkerAnswer == "Ok"

								score_user(name, checkerAnswer == good. lesson)
								
								
							# for inx in range(len(split_logEntries) // 2):
								# s.add(split_logEntries[inx])
								
							
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
			
		
			
print(i, j, k)
print("reading finished")

with codecs.open('tmp/users/users.txt', "w", 'utf-8-sig') as fout:
	for lesson in sorted(d.keys()):
		print(lesson, d[lesson][0], d[lesson][1], d[lesson][0]/ d[lesson][1])
		fout.write("{}:{}\n".format(lesson, d[lesson][0] / d[lesson][1]))
		
		
print("prining set (size: {})".format(len(s)))
for string in s:
	print(string)
	
if display_graph:
	img_name = "tmp/users/{}.png".format(sys.argv[1]);

	plt.hist([ int(d[key][0]/d[key][1] * 100) for key in d])
	plt.savefig(img_name)
	print("saved {}".format(img_name))
