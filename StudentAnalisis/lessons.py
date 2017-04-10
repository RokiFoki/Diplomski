import codecs
import re 
import time

print("reading started")

start_time = time.time()
i = 0
j = 0

s = set()
with codecs.open('logs.txt', 'r', "utf-8-sig") as fin:
	for line in fin:
		i += 1	
		if time.time() - start_time > 10: 
			print(i)
			start_time = time.time()		
				
		m = re.search("\('([^']+)', ([0-9]+), '([^']+)', '([^']+)', datetime\.datetime\(([^\)]+)\), '([^']+)', ([0-9]+)\)", line)	

		try:			
			name, id, eventName, eventType, datetime, JSONParams, contextualInfoId = m.groups();
				
		except:
			print("cant parse:")
			print(line)
			break
		
		
		try:		
			j += 1
			params = eval(JSONParams)
			def wrapper(x): 
				try: 
					tmp = x["lesson"];
					a = str(tmp)
					s.add(str(tmp))
					
				except: 
					pass
			
			wrapper(params)
				
		except:
			print("PROBLEM OCCURED", i)
			exit()
			with codecs.open('tmp.txt', 'w', "utf-8-sig") as fout:
				fout.write(JSONParams+"\n")
				pass				
				
			print(JSONParams.encode('utf8'))
			print("datetime.datetime({})".format(datetime))
			print("event name:{}".format(eventName))
			params = eval(JSONParams)
			break
			
		
			
print(i, j)
print("reading finished")

print("prining set (size: {})".format(len(s)))
with codecs.open('lessons.txt', "w", 'utf-8-sig') as fout:				
	for string in sorted(s):
		print(string)
		fout.write(string+"\n")