import os 

try:
    if os.mkdir("newDirectory"):
        print("new directory created!")
except:
    print("direcory already exist!")


# alternate for above

# if(os.path.exists("newDirectory")):
#     os.mkdir("newDirectory")
