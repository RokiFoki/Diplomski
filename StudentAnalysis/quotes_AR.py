"""
	script removes unnesesary slashes that some logs have while others don't
"""

import codecs
import re
import time
from utils import get_file_name_from_dates

import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Removes unnesesary slashes that some logs might have.")
parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')
					
args = parser.parse_args()

dates = args.date

from pprint import pprint

print("reading started")

start_time = time.time()
with codecs.open(get_file_name_from_dates('download_AR', dates), 'r', "utf-8-sig") as fin:	
	with codecs.open(get_file_name_from_dates('logs_AR', dates), 'w', "utf-8-sig") as fout:		
		for i, line in enumerate(fin):
			line = line.replace('":""Lijepu našu" je napisao?"', '":"\\"Lijepu našu\\" je napisao?"')
			line = line.replace('"Tko je pokrenuo prve novine na hrvatskom jeziku "Novine horvatske" i prilog "Danica"?"', '"Tko je pokrenuo prve novine na hrvatskom jeziku \\"Novine horvatske\\" i prilog \\"Danica\\"?"')
			line = line.replace('"Koji politicar je pokrenuo "Novine horvatske"', '"Koji politicar je pokrenuo \\"Novine horvatske\\"')
			line = line.replace('""Ljubav i zloba" je opera koju je napisao?"', '"\\"Ljubav i zloba\\" je opera koju je napisao?"')
			line = line.replace('"Tko je pokrenuo "Novine horvatske", prve novine na hrvatskom jeziku?"', '"Tko je pokrenuo \\"Novine horvatske\\", prve novine na hrvatskom jeziku?"')
			
			fout.write(line)			
		
print("reading ended")