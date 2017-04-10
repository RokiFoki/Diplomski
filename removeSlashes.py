import codecs
import re

print("reading started")

i = 0
j = 0

with codecs.open('logs_lession_preprocessed1.txt', 'r', "utf-8-sig") as fin:	
	with codecs.open('logs_lession_preprocessed2.txt', 'w', "utf-8-sig") as fout:		
		for line in fin:
			if "\\" in line:
				while "\\\"" in line: line = re.sub(r'\\\"', "\"", line)
				
				# while "\\\\n" in line: line = re.sub(r'\\\\n', "\\n", line) this will add more lines! no!
				
				i += 1
				if i % 100 == 0: print("i", i)
				
			fout.write(line)
		
			j += 1
			if j % 5000 == 0: print("j", j)
print(i)	
print("reading finished")