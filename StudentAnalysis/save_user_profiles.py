import glob
from datetime import datetime
from utils import execute_python_script

first_part = "tmp/users/results/"
second_part = "_real.txt"


starting_index = len(first_part)
ending_index = len(second_part)


def get_name_and_type(oname):
	name = oname[:]
	if name.endswith("_AR"):
		log_type = "AR"
		name = name[:-3]
	elif name.endswith("_player"):
		log_type = "competitive"
		name = name[:-7]
	else:
		log_type = "collaborative"

	return name, log_type


names = set()
date_types = set()
table = {}


for file_name in glob.glob(first_part+"*"+second_part):
	file_name = file_name[starting_index:-ending_index]

	student_name, log_type = get_name_and_type(file_name)
	
	if " " in student_name:
		names.add(student_name)


execute_python_script("display_profile.py", ['"{}"'.format(name) for name in names])

	

