import re
import gc
import os
from itertools import permutations

# File paths
input_file = '../common/names.txt'
output_file_prefix = 'emails_batch'
domain = 'example.com'
batch_size = 1000  # Number of emails per batch file
batch_counter = 1  # Counter for batch files

def normalize_name(name):
    # Convert to lowercase and replace only the first space with a single dot
    name = name.lower().strip()
    name = re.sub(r'\s+', ' ', name)  # Ensure single spaces
    name_parts = name.split(' ', 1)  # Split only on the first space
    if len(name_parts) > 1:
        name = '.'.join(name_parts)
    else:
        name = name_parts[0]
    # Remove invalid characters except for allowed ones
    name = re.sub(r'[^\w\.]', '', name)
    return name

def generate_number_suffixes(max_length=10):
    # Generate numbers with lengths from 1 to max_length digits
    suffixes = []
    for length in range(1, max_length + 1):
        for number in range(10**(length - 1), 10**length):
            suffixes.append(str(number))
    return suffixes

def generate_email_variations(name, domain):
    # Split name into parts
    parts = name.split('.')
    variations = set()

    # Generate email addresses with a single dot or no dots
    base_email = '.'.join(parts)
    variations.add(f"{base_email}@{domain}")

    for num in generate_number_suffixes():
        variations.add(f"{base_email}{num}@{domain}")

    # Add variations by reversing parts if more than one part
    if len(parts) > 1:
        reversed_email = '.'.join(reversed(parts))
        variations.add(f"{reversed_email}@{domain}")
        for num in generate_number_suffixes():
            variations.add(f"{reversed_email}{num}@{domain}")

    return variations

def write_emails_to_file(emails, batch_number):
    output_file = f"{output_file_prefix}_{batch_number}.txt"
    with open(output_file, 'w') as outfile:
        for email in emails:
            outfile.write(email + '\n')
    print(f"Batch file {output_file} created.")

# Initialize
emails_buffer = []

# Read names from the input file and generate all possible emails
with open(input_file, 'r') as infile:
    for line in infile:
        name = line.strip()
        if name:
            normalized_name = normalize_name(name)
            emails = generate_email_variations(normalized_name, domain)
            
            # Write emails to the file in chunks
            for email in emails:
                emails_buffer.append(email)
                if len(emails_buffer) >= batch_size:
                    write_emails_to_file(emails_buffer, batch_counter)
                    emails_buffer = []  # Clear the buffer
                    batch_counter += 1
                    gc.collect()  # Request garbage collection

# Write any remaining emails in the buffer to the last batch file
if emails_buffer:
    write_emails_to_file(emails_buffer, batch_counter)

print("All possible email addresses have been generated and saved in batch files.")
