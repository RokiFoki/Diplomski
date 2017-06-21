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
k = 0

s = set()
d = {}
with codecs.open(get_file_name_from_dates('logs_player', dates), 'r', "utf-8-sig") as fin:
	with codecs.open(get_file_name_from_dates('logs_player_filtered', dates), 'w', "utf-8-sig") as fout:
		for line in fin:
			i += 1	
			if time.time() - start_time > 10: 
				print("i", i, "j", j)
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
				def collect():
					global j, k
					params = eval(JSONParams)

					lesson = params["lesson"]
					if isinstance(params["logDetails"], list):
						for answer in params["logDetails"]:
							if "correct" in answer:
								fout.write(line)
								j+=1
								return
							elif "problem" in answer:
								problem = answer["problem"]
								if "correct" in problem:
									fout.write(line)
									j+=1
									return
							
								
					elif(isinstance(params["logDetails"], dict)):					
						logDetails = params["logDetails"]
						if "inputParams" in logDetails:						
							if "isCollaborative" in logDetails["inputParams"] and logDetails["inputParams"]["isCollaborative"]:
								return
												
							if "logEntries" in logDetails:
								for logEntry in logDetails["logEntries"]:
									if(isinstance(logEntry, list)):
										for entry in logEntry:
											if "answers" in entry:
												for answer in entry["answers"]:
													if "correct" in answer:
														fout.write(line)
														j+=1
														return
									else:
										if "problem" in logEntry:
											problem = logEntry["problem"]
											if "correct" in problem:
												fout.write(line)
												j+=1
												return

										elif "answers" in logEntry:
											answers = logEntry["answers"]
											if isinstance(answers, list):
												for answer in answers:
													if "correct" in answer:
														fout.write(line)
														j+=1
														return


							elif "logEntry" in logDetails:
								logEntry = logDetails["logEntry"]
								if "problem" in logEntry:
									problem = logEntry["problem"]
									if "correct" in problem:
										fout.write(line)
										j+=1
										return 
									
						else:
							if "data" in logDetails:
								data = logDetails["data"]
								if "partial_logEntries" in data:
									partial_logEntries = data["partial_logEntries"]
									if(isinstance(partial_logEntries, list)):
										for entry in partial_logEntries:
											if "problem" in entry:
												problem = entry["problem"]
												if "correct" in problem:
													fout.write(line)
													j+=1
													return
												else:
													pass
													# first, second third part

							elif "gameLog" in logDetails:
								gameLog = logDetails["gameLog"]
								if "logEntries" in gameLog:
									logEntries = gameLog["logEntries"]
									if isinstance(logEntries, list):
										for logEntry in logEntries:
											if "correct" in logEntry:
												fout.write(line)
												j+=1
												return
								else:
									if isinstance(gameLog, list):
										for entry in gameLog:
											if "correct" in entry:												
												fout.write(line)
												j+=1
												return				

				collect()
				
					
			except Exception as e:
				import traceback
				print("PROBLEM OCCURED", i, e)
				print(line)
				
				traceback.print_exc()
				exit()
				
		
			
print(i, j, k)
print("reading finished")

print("prining set (size: {})".format(len(s)))
for string in sorted(s):
	print(string)
