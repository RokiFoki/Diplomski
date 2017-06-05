"""
	script that analyses users and gives them weights. Usually used at same time with analyseLessons.
"""

import codecs
import time
import re 
import sys
from pprint import pprint

import os.path
from utils import get_file_name_from_dates

import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Removes unnesesary quotes that some logs might have.")
parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')
					
args = parser.parse_args()

dates = args.date

print("reading started")
start_time = time.time() # save time
i = 0
j = 0

s = set()
d = {}

with codecs.open(get_file_name_from_dates('logs_player', dates), 'r', "utf-8-sig") as fin:
	with codecs.open(get_file_name_from_dates('logs_player_filtered', dates), 'w', "utf-8-sig") as fout:
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
				
		
			
print(i, j)
print("reading finished")

print("prining set (size: {})".format(len(s)))
for string in sorted(s):
	print(string)
