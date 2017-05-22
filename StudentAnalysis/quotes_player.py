"""
	script that removes unnesesary quotes
"""

import codecs
import re
import time

print("reading started")

start_time = time.time()
i = 0
j = 0
with codecs.open('slashes_player.txt', 'r', "utf-8-sig") as fin:	
	with codecs.open('logs_player.txt', 'w', "utf-8-sig") as fout:		
		for line in fin:
			i += 1
			if time.time() - start_time > 10: 
				print("i", i)
				start_time = time.time()
			
			line = line.replace('"[', '[')
			line = line.replace(']"', ']')
			
			line = line.replace('"Provjeri"', r'\"Provjeri\"')
			
			fout.write(line)

print(i, j)
	
print("reading finished")