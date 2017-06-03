"""
	script that removes unnesesary quotes
"""

import codecs
import re
import time
from utils import get_file_name_from_dates

import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="removes unnesesary quotes.")
parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')
					
args = parser.parse_args()

dates = args.date

print("reading started")

start_time = time.time()
i = 0
j = 0
with codecs.open(get_file_name_from_dates('slashes_collaborative', dates), 'r', "utf-8-sig") as fin:	
	with codecs.open(get_file_name_from_dates('quotes_collaborative', dates), 'w', "utf-8-sig") as fout:		
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