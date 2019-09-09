import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def findMin(x,l=0.001):
	lamb = l
	count = 0
	while len_grad_f(x[0], x[1]) > 10**-8:
		count += 1
		x = x - (lamb * grad(x[0], x[1]))
	return count

def f(x, y):
	return (4 * (x ** 2)) - (3 * x * y) + (2 * (y ** 2)) + (24 * x) - (20 * y)
	#return ((1 - y) ** 2) + (100 * ((x - (y ** 2)) ** 2))

def grad(x, y):
	return np.array([(8 * x) - (3 * y) + 24, (-3 * x) + (4 * y) - 20])
	#return np.array([200 * (x - (y ** 2)), (-2 * (1 - y)) + (200 * (x - (y ** 2)) * (-2 * y))])

def len_grad_f(x, y):
	temp = grad(x, y)
	return ((temp[0] ** 2) + (temp[1] ** 2)) ** 0.5

x, y = [], []
for a in np.linspace(0.001, 0.01, 100):
	xy = findMin(np.array([1, 0]), a)
	x.append(a)
	y.append(xy)
	plt.plot(x,y)
	print(xy)
plt.savefig('graph.png')
