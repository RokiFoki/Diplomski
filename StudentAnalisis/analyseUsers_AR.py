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

print("reading started - Users")
start_time = time.time() # save time
i = 0
j = 0
k = 0

display_graph = len(sys.argv) > 1 # graphs are displayed if there is at least one additional parameter to the script

lessons = {}
lessons_path = "tmp/lessons/lessons.txt" # location of lesson weights
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

def score_user(user, score, lesson):
	global d
	tmp = d.get(user, [0, 0])
	
	score = 1 if score == True else \
			0 if score == False else \
			score 
	
	if lesson not in lessons: 
		print("{} not in lessons!".format(lesson))
		lessons[lesson] = 0.5
	
	tmp[0] += fr(score) * ft(score) * fp(lessons[lesson])**score
	tmp[1] += fr(score) * fp(lessons[lesson])**score
	
	d[user] = tmp
	
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
			#if i == 168: print(); pprint(params)
			if eventType == "AR.Shapes" and "answers" in params[0]:
				for question in params:
				
					#if i == 168: print(); pprint(question)
					lesson = question['task']
					answers = [answer for answer in question["answers"] if int(answer["elapsedSeconds"]) > 1000 or answer["correct"] == 'True']
					
					#if i == 168: print(); pprint(answers)
					def exists(list, condition):
						try:
							# return first element thats correct, otherwise 'None'
							el = next((element for element in list if condition(element)), None)
							
							return el is not None
						except:
							return False
							
					score_user(name, exists(answers, lambda x: x['correct'] == 'True'), lesson)
					
			elif eventType == "AR.Shapes" and "answers" not in params[0]:
				pprint(params)
				print()
				
		except Exception as e:
			print("PROBLEM OCCURED", i, e)
			print(line)
			exit()
			with codecs.open('tmp.txt', 'w', "utf-8-sig") as fout:
				fout.write(JSONParams+"\n")
				
			break
			
		
			
print(i, j, k)
print("reading finished")

print("prining set (size: {})".format(len(s)))
for string in s:
	print(string)

exit()
	
with codecs.open('tmp/users/users.txt', "w", 'utf-8-sig') as fout:
	for lesson in sorted(d.keys()):
		print(lesson, d[lesson][0], d[lesson][1], d[lesson][0]/ d[lesson][1])
		fout.write("{}:{}\n".format(lesson, d[lesson][0] / d[lesson][1]))
		
		

	
if display_graph:
	img_name = "tmp/users/{}.png".format(sys.argv[1]);

	plt.hist([ int(d[key][0]/d[key][1] * 100) for key in d])
	plt.savefig(img_name)
	print("saved {}".format(img_name))
