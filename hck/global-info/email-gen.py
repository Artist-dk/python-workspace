import re
from itertools import permutations

# File paths
input_file = 'names.txt'
output_file = 'emails.txt'
domain = 'example.com'

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

# Read names from the input file and generate all possible emails
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        name = line.strip()
        if name:
            normalized_name = normalize_name(name)
            emails = generate_email_variations(normalized_name, domain)
            for email in emails:
                outfile.write(email + '\n')

print(f"All possible email addresses have been generated and saved to {output_file}.")
