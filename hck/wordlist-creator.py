import itertools
import time
import os
import psutil  # For memory management

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

    update_interval = 5
    last_update_time = time.time()

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

    # Save any remaining words in the last batch
    if current_batch:
        save_wordlist_to_file(current_batch, 'wordlist', batch_index)
        clear_memory()
        batch_index += 1
        batchcount += 1

    return wordlist

def save_wordlist_to_file(wordlist, base_filename, batch_index):
    global wordcount
    global total_combinations

    os.makedirs('wordlists', exist_ok=True)

    filename = f'wordlists/{base_filename}_{batch_index}.txt'
    with open(filename, 'w') as file:
        file.write('\n'.join(wordlist) + '\n')

    print(f"Batch {batch_index} saved to '{filename}'")
    print(f"Word count: {wordcount} -> {total_combinations}, Batch count: {batchcount}")
    print("---")

def aggregate_wordlists(base_filename, num_batches):
    with open(f'wordlists/{base_filename}_aggregate.txt', 'w') as aggregate_file:
        for batch_index in range(1, num_batches + 1):
            filename = f'wordlists/{base_filename}_{batch_index}.txt'
            with open(filename, 'r') as batch_file:
                lines = batch_file.readlines()
                aggregate_file.writelines(lines)
            print(f"Content of batch {batch_index} appended to aggregate file.")

def clear_memory():
    import gc
    gc.collect()

if __name__ == "__main__":
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=`~"
    min_length = 4
    max_length = 7

    generate_wordlist(characters, min_length, max_length)

    num_batches = batchcount

    # Aggregate all batch files into one
    aggregate_wordlists('wordlist', num_batches)

    print(f"All batches aggregated and saved to 'wordlists/wordlist_aggregate.txt'")
