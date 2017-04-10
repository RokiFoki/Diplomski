import codecs

print("reading started")

i = 0
with codecs.open('logs_lession.txt', 'r', "utf-8-sig") as fin:	
	with codecs.open('logs_lession_preprocessed1.txt', 'w', "utf-8-sig") as fout:	
		for line in fin:
			if len(line) > 60:				
				line = line.replace('\\x', '?')	 # hrvatski znakovi smetaju pri jsonizaciji
				fout.write(line)
				
				if i % 5000 == 0: print(i)
				i += 1
	
print(i)	
print("reading finished")