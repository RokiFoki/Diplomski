from utils import execute_python_script

#execute_python_script("controller.py", ["-f", 10, "-t", 10, "AR", "1.1.2016", "10.10.2017"])
#execute_python_script("controller.py", ["-e", "AR", "1.1.2016", "10.10.2017"])

#execute_python_script("controller.py", ["-f", 10, "-t", 10, "collaborative", "1.1.2016", "10.10.2017"])
#execute_python_script("controller.py", ["-e", "collaborative", "1.1.2016", "10.10.2017"])

execute_python_script("controller.py", ["-f", 10, "-t", 10, "competitive", "1.1.2016", "10.10.2017"])
execute_python_script("controller.py", ["-e", "competitive", "1.1.2016", "10.10.2017"])


execute_python_script("save_user_profiles.py", "28.6.2017")

