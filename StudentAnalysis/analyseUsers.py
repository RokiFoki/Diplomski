"""
	script that analyses users and gives them weights. Usually used at same time with analyseLessons.
"""

import codecs
import time
import re 
import sys

import os.path
import matplotlib.pyplot as plt
from pprint import pprint

from utils import get_file_name_from_dates
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="calculates student success from collaborative logs defined with specified dates")

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

lessons = {}
lessons_path = "tmp/lessons/{}.txt".format(args.d) # location of lesson weights
if os.path.isfile(lessons_path): # if there are saved weights for the lessons use them
	with codecs.open(lessons_path, "r", "utf-8-sig") as fin:
		for line in fin:
			a, b = line.split(":")
			a, b = a, float(b)
			
			lessons[a] = b
else:
	print("there is no file {}".format(lessons_path))
		
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

k=3
def fp(x): return k**(1-2*x)
def fr(x): return x**2
def ft(x): return (x+1)/2.0

def score_user(user, score, lesson, percentage=1): 
	global d
	tmp = d.get(user, [0, 0])
	
	score = 1 if score == True else \
			-1 if score == False else \
			score 
	
	if lesson not in lessons: 
		print("{} not in lessons!".format(lesson))
		lessons[lesson] = 0.8
	
	tmp[0] += fr(score) * ft(score) * fp(lessons[lesson])**score * percentage
	tmp[1] += fr(score) * fp(lessons[lesson])**score
	
	d[user] = tmp

	
