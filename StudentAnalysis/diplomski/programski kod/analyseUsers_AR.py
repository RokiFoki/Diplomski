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

parser = argparse.ArgumentParser(description="calculates student success from AR logs defined with specified dates")

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

penalty_miliseconds = 2 * 1000
max_miliseconds = 120 * 1000
normal_miliseconds = 40 * 1000

lessons = {}
lessons_path = "tmp/lessons/{}_AR.txt".format(args.d) # location of lesson weights
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

def score_user(user, score, lesson, percentage=1):
	global d
	tmp = d.get(user, [0, 0])
	
	score = 1 if score == True else \
			-1 if score == False else \
			score 
	
	if lesson not in lessons: 
		if len(str(lesson)) < 20: print("{} not in lessons!".format(lesson))
		lessons[lesson] = 0.5
	
	tmp[0] += fr(score) * ft(score) * fp(lessons[lesson])**score * percentage
	tmp[1] += fr(score) * fp(lessons[lesson])**score
	
	d[user] = tmp
	
with codecs.open(get_file_name_from_dates('logs_AR', dates), 'r', "utf-8-sig") as fin:
	for line in fin:
		i += 1	
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
			
			def math_analyse(params):
				for question in params:
					if "answers" not in question: continue
					
					correctAnswer = question["correctAnswer"]
					answerLen = len(correctAnswer)
					correctAnswers = []
					for i, c in enumerate(correctAnswer):
						correctAnswers.append(c + '0'*(answerLen-1-i))
						
					answeredAnswers = [0] * answerLen
					answers = question["answers"]
					
					elapsedSeconds = 0
					for answer in answers:
						if answer["answer"] in correctAnswers:
							answeredAnswers[correctAnswers.index(answer["answer"])] = 1
							
							elapsedSeconds = int(answer["elapsedSeconds"])
					
					if 0 in answeredAnswers:
						pass
					
					# str(question) is probably always different
					
					miliseconds = max(elapsedSeconds - normal_miliseconds, 0)
					penalty = penalty_miliseconds * (len(answers) - answerLen)
					
					score_user(userid, 0 not in answeredAnswers, str(question), 1 - min(miliseconds + penalty, max_miliseconds) / max_miliseconds)
			
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
								
								return sovled, 1 - min(miliseconds + penalty, max_miliseconds) / max_miliseconds								
							
						except Exception as e:
							print("Exception", e)
							return -1, -1
					
					sovled, score = cal_score(answers)
					
					score_user(userid, sovled, lesson, score)
					
			elif eventType == "AR.Shapes" and "answers" not in params[0]:
				math_analyse(params)
			elif eventType == "AR.Math":
				math_analyse(params)	
				pass
		except Exception as e:
			print("PROBLEM OCCURED", i, e)
			print(line)
			exit(1)
			with codecs.open('tmp.txt', 'w', "utf-8-sig") as fout:
				fout.write(JSONParams+"\n")
				
			break
			
		
			
print(i, j, k)
print("reading finished")

print("prining set (size: {})".format(len(s)))
for string in s:
	print(string)
	
	
with codecs.open('tmp/users/{}_AR.txt'.format(args.r), "w", 'utf-8-sig') as fout:
	for user in sorted(d.keys()):
		print(user, d[user][0], d[user][1], d[user][0]/ d[user][1])
		fout.write("{}:{}\n".format(user, d[user][0] / d[user][1]))

		
if args.i:
	img_name = "tmp/users/{}_AR.png".format(args.i);

	plt.hist([ int(d[key][0]/d[key][1] * 100) for key in d])
	plt.savefig(img_name)
	print("saved {}".format(img_name))
