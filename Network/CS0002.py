# password cracker

import hashlib

type_of_hash = str(input("Which thype of hash you want to bruteforce ?"))
file_path = str(input("Enter path to the file to bruteforce with: "))
hash_to_decrypt = str(input("Enter hash value to bruteforce:"))

with open(file_path, 'r') as file:
    for line in file.readlines():
        if type_of_hash == 'md5':
            hash_object = hashlib.md5(line.strip().encode())
            hashed_word = hash_object.hexdigest()
            if hashed_word == hash_to_decrypt:
                print('Found MD5 Password: ' + line.strip())
                exit(0)

# 8750307bd8b11fe6f9d319283986d121 == getpass
# 5f4dcc3b5aa765d61d8327deb882cf99 == password