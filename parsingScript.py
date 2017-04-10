import codecs
import re 
import json
from collections import namedtuple
import time

print("reading started")

start_time = time.time()
i = 0
j = 0

with codecs.open('logs_lession_preprocessed4.txt', 'r', "utf-8-sig") as fin:
	with codecs.open('logs_lession_widget_log.txt', "w", "utf-8-sig") as fout:
		for line in fin:
			i += 1	
			if time.time() - start_time > 10: 
				print(i)
				start_time = time.time()		
			
			m = re.search("\(([0-9]+), '([^']+)', '([^']+)', datetime\.datetime\(([^\)]+)\), '([^']+)', ([0-9]+)\)", line)		
			
			try:			
				id, eventName, eventType, datetime, JSONParams, contextualInfoId = m.groups();
				
				if eventName == "widget_log":
					j += 1
					fout.write(line)
				
					
			except:
				print("cant parse")
				print(line)
				break				
print(i, j)
print("reading finished")

"""print("printing set (size:{})".format(len(s)))
for string in s:
	print(string)"""