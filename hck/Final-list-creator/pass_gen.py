import itertools
import os
import gc
import time
import sys
from pass_progress import ProgressMsg
from config import min_length, max_length, characters, wordlist_directory

wordcount = 0
batchcount = 0
used_storage = 0

def generate_wordlist():
    global wordcount
    global batchcount
    global used_storage

    progress = ProgressMsg()
    progress.total_combinations = sum(len(characters) ** length for length in range(min_length, max_length + 1))
    progress.calculate_required_storage_size(min_length, max_length, progress.total_combinations)

    batch_size = 10000000
    current_batch = []
    batch_index = 1

    start_time = time.time()

    for length in range(min_length, max_length + 1):
        for combination in itertools.product(characters, repeat=length):
            word = ''.join(combination).strip()
            wordcount += 1
            current_batch.append(word)

            if len(current_batch) == batch_size:
                save_wordlist_to_file(current_batch, 'wordlist', batch_index)
                clear_memory()
                current_batch = []
                batch_index += 1
                batchcount += 1

            if wordcount % 100000 == 0:
                progress.batch_index = batch_index
                progress.wordcount = wordcount
                progress.elapsed_time = time.time() - start_time
                progress.update_remaining_time_chunks(
                    (progress.elapsed_time / (progress.wordcount / progress.total_combinations)) - progress.elapsed_time
                )
                progress.filename = 'wordlist'
                progress.calculate_used_storage(used_storage)
                progress.generate_progress_msg()
                sys.stdout.write('\033[F\033[K' * 20)
                sys.stdout.write(progress.progress_msg)
                sys.stdout.flush()

    if current_batch:
        save_wordlist_to_file(current_batch, 'wordlist', batch_index)
        clear_memory()
        batch_index += 1
        batchcount += 1

    progress.batch_index = batch_index
    progress.wordcount = wordcount
    progress.elapsed_time = time.time() - start_time
    progress.update_remaining_time_chunks(
        (progress.elapsed_time / (progress.wordcount / progress.total_combinations)) - progress.elapsed_time
    )
    progress.filename = filename
    progress.calculate_used_storage(used_storage)
    progress.generate_progress_msg()
    sys.stdout.write('\033[F\033[K' * 25)
    sys.stdout.write(progress.progress_msg)
    sys.stdout.flush()

def save_wordlist_to_file(wordlist, base_filename, batch_index):
    global list_directory
    global used_storage
    os.makedirs(list_directory, exist_ok=True)
    filename = f'{list_directory}/{base_filename}_{batch_index}.txt'
    with open(filename, 'w') as file:
        file.write('\n'.join(wordlist))
    used_storage += os.path.getsize(filename)
    sys.stdout.flush()

def clear_memory():
    gc.collect()
