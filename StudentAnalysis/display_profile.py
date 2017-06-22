import os
import argparse
from utils import get_file_name_from_dates, execute_python_script
from datetime import datetime
import time
import codecs
import glob
from shutil import copyfile


import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="aproximates data collected from file with a Stanford-B model learning curve function and displays it")
parser.add_argument('name', help="name of the student", type=str)
parser.add_argument('-lr', help="learning rate", type=float, default=0.01)
parser.add_argument('-te', help="number of training epoches", type=int, default=1000)
parser.add_argument('-ds', help="every 'display step' of iteration lost is displayed", type=float, default=100)
				
args = parser.parse_args()

name = args.name

learning_rate = args.lr
training_epochs = args.te
display_step = args.ds

types = ["collaborative", "AR", "competitive"]

file_type ={
	"collaborative" : "",
	"AR" : "_AR",
	"competitive" : "_player"
}

grades {}

for type in types:
	file_name = 'tmp/users/results/{}{}_real.txt'.format(name, file_type[type])
	if os.path.isfile(file_name):
		with open(file_name) as fin:
			grades[type] = np.mean(np.array([float(line.strip().split(":")[1]) for line in fin.readlines()]))
	else:
		grades[type] = 0
		print("file {} not found".format(file_name))
		
