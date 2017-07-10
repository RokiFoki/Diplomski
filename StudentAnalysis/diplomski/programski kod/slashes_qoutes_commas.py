import os 
from utils import get_file_name_from_dates, execute_python_script
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="Executes slashes.py quotes.py and commas.py with given dates.")

parser.add_argument('date', help="dates (dd.mm.YYYY)", type=lambda x: datetime.strptime(x, '%d.%m.%Y'), nargs='+')
args = parser.parse_args()
dates = args.date

execute_python_script("slashes.py", [date.strftime("%d.%m.%Y") for date in dates])
execute_python_script("quotes.py", [date.strftime("%d.%m.%Y") for date in dates])
execute_python_script("commas.py", [date.strftime("%d.%m.%Y") for date in dates])