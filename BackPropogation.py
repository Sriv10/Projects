import random
import numpy
import itertools
from progress.bar import Bar


def padbin(x,n):
    temp = "0%sb" % (n)
    binString = format(x, temp)
    return binString

def makeCircleTs(squareSize):
	locX = -squareSize
	locY = -squareSize
	incr = (squareSize * 2) / 100
	final = []
	for x in range(100):
		for y in range(100):
			result = 0
			loc = pow(locX,2) + pow(locY,2)
			if (loc <= 1):
				result = 1
			tup = numpy.array(([locX,locY])), result
			final.append(tup)
			locY+=incr
		locY = -squareSize
		locX+=incr
	return final

def makeTs(len, num):
    final = []
    num = padbin(num, pow(2, len))
    counter = 0
    for l in (itertools.product([0,1], repeat = len)):
        tup = numpy.array(list(l)), int(num[counter])
        final.append(tup)
        counter+=1
    return ((final))

def sigmoid(val):
	return 1.0 / (1.0 + numpy.exp(-val))

def sigmoidDeriv(val):
	return numpy.multiply(sigmoid(val),(1 - sigmoid(val)))

def backProp(ts):
	w0 = (numpy.random.rand(2,2))
	w1 = (numpy.random.rand(2,1))
	b1 = (numpy.random.rand(2,2))
	b2 = (numpy.random.rand(2,1))
	weights = [w0,w1]
	bias = [b1,b1,b2]
	deltas = [w0,w1,w1]
	dots = [w0,w1,w1]
	lamb = 1
	count = 1
	results = []
	temp_error = 0
	for epochs in range(1000):
		temp_error = 0
		results = []
		for x,output in ts:
			a = []
			dots = []
			a.append(x)
			dots.append(x)
			for index in range(1,len(weights) + 1): #len 2
				dots.append(numpy.add(numpy.dot(a[index-1], weights[index-1]),bias[index]))
				print("index " + str(bias[index]))
				a.append(sigmoid(dots[index]))
			deltas[2] = sigmoidDeriv(dots[2]) * (a[2] - output)
			#print(a[2] - output)
			#temp_error+=(a[2] - output)
			#print(deltas[2])
			while (count > 0):
				deltas[count] = sigmoidDeriv(dots[count]) * numpy.dot(deltas[count+1] , weights[count].T)
				count-=1
			for l in range(0,len(weights)):
				weights[l] = weights[l] + lamb * numpy.dot(a[l+1].T,deltas[l+1])
				bias[l+1] = bias[l+1] + lamb * deltas[l+1]
			results.append(a[2])
		#print(temp_error/4)
		'''
			temp_error += (a[length] - output) ** 2
			#Back Prop
			deltas[3] = sigmoidDeriv(dots[-2]) * (output - a[length])
			print(dots[-2].shape)
			while (count > -1):
				#print(dots[count].shape, deltas[count+1].shape, weights[count].shape)
				deltas[count] = numpy.dot(sigmoidDeriv(dots[count]) * (deltas[count+1]),weights[count].T)
				count-=1
			for l in range(0,3):
				weights[l] = weights[l] + lamb * numpy.dot(a[-1].T,deltas[l+1])
				# print(weights)
		print("Learning Error: " + str((temp_error)))
		temp_error = 0
		'''
	return weights, results

def backPropDifWay(ts):
	w0 = (numpy.random.uniform(-1,1, (2,2)))
	w1 = numpy.random.uniform(-1,1, (2,1))
	b0 = numpy.random.uniform(-1,1, (1,2))
	b1 = numpy.random.uniform(-1,1, (1,1))
	lamb = 5
	error = 0
	bar = Bar("Learning", suffix="Iterations: %(index)d/%(max)d, Elapsed: %(elapsed_td)s, %(error)s")
	bar.error = error
	for epochs in bar.iter(range(500000)):
		output = numpy.matrix([numpy.array(y) for x,y in ts]).T
		a0 = numpy.matrix([x for x,y in ts])
		dot1 = numpy.dot(a0,w0) + b0
		a1 = sigmoid(dot1)
		dot2 = numpy.dot(a1,w1) + b1
		a2 = sigmoid(dot2)
		delta1 = numpy.multiply(sigmoidDeriv(dot2),(output-a2))
		delta0 = numpy.multiply(sigmoidDeriv(dot1),numpy.dot(delta1, w1.T))
		w0 = w0 + lamb * numpy.dot(a1.T, delta0)
		w1 = w1 + lamb * numpy.dot(a2.T, delta1)
		b0 = b0 + lamb * delta0
		b1 = b1 + lamb * delta1
		bar.error = sum(abs(a2 - output)) / 4
	print(delta0.shape, delta1.shape)
	print(w0.shape,w1.shape)
	return (a2)


checkSet = makeTs(2,6)
output = backPropDifWay(checkSet)
print(output)
