x = "Hello World"
print("Line 1: ",type(x))

x = 20
print("Line 2: ",type(x))

x = 20.5
print("Line 3: ",type(x))

x = 1j 
print("Line 4: ",type(x))

x = ["apple", "banana", "cherry"]
print("Line 5: ",type(x))

x = ("apple", "banana", "cherry")
print("Line 6: ",type(x))

x = range(6)
print("Line 7: ",type(x))

x = {"Name" : "Artist", "Age":22} 
print("Line 8: ",type(x))

x = {"apple","banana","cherry"}
print("Line 9: ",type(x))

x = frozenset({"apple", "banana", "cherry"})
print("Line 10: ",type(x))

x = True
print("Line 11: ",type(x))

x = b"Hello"
print("Line 12: ",type(x))

x = bytearray(5)
print("Line 13: ",type(x))

x = memoryview(bytes(5))
print("Line 14: ",type(x))

x = None
print("Line 15: ",type(x))