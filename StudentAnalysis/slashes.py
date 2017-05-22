"""
	script removes unnesesary slashes that some logs have while others don't
"""

import codecs
import re
import time

print("reading started")

regex = r'(.*)<img([^>]+)([^\\>])"(.*)'
ct = r'\1<img\2\3\"\4'

i = 0
i2 = 0
j = 0
start_time = time.time()
with codecs.open('download_collaborative.txt', 'r', "utf-8-sig") as fin:	
	with codecs.open('slashes_collaborative.txt', 'w', "utf-8-sig") as fout:		
		for line in fin:
			j += 1
			if time.time() - start_time > 10: 
				print("i", i)
				print("j", j)
				
				start_time = time.time()
			
			if "\\" in line:
				while "\\\"" in line: line = re.sub(r'\\\"', "\"", line)
				
				i += 1
				
			if "<img" in line:
				m = re.search(regex, line)
				if m:
					i2 += 1				
					
					if i2 % 5 == 0: print("i", i2)
				
					k = 0
					while m:
						line = re.sub(regex, ct, line)						
						m = re.search(regex, line)
						
						k += 1
						
						if k > 1000:
							print(line)
							break
				
			fout.write(line)
print(i, j)	
print("reading finished")