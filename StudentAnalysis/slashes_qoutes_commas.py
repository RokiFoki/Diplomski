import os 

def execute_python_script(name):
	print("executing {}".format(name))
	os.system("python {}".format(name))
	print()

execute_python_script("slashes.py")
execute_python_script("quotes.py")
execute_python_script("commas.py")