# Employee Class
class Employee(object):
	def __init__(self, name, age):
		self.name = name
		self.age = age

	def __repr__(self):
		return "%s (age %s)" % (self.name, self.age)

	def __lt__(self, other):
		return self.age < other.age

fred = Employee("Fred", 40)
bill = Employee("Bill", 39)
jan = Employee("Jan", 50)

x = [fred, bill, jan]
print "Original list: ", x
print "Sorted list: ", sorted(x)