import codecs
import time
import re 

print("reading started")
start_time = time.time()
i = 0
j = 0

def get_entries_element(splited_entries, name):
	n = len(splited_entries)
	
	grupa_index = splited_entries.index(name)
	grupa = splited_entries[n//2 + grupa_index]
	
	return grupa
	
s = set()
d = {}

def score_lesson(lesson, score):
	global d
	tmp = d.get(lesson, [0, 0])
	tmp[1] += 1
	tmp[0] += 1 if score else 0
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
								score_lesson(lesson, problem["correct"])
							else:
								if "fourthPart" in problem:
									string = problem["firstPart"]+problem["secondPart"]+problem["thirdPart"]+"="+problem["fourthPart"]
								else:
									string = problem["firstPart"]+problem["secondPart"]+problem["thirdPart"]
							
								first, second = string.replace(":", "/").replace("·", "*").split("=")
								
								try:
									first = eval(first)
									second = eval(second)
									
									score_lesson(lesson, first == second)
								except:
									print(problem, problem["correct"] if "correct" in problem else  "??")
									print(string)
									print()
									
									score_lesson(lesson, False)
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
							
							score_lesson(lesson, first == second)
						else:
							authorAnswer = get_entries_element(split_logEntries, "AuthorAnswer")
							
							score_lesson(lesson, authorAnswer+"="+editorAnswer == problemFormula)
						
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
		fout.write("{} {}\n".format(lesson, d[lesson][0] / d[lesson][1]))
		
		
print("prining set (size: {})".format(len(s)))
for string in s:
	print(string)