with codecs.open(get_file_name_from_dates('logs_collaborative', dates), 'r', "utf-8-sig") as fin:
	for i, line in enumerate(fin):
			
		if time.time() - start_time > 10: 
			print("i", i)
			start_time = time.time()	
				
		m = re.search("\(([0-9]+), '([^']+)', ([0-9]+), '([^']+)', '([^']+)', datetime\.datetime\(([^\)]+)\), '([^']+)', ([0-9]+)\)", line)	


		try:			
			userid, name, id, eventName, eventType, datetime, JSONParams, contextualInfoId = m.groups();
			
			name = name.strip()
				
		except:
			print("cant parse:")
			print(line)
			break
		
		try:		
			params = eval(JSONParams)
			x = params
			
			if "inputParams" in x["logDetails"]: # collaborative logs have inputParams
				isCollaborative = x["logDetails"]["inputParams"]["isCollaborative"]
				
				if not isCollaborative: # sve su kolaborativne
					continue
				
				lesson = str(x["lesson"])					
				logEntries = x["logDetails"]["logEntries"]
				if len(logEntries) == 0: continue
			
				if isinstance(logEntries[0], dict): #there are 498 of them -> big logs
					try:
						if ":" not in x["logDetails"]["inputParams"]["groupMembers"][0]:
							# [' Ime Prezime', ' Ime2 Prezime2']
							members = [a.strip() for a in x["logDetails"]["inputParams"]["groupMembers"]]
							user_index = members.index(name)
							
							if len(members) == 2:
								role = 'E' if user_index == 0 else 'C'
							else:
								role = 'A' if user_index == 0 else 'C' if user_index == 1 else 'E'
						else:
							# ['E: Ime Prezime', 'C: Ime2 Prezime2']
							members = [a.split(":")[1].strip() for a in x["logDetails"]["inputParams"]["groupMembers"]]	
							roles = [a.split(":")[0].strip() for a in x["logDetails"]["inputParams"]["groupMembers"]]
						
							user_index = members.index(name)
							role = roles[user_index]
							
					except ValueError:
						# happened once, name = 'Učiteljica (zamjenski tablet)', members = ['nesto', 'Uciteljica (zamjenski tablet)' (c != č)
						
						print(i, "PROBLEM:", name, 'is not in', members)
						br += 1
						continue
					
						
					if role != 'E': continue # TOOOOOOOOOOOOOOOOOOODOOOOOOOOOOOOOOOO
					j+=1
					
					for logEntrie in logEntries:														
						#j += 1
						problem = logEntrie["problem"]
						
						if "correct" in problem and problem["correct"] is not None:
							score_user(userid, problem["correct"], lesson)
						else:
							if "fourthPart" in problem:
								string = problem["firstPart"]+problem["secondPart"]+problem["thirdPart"]+"="+problem["fourthPart"]
							else:
								string = problem["firstPart"]+problem["secondPart"]+problem["thirdPart"]
						
							first, second = string.replace(":", "/").replace("·", "*").split("=")
							
							try:
								first = eval(first)
								second = eval(second)
								
								score_user(userid, first == second, lesson)
							except:
								print(problem, problem["correct"] if "correct" in problem else  "??")
								print(string)
								print()
								
								score_user(userid, False, lesson)
				elif isinstance(logEntries[0], str): #there are 1657 of them, small logs
					j += 1						
					split_logEntries = logEntries[0].split(";")
					
					grupa = get_entries_element(split_logEntries, "Grupa")
					
					try:
						if ":" not in grupa:
							# "Ime Prezime, ime2 prezime2,..."
							split_grupa = [a.strip() for a in grupa.split(",")]
							user_index = split_grupa.index(name)
							
							if len(split_grupa) == 2:
								role = 'E' if user_index == 0 else 'C'
							else:
								role = 'A' if user_index == 0 else 'C' if user_index == 1 else 'E'
						else:
							# "E: Ime prezime, C: Ime2 prezime2"
							split_grupa = [a.split(":")[1].strip() for a in grupa.split(",")]
							roles = [a.split(":")[0].strip() for a in grupa.split(",")]
							
							user_index = split_grupa.index(name)
							role = roles[user_index]
					except ValueError:
						# happened once, name = 'Učiteljica (zamjenski tablet)', split_grupa = ['nesto', 'Uciteljica (zamjenski tablet)' (c != č)
						
						continue
						
						
					
					problemFormula = get_entries_element(split_logEntries, "ProblemFormula")
					
					editorAnswerCorrect = None
					try:
						editorAnswer = get_entries_element(split_logEntries, "EditorAnswer")
						# if editorAnswer is empty set it as some random number
						
					except ValueError:
						editorAnswer = get_entries_element(split_logEntries, "GivenAnswerCalculation").strip()
					
					editorAnswer = "-100000" if editorAnswer == '' else editorAnswer 
						
					try:
						checkerAnswer = get_entries_element(split_logEntries, "CheckerAnswer")
					except ValueError:
						# if there is no entry for checker, that means
						checkerAnswer = "Ok"
					
					if "?" in problemFormula: 	# some problems look like 1 + ? = 3
						solvedProblem = problemFormula.replace('?', editorAnswer)
						first, second = solvedProblem.split("=")
														
						first = eval(first.replace('·', '*').replace(':', '/'))
						second = eval(second)
						
						if role == 'E': #editor
							score_user(userid, first == second, lesson)
						elif role == 'C': #checker ZERO TIMES!!!!!!!!!
							score_user(userid, first == second if checkerAnswer=="Ok" else first != second, lesson)
					else:
						try:
							authorAnswer = get_entries_element(split_logEntries, "AuthorAnswer")
						except ValueError:
							authorAnswer = get_entries_element(split_logEntries, "GivenAnswerFormula")
						
						if "=" in problemFormula:
							first, second = problemFormula.split("=")
						else:
							first = problemFormula
						
						first = first.replace('·', '*').replace(':', '/')
						
						if role == 'A': # author zero times
							score_user(userid, authorAnswer == first, lesson)
						elif role == 'E': # editor 528 times
							good = True
							try:
								authorA = eval(authorAnswer)
							except:
								good = False;
							
							if good:
								try:
									score_user(userid, authorA == eval(editorAnswer), lesson)
								except:
									score_user(userid, False, lesson)
						elif role == 'C': # checker ZERO times (not anymore??)
							good = (authorAnswer == first and editorAnswer == eval(first))
							
							checkerGood = checkerAnswer == "Ok"
							
							score_user(userid, checkerAnswer == good, lesson)
							
							
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
				
		except Exception as e:
			print("PROBLEM OCCURED", i, e)
			import traceback
			traceback.print_exc()
			
			print(line)
			exit(1)
			with codecs.open('tmp.txt', 'w', "utf-8-sig") as fout:
				fout.write(JSONParams+"\n")
				
			break
			
		
			
print(i, j)
print("reading finished")

with codecs.open('tmp/users/{}.txt'.format(args.r), "w", 'utf-8-sig') as fout:
	for lesson in sorted(d.keys()):
		print(lesson, d[lesson][0], d[lesson][1], d[lesson][0]/ d[lesson][1])
		fout.write("{}:{}\n".format(lesson, d[lesson][0] / d[lesson][1]))
		
		
print("prining set (size: {})".format(len(s)))
for string in s:
	print(string)
	
if args.i:
	img_name = "tmp/users/{}.png".format(args.i);

	plt.hist([ int(d[key][0]/d[key][1] * 100) for key in d])
	plt.savefig(img_name)
	print("saved {}".format(img_name))
