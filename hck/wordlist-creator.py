import itertools
import os
import time
import gc
import sys

wordcount = 0
batchcount = 0
total_combinations = 0

def generate_wordlist(characters, min_length, max_length):
    global wordcount
    global batchcount
    global total_combinations

    wordlist = []

    total_combinations = 0
    for length in range(min_length, max_length + 1):
        num_combinations = len(characters) ** length
        total_combinations += num_combinations

    batch_size = 10000000
    current_batch = []
    batch_index = 1

    for length in range(min_length, max_length + 1):
        for combination in itertools.product(characters, repeat=length):
            word = ''.join(combination)
            wordcount += 1
            current_batch.append(word)

            if len(current_batch) == batch_size:
                save_wordlist_to_file(current_batch, 'wordlist', batch_index)
                clear_memory()
                current_batch = []
                batch_index += 1
                batchcount += 1

            # Update terminal output
            if wordcount % 100000 == 0:
                print_progress(batch_index, wordcount, total_combinations)

    # Save any remaining words in the last batch
    if current_batch:
        save_wordlist_to_file(current_batch, 'wordlist', batch_index)
        clear_memory()
        batch_index += 1
        batchcount += 1

    print_progress(batch_index, wordcount, total_combinations, final=True)
    return wordlist

def save_wordlist_to_file(wordlist, base_filename, batch_index):
    global wordcount
    global total_combinations

    os.makedirs('wordlists', exist_ok=True)

    filename = f'wordlists/{base_filename}_{batch_index}.txt'
    with open(filename, 'w') as file:
        file.write('\n'.join(wordlist))

    sys.stdout.write(f"\n[+] Batch {batch_index} saved to '{filename}'\n")
    sys.stdout.flush()

def clear_memory():
    gc.collect()

def print_progress(batch_index, wordcount, total_combinations, final=False):
    progress_msg = f"Batch {batch_index}, Word count: {wordcount}/{total_combinations} ({wordcount / total_combinations * 100:.2f}%)"
    sys.stdout.write('\r' + progress_msg + ' ' * (80 - len(progress_msg)))
    sys.stdout.flush()
    if final:
        # Print the final message on a new line
        sys.stdout.write('\n')
        sys.stdout.flush()

if __name__ == "__main__":
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=`~\" "
    min_length = 4
    max_length = 5

    generate_wordlist(characters, min_length, max_length)
