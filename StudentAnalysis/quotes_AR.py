"""
	script removes unnesesary slashes that some logs have while others don't
"""

import codecs
import re
import time

from pprint import pprint

print("reading started")

start_time = time.time()
with codecs.open('download_AR.txt', 'r', "utf-8-sig") as fin:	
	with codecs.open('logs_AR.txt', 'w', "utf-8-sig") as fout:		
		for i, line in enumerate(fin):
			line = line.replace('":""Lijepu našu" je napisao?"', '":"\\"Lijepu našu\\" je napisao?"')
			line = line.replace('"Tko je pokrenuo prve novine na hrvatskom jeziku "Novine horvatske" i prilog "Danica"?"', '"Tko je pokrenuo prve novine na hrvatskom jeziku \\"Novine horvatske\\" i prilog \\"Danica\\"?"')
			line = line.replace('"Koji politicar je pokrenuo "Novine horvatske"', '"Koji politicar je pokrenuo \\"Novine horvatske\\"')
			line = line.replace('""Ljubav i zloba" je opera koju je napisao?"', '"\\"Ljubav i zloba\\" je opera koju je napisao?"')
			line = line.replace('"Tko je pokrenuo "Novine horvatske", prve novine na hrvatskom jeziku?"', '"Tko je pokrenuo \\"Novine horvatske\\", prve novine na hrvatskom jeziku?"')
			
			fout.write(line)			
		
print("reading ended")