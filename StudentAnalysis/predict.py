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
import tensorflow as tf

parser = argparse.ArgumentParser(description="aproximates data collected from file with a Stanford-B model learning curve function and displays it")
parser.add_argument('type', help="type of lessons. Allowed types: collaborative, competitive, AR", type=str)
parser.add_argument('name', help="name of the student", type=str)
parser.add_argument('-lr', help="learning rate", type=float, default=0.01)
parser.add_argument('-te', help="number of training epoches", type=int, default=1000)
parser.add_argument('-ds', help="every 'display step' of iteration lost is displayed", type=float, default=100)
				
args = parser.parse_args()

type = args.type
name = args.name

learning_rate = args.lr
training_epochs = args.te
display_step = args.ds

file_type ={
	"collaborative" : "",
	"AR" : "_AR",
	"competitive" : "_player"
}

file_name = 'tmp/users/results/{}{}_real.txt'.format(name, file_type[type])
if os.path.isfile(file_name):
	with open(file_name) as fin:
		grades = np.array([float(line.strip().split(":")[1]) for line in fin.readlines()])
		indexes = np.arange(1, len(grades)+1)

		X = tf.placeholder(tf.float32)
		Y = tf.placeholder(tf.float32)

		C = tf.Variable(0.5, name="C")
		b = tf.Variable(-0.5, name="b")
		B = tf.Variable(0.0, name="B")

		C = tf.maximum(0.0, tf.minimum(1.0, C)) 
		b = tf.maximum(-1.0, tf.minimum(0.0, b))
		pred = tf.subtract(1.0, tf.scalar_mul(C, tf.pow(tf.add(X, B), b)))

		cost = tf.reduce_mean(tf.pow(Y-pred, 2))
		optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

		init = tf.global_variables_initializer()

		with tf.Session() as sess:
			sess.run(init)

			for epoch in range(training_epochs):
				for x, y in zip(indexes, grades):
					sess.run(optimizer, feed_dict={X: x, Y: y})

				if (epoch+1) % display_step == 0:
					c = sess.run(cost, feed_dict={X: indexes, Y: grades})
					print("Epoch {}: cost={}".format(epoch+1, c))
			
			C_trained, b_trained, B_trained = sess.run([C, b, B])

			plt.plot(indexes, grades, "ro", label="Original data")

			min_x = 1
			max_x = indexes[-1]+2
			x_range = np.arange(min_x, max_x+1)

			predicted = sess.run(pred, feed_dict={X: x_range})

			min_y = max(0, min(min(predicted), min(grades))-0.05)
			max_y = min(1, max(max(predicted), max(grades))+0.05)

			plt.plot(x_range, predicted, label="Trained data")	
			
			plt.axis([min_x, max_x, min_y, max_y])
			plt.legend(loc=0)
			plt.show()

			
			print("Trained parameters:")
			print("C:{}, b:{}, B:{}".format(C_trained, b_trained, B_trained))

else:
	print("file {} not found".format(file_name))