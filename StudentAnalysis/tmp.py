import codecs
import time
import re

d = dict()

start_time = time.time()
with codecs.open('logs_collaborative.txt', 'r', "utf-8-sig") as fin:
	for i, line in enumerate(fin):
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
			
		#params = eval(JSONParams)
		
		if "A:" in JSONParams or "E:" in JSONParams or "C:" in JSONParams:
			try:
				m = re.search(".*(\[.*;[^]]*\]).*", JSONParams)
			
				upitno = m.group(1)
				upitno2 = upitno[2:-2].split(";")
				
				n = len(upitno2)
				upitno2 = upitno2[0: n//2]
				
				
				d[str(upitno2)] = upitno
			except AttributeError:
				pass
				
				
print("prining dict (size: {})".format(len(d)))
for key in d:
	print(key, d[key])
	print()