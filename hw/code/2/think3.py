# Exercise 1
repeat_lyrics()

def print_lyrics():
    print "I'm a lumberjack, and I'm okay."
    print "I sleep all night and I work all day."

def repeat_lyrics():
    print_lyrics()
    print_lyrics()


# Exercise 2
def repeat_lyrics():
    print_lyrics()
    print_lyrics()

def print_lyrics():
    print "I'm a lumberjack, and I'm okay."
    print "I sleep all night and I work all day."

repeat_lyrics()


# Exercise 3
def right_justify(s):
	print " " * (70-len(s)) + s
right_justify("allen")

# Exercise 4
# Part 1
def do_twice(f):
	f()
	f()
def print_spam():
	print 'spam'
do_twice(print_spam)

# Part 2
def do_twice(f, x):
	f(x)
	f(x)

# Part 3
def print_twice(s):
	print s
	print s

# Part 4
do_twice(print_twice, "spam")

# Part 5
def do_four(f, v):
	do_twice(f, v)
	do_twice(f, v)


# Exercise 5
def generateGrid(cellWidth, cellHeight, numCols, numRows):
	rowOuterFragment = "+ " + "- "*cellWidth 
	rowOuter = rowOuterFragment*numCols + "+\n"
	rowInnerFragment = "| " + "  "*cellWidth
	rowInner = rowInnerFragment*numCols + "|\n"
	cell = rowOuter + rowInner*cellHeight
	grid = cell*numRows+rowOuter
	return grid

# Part 1
print generateGrid(4, 4, 2, 2), "\n\n"

# Part 2
print generateGrid(4, 4, 4, 4)