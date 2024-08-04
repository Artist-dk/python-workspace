import os

for i in range(0, 100):
    os.rename(f"newDirectory/file_{i+1}.txt", f"rnFile_{i+1}")