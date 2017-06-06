import os
import argparse
from utils import get_file_name_from_dates, execute_python_script
from datetime import datetime
import time
import codecs
import glob
from shutil import copyfile


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="")
parser.add_argument('type', help="types of lessons", type=str)

parser.add_argument('name', help="name of the student", type=str)
					
args = parser.parse_args()
type = args.type
name = args.name

learning_rate = 0.01
training_epochs = 1000
display_step = 50



file_name = 'tmp/users/results/{}_{}_real.txt'.format(name, type)
if os.path.isfile(file_name.format(name, type)):
	with open(file_name) as fin:
		grades = np.array([line.strip().split(":")[1] for line in fin.readlines()])
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
			plt.plot(indexes, sess.run(pred, feed_dict={X: indexes, Y: grades}), label="Trained data")	
			plt.legend()
			plt.show()

		