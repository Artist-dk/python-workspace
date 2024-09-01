# config.py

# Configuration for wordlist generation
min_length = 6
max_length = 7
characters = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
wordlist_directory = '/home/kernel/Desktop/Wordlists/email/'  # Update to a valid directory path

# Configuration for email generation
input_file = '../common/names.txt'
output_file = '../common/emails.txt'
domain = '../common/example.com'  # Default domain for email generation

# Progress message settings
batch_size = 10000000  # Number of entries per batch in wordlist generation
