import itertools
import os
import sys
import gc

def generate_wordlist(characters, min_length, max_length, wordlist_directory, progress):
    wordcount = 0
    batch_size = 10000000
    current_batch = []
    batch_index = 1
    used_storage = 0
    filename = ''

    for length in range(min_length, max_length + 1):
        for combination in itertools.product(characters, repeat=length):
            word = ''.join(combination).strip()
            wordcount += 1
            current_batch.append(word)

            if len(current_batch) == batch_size:
                filename = save_wordlist_to_file(current_batch, wordlist_directory, 'wordlist', batch_index)
                used_storage += os.path.getsize(filename)
                clear_memory()
                current_batch = []
                batch_index += 1

            if wordcount % 100000 == 0:
                update_progress(progress, wordcount, used_storage, batch_index, filename)

    if current_batch:
        filename = save_wordlist_to_file(current_batch, wordlist_directory, 'wordlist', batch_index)
        used_storage += os.path.getsize(filename)
        clear_memory()
        batch_index += 1

def save_wordlist_to_file(wordlist, wordlist_directory, base_filename, batch_index):
    os.makedirs(wordlist_directory, exist_ok=True)
    filename = f'{wordlist_directory}/{base_filename}_{batch_index}.txt'
    with open(filename, 'w') as file:
        file.write('\n'.join(wordlist))
    return filename

def update_progress(progress, wordcount, used_storage, batch_index, filename):
    progress.batch_index = batch_index
    progress.wordcount = wordcount
    progress.calculate_used_storage(used_storage)
    progress.filename = filename
    progress.generate_progress_msg()
    sys.stdout.write('\033[F\033[K' * 19)
    sys.stdout.write(progress.progress_msg)
    sys.stdout.flush()

def clear_memory():
    gc.collect()
