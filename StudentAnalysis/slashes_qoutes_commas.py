import os 
from utils import get_file_name_from_dates
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="?????.")

parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')
args = parser.parse_args()
dates = args.date

def execute_python_script(name, params):
	print("executing {} {}".format(name, " ".join([str(param) for param in params])))
	os.system("python {} {}".format(name, " ".join([str(param) for param in params])))
	print()

execute_python_script("slashes.py", [date.strftime("%d.%m.%Y") for date in dates])
execute_python_script("quotes.py", [date.strftime("%d.%m.%Y") for date in dates])
execute_python_script("commas.py", [date.strftime("%d.%m.%Y") for date in dates])