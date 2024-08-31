# email_generator.py

import re
import os
import gc
import time
import config  # Import configuration settings
from email_progress import EmailProgressMsg  # Import EmailProgressMsg for progress updates


def normalize_name(name):
    """
    Normalize the name by converting it to lowercase, removing extra spaces, 
    and replacing the first space with a dot. Remove any invalid characters.
    """
    name = name.lower().strip()
    name = re.sub(r'\s+', ' ', name)  # Ensure single spaces
    name_parts = name.split(' ', 1)  # Split only on the first space
    if len(name_parts) > 1:
        name = '.'.join(name_parts)
    else:
        name = name_parts[0]
    name = re.sub(r'[^\w\.]', '', name)  # Remove invalid characters except for allowed ones
    return name

def generate_number_suffixes(max_length=10):
    """
    Generate number suffixes for email addresses up to a specified length.
    """
    suffixes = []
    for length in range(1, max_length + 1):
        for number in range(10**(length - 1), 10**length):
            suffixes.append(str(number))
    return suffixes

def generate_email_variations(name):
    """
    Generate variations of email addresses using the provided name and domain.
    """
    parts = name.split('.')
    variations = set()

    # Generate email addresses with a single dot or no dots
    base_email = '.'.join(parts)
    variations.add(f"{base_email}@{config.domain}")

    # Add variations with number suffixes
    for num in generate_number_suffixes():
        variations.add(f"{base_email}{num}@{config.domain}")

    # Add variations by reversing parts if more than one part
    if len(parts) > 1:
        reversed_email = '.'.join(reversed(parts))
        variations.add(f"{reversed_email}@{config.domain}")
        for num in generate_number_suffixes():
            variations.add(f"{reversed_email}{num}@{config.domain}")

    return variations

def save_emails_to_file(emails, directory, base_filename, batch_index):
    """
    Save a batch of emails to a file and return the filename.
    """
    os.makedirs(directory, exist_ok=True)
    filename = f'{directory}/{base_filename}_{batch_index}.txt'
    with open(filename, 'w') as file:
        file.write('\n'.join(emails))
    return filename

def clear_memory():
    """
    Clear memory by triggering garbage collection.
    """
    gc.collect()

def generate_emails(characters, min_length, max_length, directory, progress):
    """
    Generate email addresses from names in an input file and save to an output file in batches.
    Show progress updates during the generation process.
    """
    batch_size = config.batch_size
    batch_index = 1
    current_batch = []
    wordcount = 0  # Track the number of emails generated

    total_lines = sum(1 for line in open(config.input_file))  # Total names in the input file
    progress.total_combinations = total_lines * (2 * len(generate_number_suffixes()))  # Estimate total combinations

    start_time = time.time()

    with open(config.input_file, 'r') as infile:
        for line in infile:
            name = line.strip()
            if name:
                normalized_name = normalize_name(name)
                emails = generate_email_variations(normalized_name)
                current_batch.extend(emails)
                wordcount += len(emails)  # Update the word count

                if len(current_batch) >= batch_size:
                    save_emails_to_file(current_batch, directory, 'emails', batch_index)
                    clear_memory()  # Clear memory after saving each batch
                    current_batch = []  # Reset the batch
                    batch_index += 1

                # Update progress every 100,000 emails
                if wordcount % 100000 == 0:
                    progress.batch_index = batch_index
                    progress.wordcount = wordcount
                    progress.elapsed_time = time.time() - start_time
                    progress.update_remaining_time_chunks(
                        (progress.elapsed_time / (progress.wordcount / progress.total_combinations)) - progress.elapsed_time
                    )
                    progress.filename = f'{directory}/emails_{batch_index}.txt'
                    progress.calculate_used_storage(os.path.getsize(progress.filename))
                    progress.generate_progress_msg()
                    progress.print_progress()

        # Save any remaining emails in the last batch
        if current_batch:
            save_emails_to_file(current_batch, directory, 'emails', batch_index)
            clear_memory()

    # Final progress message after completion
    progress.batch_index = batch_index
    progress.wordcount = wordcount
    progress.elapsed_time = time.time() - start_time
    progress.update_remaining_time_chunks(
        (progress.elapsed_time / (progress.wordcount / progress.total_combinations)) - progress.elapsed_time
    )
    progress.filename = f'{directory}/emails_{batch_index}.txt'
    progress.calculate_used_storage(os.path.getsize(progress.filename))
    progress.generate_progress_msg()
    progress.print_progress()

    print(f"All possible email addresses have been generated and saved in batches to {directory}.")

# Call the function if needed to generate emails independently
if __name__ == "__main__":
    generate_emails(config.characters, config.min_length, config.max_length, config.wordlist_directory, None)
