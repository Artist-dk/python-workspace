# instagram password encrypter and decrypter

import urllib.parse
import hashlib
import base64

# Original string
original_string = 'abcdefgh'

# Step 1: URL encode the string
url_encoded_string = urllib.parse.quote(original_string)

# Step 2: Generate a hash (SHA-256) of the URL encoded string
hashed_string = hashlib.sha256(url_encoded_string.encode()).hexdigest()

# Step 3: Base64 encode the hash
base64_encoded_hash = base64.urlsafe_b64encode(hashed_string.encode()).decode().rstrip('=')

# Step 4: Construct the final encrypted form
encrypted_form = f'%23PWD_INSTAGRAM_BROWSER%3A10%3A1719242223%3A{base64_encoded_hash}'

print(encrypted_form)
