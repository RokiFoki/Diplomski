import glob
from datetime import datetime

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
	names.add(student_name)


names = sorted(names)
for student_name in names:
	if student_name not in table: table[student_name] = {}

	for file_name in glob.glob(first_part+student_name+"*"+second_part):
		_, log_type = get_name_and_type(file_name[starting_index:-ending_index])
		
		with open(file_name, "r") as f:
			for line in f:
				date, grade = line.strip().split(":")

				date_type = date+"_"+log_type
				date_types.add(date_type)

				table[student_name][date_type] = grade

date_types = sorted(date_types, key=lambda x: datetime.strptime(x.split("_")[0], '%d.%m.%Y'))


with open("data.csv", "w") as f:
	f.write("name")
	for date_type in date_types:
		f.write("," + date_type)

	f.write("\n")

	for student_name in names:
		f.write(student_name)
		for date_type in date_types:
			f.write(",{}".format(table[student_name].get(date_type, " ")))

		f.write("\n")


	

