with open('student.txt') as f:
    data = f.read()
    print(data)
    print(f.closed)
print(f.closed)