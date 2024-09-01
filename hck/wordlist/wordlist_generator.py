# wordlist_generator.py

import itertools
import os
import gc
import sys
import time
import config  # Import configuration settings
from progress_msg import ProgressMsg

def generate_wordlist(characters, min_length, max_length, wordlist_directory, progress):
    """
    Generate a wordlist of all possible combinations of the given characters 
    with lengths between min_length and max_length and save in batches.
    """
    wordcount = 0
    batchcount = 0
    batch_index = 1
    used_storage = 0

    progress.total_combinations = sum(len(characters) ** length for length in range(min_length, max_length + 1))
    progress.calculate_required_storage_size(min_length, max_length, progress.total_combinations)

    current_batch = []
    start_time = time.time()

    for length in range(min_length, max_length + 1):
        for combination in itertools.product(characters, repeat=length):
            word = ''.join(combination).strip()
            wordcount += 1
            current_batch.append(word)

            if len(current_batch) == config.batch_size:
                filename = save_wordlist_to_file(current_batch, wordlist_directory, 'wordlist', batch_index)
                clear_memory()
                current_batch = []
                batch_index += 1
                batchcount += 1
                progress.filename = filename
                progress.calculate_used_storage(used_storage)

            if wordcount % 100000 == 0:
                progress.batch_index = batch_index
                progress.wordcount = wordcount
                progress.elapsed_time = time.time() - start_time
                progress.update_remaining_time_chunks(
                    (progress.elapsed_time / (progress.wordcount / progress.total_combinations)) - progress.elapsed_time
                )
                sys.stdout.write('\033[F\033[K' * 19)
                sys.stdout.write(progress.progress_msg)
                sys.stdout.flush()

    if current_batch:
        filename = save_wordlist_to_file(current_batch, wordlist_directory, 'wordlist', batch_index)
        clear_memory()
        batchcount += 1
        progress.filename = filename

    progress.batch_index = batch_index
    progress.wordcount = wordcount
    progress.elapsed_time = time.time() - start_time
    progress.update_remaining_time_chunks(
        (progress.elapsed_time / (progress.wordcount / progress.total_combinations)) - progress.elapsed_time
    )
    progress.calculate_used_storage(used_storage)
    sys.stdout.write('\033[F\033[K' * 25)
    sys.stdout.write(progress.progress_msg)
    sys.stdout.flush()

def save_wordlist_to_file(wordlist, wordlist_directory, base_filename, batch_index):
    """
    Save the current batch of words to a file and return the filename.
    """
    os.makedirs(wordlist_directory, exist_ok=True)
    filename = f'{wordlist_directory}/{base_filename}_{batch_index}.txt'
    with open(filename, 'w') as file:
        file.write('\n'.join(wordlist))
    return filename

def clear_memory():
    """
    Clear memory by triggering garbage collection.
    """
    gc.collect()
