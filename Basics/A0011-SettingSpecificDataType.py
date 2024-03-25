x = str("Hello World")
print("Line 01: ",type(x))

x = int(20)
print("Line 02: ",type(x))

x = float(20.5)
print("Line 03: ",type(x))

x = complex(1j)
print("Line 04: ",type(x))

x = list(("Apple", "Banana", "Cherry"))
print("Line 05: ",type(x))

x = tuple(("Apple","Banana","Cherry"))
print("Line 06: ",type(x))

x = range(6)
print("Line 07: ",type(x))

x = dict(name="Artist", age=22)
print("Line 08: ",type(x))

x = set(("Apple", "Banana", "Cherry"))
print("Line 09: ",type(x))

x = frozenset(("Apple", "Banana", "Cherry"))
print("Line 10: ",type(x))

x = bool(5)
print("Line 11: ",type(x))

x = bytes(5)
print("Line 12: ",type(x))

x = bytearray(5)
print("Line 13: ",type(x))

x = memoryview(bytes(5))
print("Line 14: ",type(x))
