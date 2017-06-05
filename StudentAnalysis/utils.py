import os

def execute_python_script(name, params):
	print("executing {} {}".format(name, " ".join([str(param) for param in params])))
	os.system("python {} {}".format(name, " ".join([str(param) for param in params])))
	print()

def get_file_name_from_dates(base_name, dates, prefix="logs/", suffix=".txt"):
	return "{}{}_{}{}".format(
		prefix,
		base_name,
		dates[0].strftime("%d-%m-%Y") if len(dates) == 1 else 
		"{}-{}_({})".format(dates[0].strftime("%d-%m-%Y"), dates[-1].strftime("%d-%m-%Y"), len(dates)),
		suffix
	)