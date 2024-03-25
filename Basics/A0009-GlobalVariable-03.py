y = "Apple"

def myfunc():
  global x # declaration of global variable x
  x = 'fantastic'
  global y
  y = "Cherry" # change the value of global variable y

myfunc()

print("python is " + x)
print("Name of fruit: " + y)


'''
def myfunc2():
  y = 'awesome'

myfunc2()

print("Python is " + y)
'''