import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def min_f(x, l=0.001):
	lmbda = l
	count = 0
	while len_grad_f(x[0], x[1]) > 10 ** -8:
		count += 1
		x = x - (lmbda * grad_f(x[0], x[1]))
	return count

def f(x, y):
	return ((1 - y) ** 2) + (100 * ((x - (y ** 2)) ** 2))
	# return (4 * (x ** 2)) - (3 * x * y) + (2 * (y ** 2)) + (24 * x) - (20 * y)

def grad_f(x, y):
	#return np.array([200 * (x - (y ** 2)), (-2 * (1 - y)) + (200 * (x - (y ** 2)) * (-2 * y))])
	return np.array([(8 * x) - (3 * y) + 24, (-3 * x) + (4 * y) - 20])

def len_grad_f(x, y):
	temp = grad_f(x, y)
	return ((temp[0] ** 2) + (temp[1] ** 2)) ** 0.5

def main():
	x_vals, y_vals = [], []
	for i in np.linspace(0.001, 0.01, 1000):
		count = min_f(np.array([1, 0]), i)
		x_vals.append(i)
		y_vals.append(count)
		#print(i, count)
	plt.plot(x_vals, y_vals)
	plt.show()
	print("Done")
	#plt.savefig('grad.png')
	#os.system('open grad.png')

main()
