import os 

def execute_python_script(name):
	print("executing {}".format(name))
	os.system("python {}".format(name))
	print()

execute_python_script("slashes_player.py")
execute_python_script("quotes_player.py")
execute_python_script("filter_player.py")