import os

command = "python3"

def execute_python_script(name, params):
	global command
	
	print("executing {} {}".format(name, " ".join([str(param) for param in params])))
	exit_status = os.system("{} {} {}".format(command, name, " ".join([str(param) for param in params])))
	if exit_status: # check both python3 and python
		if command != "python":
			command = "python"
			execute_python_script(name, params)
		else:
			exit(1)
	print("")

def get_file_name_from_dates(base_name, dates, prefix="logs/", suffix=".txt"):
	return "{}{}_{}{}".format(
		prefix,
		base_name,
		dates[0].strftime("%d-%m-%Y") if len(dates) == 1 else 
		"{}-{}_({})".format(dates[0].strftime("%d-%m-%Y"), dates[-1].strftime("%d-%m-%Y"), len(dates)),
		suffix
	)