import time
from ok import *

print time.strftime("%H:%M:%S\n")

@ok
def _ok():
  assert 9 == 3
  
@ok
def _ok1():
  assert 1==1

@ok
def _ok2():
  assert 2==1

@ok
def _ok3():
  assert 3==3 

@ok
def _ok4():
  assert unittest.tries==4
  assert unittest.fails==1
  print unittest.score() 

@ok
def _okRegular():
  assert 0 == False
  assert 1 == True

@ok
def _okFunFact():
  # Fun fact: boolean is a subclass of int in Python 2.7
  # Python 3 changed it to a keyword to avoid this problem
  False = True
  assert 0 == False
  assert 1 == True