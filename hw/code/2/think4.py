from swampy.TurtleWorld import *
from math import pi, sin

print "hello world"

def square(t, length):
	for i in range(4):
		fd(t, length)
		lt(t)	

def polygon(t, length, n, angle=360.0):
	for i in range(n):
		fd(t, length)
		lt(t, angle/n)

def circle(t, r):
	n = 100
	circumference = 2*r*pi
	length = circumference / float(n)
	print length, circumference
	polygon(t, length, n)

def arc(t, r, angle):
	n = 100
	circumference = 2*r*pi
	length = circumference / float(n)
	polygon(t, length, n, angle=angle)



# Exercise 2

def petal(t, r, angle):
	for i in xrange(2):
		arc(t, r, angle)
		lt(t, 180-angle)

def flower(t, num_petals, r, angle):
    for i in range(num_petals):
        petal(t, r, angle)
        lt(t, 360.0/num_petals)
# Exercise 3

def pie(t, length, n):
	polygon(t, length, n)
	radius = 0.5*length / sin(pi / n)
	turn_angle = 180 - 360.0/n

	lt(t, 0.5*turn_angle)
	fd(t, radius)
	lt(t, turn_angle)
	for i in xrange(n-1):
		fd(t, radius)
		lt(t, 180)
		fd(t, radius)
		lt(t, turn_angle)





world = TurtleWorld()
bob = Turtle()
bob.delay = 0.01
print bob

#square(bob, 100)
#polygon(bob, 100, 6)
#circle(bob, 50)
#arc(bob, 25, 70.0)
#pie(bob, 140,5)
flower(bob, 15, 25, 70.0)

wait_for_user()