import codecs
import re
import time

print("reading started")

i = 0
j = 0

regex = r'(.*)<img([^>]+)([^\\>])"(.*)'
ct = r'\1<img\2\3\"\4'

start_time = time.time()

with codecs.open('logs_lession_preprocessed2.txt', 'r', "utf-8-sig") as fin:
	with codecs.open('logs_lession_preprocessed3.txt', 'w', "utf-8-sig") as fout:			
		for line in fin:
			if time.time() - start_time > 10: 
				print("j" , j)
				start_time = time.time()
			j += 1
			if "<img" in line:
				m = re.search(regex, line)
				if m:
					i += 1				
					
					if i % 5 == 0: print("i", i)
				
					k = 0
					while m:
						line = re.sub(regex, ct, line)						
						m = re.search(regex, line)
						
						k += 1
						
						if k > 1000:
							print(line)
							break
			
			
			fout.write(line)
			
print(i)
print("reading finished")	
