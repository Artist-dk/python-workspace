import itertools
import os
import gc
import sys

wordcount = 0
batchcount = 0
batch_index = 0
total_combinations = 0
filename = ''
wordlist_directory = '/media/kernel/KERNEL-ntfs/wordlist/temp'

def generate_wordlist(characters, min_length, max_length):
    global wordcount
    global batchcount
    global total_combinations

    total_combinations = sum(len(characters) ** length for length in range(min_length, max_length + 1))

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

            if wordcount % 100000 == 0:
                print_progress(batch_index, wordcount, total_combinations)

    if current_batch:
        save_wordlist_to_file(current_batch, 'wordlist', batch_index)
        clear_memory()
        batch_index += 1
        batchcount += 1

    print_progress(batch_index, wordcount, total_combinations, final=True)
    return current_batch

def save_wordlist_to_file(wordlist, base_filename, batch_index):
    global wordlist_directory
    global filename
    os.makedirs(wordlist_directory, exist_ok=True)
    filename = f'{wordlist_directory}/{base_filename}_{batch_index}.txt'
    with open(filename, 'w') as file:
        file.write('\n'.join(wordlist))
    sys.stdout.flush()

def clear_memory():
    gc.collect()

def print_progress(batch_index, wordcount, total_combinations, final=False):
    global filename
    
    progress_percent = (wordcount / total_combinations) * 100
    bar_length = 40
    
    
    filled_length = int(bar_length * wordcount / total_combinations)
    empty_length = bar_length - filled_length

    filled_color = '\033[91m'
    empty_color = '\033[90m'
    reset_color = '\033[0m'

    red_color = '\033[91m'

    bar = filled_color + '█' * filled_length + empty_color + '█' * empty_length + reset_color
    
    
    progress_msg = f"""\

Batch No.:           {batch_index}{red_color}
Saved words:         {wordcount}{reset_color}
Total combinations:  {total_combinations}
[+] New batch        {filename}

{bar} {progress_percent:.2f}%


"""
    
    # Clear previous message (15 lines)
    sys.stdout.write('\033[F\033[K' * 15)
    sys.stdout.write(progress_msg)
    sys.stdout.flush()
    
    if final:
        sys.stdout.write('\n')
        sys.stdout.flush()

if __name__ == "__main__":
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=`~\" "
    min_length = 1
    max_length = 4

    generate_wordlist(characters, min_length, max_length)
