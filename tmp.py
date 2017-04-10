import codecs
import re 
import time

print("reading started")

start_time = time.time()
i = 0
j = 0

data = set()

with codecs.open('inputParams.txt', 'r', "utf-8-sig") as fin:
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
				
				for name in params["logDetails"]["inputParams"]["groupMembers"]:
					data.add(name)
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

def fixStr(str):
	return str.replace("?8a", "Š").replace("?8e", "Ž").strip()

with codecs.open('groupMembers.txt', "w", "utf-8-sig") as fout:
	for d in data:
		fout.write(fixStr(d) + "\n");

