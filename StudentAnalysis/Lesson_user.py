import os 
import sys
import time

if len(sys.argv) > 1: n = int(sys.argv[1])
else: print("Number of iterations needed"); exit()

print("running {} iterations".format(n))

if len(sys.argv) > 2: display_each = int(sys.argv[2])
else: display_each = 1

print("displaying each {} iteration".format(display_each))
if len(sys.argv) > 3:
	if sys.argv[3] == "0": 
		display_users = False
		display_lessons = False
	elif sys.argv[3] == "1":
		display_users = True
		display_lessons = False
	elif sys.argv[3] == "2":
		display_users = False
		display_lessons = True
	else:
		display_users = True
		display_lessons = True
else:
	display_users = True
	display_lessons = True
	
print("displaying users:{} displaying lessons:{}".format(display_users, display_lessons))

def execute_python_script(name):
	print("executing {}".format(name))
	os.system("python {}".format(name))
	print()

for i in range(n):
	print("iteration {} started".format(i+1))
	parameter = ' lessons_{}'.format(i+1) if display_lessons and i % display_each == 0 else ''
	execute_python_script("analyseLessons.py" + parameter) #USE THE ONE FROM import utils!!!!!!!!!!!!!!!!!!!
	
	parameter = ' users_{}'.format(i+1) if display_users and i % display_each == 0 else ''
	execute_python_script("analyseUsers.py" + parameter)