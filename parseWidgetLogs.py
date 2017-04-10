import codecs
import re 
import time

print("reading started")

start_time = time.time()
i = 0
j = 0

s = []
with codecs.open('logs_lession_widget_log.txt', 'r', "utf-8-sig") as fin:
	for line in fin:
		i += 1	
		if time.time() - start_time > 10: 
			print(i)
			start_time = time.time()		
				
		m = re.search("\(([0-9]+), '([^']+)', '([^']+)', datetime\.datetime\(([^\)]+)\), '([^']+)', ([0-9]+)\)", line)		
		
		try:			
			id, eventName, eventType, datetime, JSONParams, contextualInfoId = m.groups();
				
		except:
			print("cant parse")
			print(line)
			break
		
		JSONParams = JSONParams.replace('null', 'None')
		JSONParams = JSONParams.replace('true', 'True')
		JSONParams = JSONParams.replace('false', 'False')

		try:		
			if len(JSONParams) > 10:
				j += 1
				params = eval(JSONParams)
				def wrapper(x): 
					try: 
						a = str(x["logDetails"]["logEntries"])
						s.append(line)
					except: 
						pass
				
				if isinstance(params["logDetails"], list):
					for problem in params["logDetails"]:
						wrapper(params)
							
				elif isinstance(params["logDetails"], dict):
					wrapper(params)
				else:
					wrapper({"->"+str(params["logDetails"])+"<-": ""})
				#time.sleep(1)
				
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
with codecs.open('inputParams.txt', "w", 'utf-8-sig') as fout:				
	for string in s:
		print(string)
		fout.write(string)
		

"""print("printing set (size:{})".format(len(s)))
for string in s:
	print(string)"""