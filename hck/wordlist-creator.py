import itertools
import os
import gc
import sys
import time

min_length = 6
max_length = 7
characters = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
# characters = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=`~\""
filename = ''
wordlist_directory = '/home/kernel/Desktop/Wordlist/temp'

wordcount = 0
batchcount = 0
batch_index = 0
total_combinations = 0
used_storage = 0

class ProgressMsg:
    def __init__(self):
        self.batch_index = 0
        self.wordcount = 0
        self.total_combinations = 0
        self.elapsed_time = 0
        self.remaining_time_seconds = 0
        self.remaining_time_minutes = 0
        self.remaining_time_hours = 0
        self.remaining_time_days = 0
        self.remaining_time_months = 0
        self.remaining_time_years = 0
        self.size_mb = 0
        self.size_gb = 0
        self.size_tb = 0
        self.used_storage_mb = 0
        self.used_storage_gb = 0
        self.used_storage_tb = 0
        self.filename = ''
        self.progress_msg = ''

    def calculate_required_storage_size(self, min_length, max_length, total_combinations):
        avg_word_length = (min_length + max_length) / 2
        avg_word_size = avg_word_length + 1
        total_size = total_combinations * avg_word_size
        self.size_mb = total_size / (1024 ** 2)
        self.size_gb = total_size / (1024 ** 3)
        self.size_tb = total_size / (1024 ** 4)

    def calculate_used_storage(self, used_storage):
        self.used_storage_mb = used_storage / (1024 ** 2)
        self.used_storage_gb = used_storage / (1024 ** 3)
        self.used_storage_tb = used_storage / (1024 ** 4)

    def format_time(self, seconds):
        units = [
            ("second", 60), 
            ("minute", 60), 
            ("hour", 24), 
            ("day", 30.44), 
            ("month", 12), 
            ("year", float('inf'))
        ]
        time_str = []
        remaining_time = seconds
        for unit_name, unit_size in units:
            if remaining_time < 1:
                break
            unit_value = remaining_time % unit_size
            remaining_time = remaining_time // unit_size
            if unit_value:
                time_str.append(f"{unit_value:.2f} {unit_name}{'s' if unit_value != 1 else ''}")
        return ', '.join(reversed(time_str))

    def update_remaining_time_chunks(self, remaining_seconds):
        self.remaining_time_seconds = remaining_seconds % 60
        remaining_minutes = remaining_seconds // 60

        self.remaining_time_minutes = remaining_minutes % 60
        remaining_hours = remaining_minutes // 60

        self.remaining_time_hours = remaining_hours % 24
        remaining_days = remaining_hours // 24

        self.remaining_time_days = remaining_days % 30.44
        remaining_months = remaining_days // 30.44

        self.remaining_time_months = remaining_months % 12
        self.remaining_time_years = remaining_months // 12

    def generate_progress_msg(self):
        progress_percent = (self.wordcount / self.total_combinations) * 100
        bar_length = 40
        filled_length = int(bar_length * self.wordcount / self.total_combinations)
        empty_length = bar_length - filled_length

        filled_color = '\033[91m'
        empty_color = '\033[90m'
        reset_color = '\033[0m'
        red_color = '\033[91m'

        black_color = '\033[30m'
        red_bold_color = '\033[31m'
        green_color = '\033[32m'
        yellow_color = '\033[33m'
        blue_color = '\033[34m'
        magenta_color = '\033[35m'
        cyan_color = '\033[36m'
        white_color = '\033[37m'

        bright_black_color = '\033[90m'
        bright_red_color = '\033[91m'
        bright_green_color = '\033[92m'
        bright_yellow_color = '\033[93m'
        bright_blue_color = '\033[94m'
        bright_magenta_color = '\033[95m'
        bright_cyan_color = '\033[96m'
        bright_white_color = '\033[97m'

        underline_red_color = '\033[4;31m'
        underline_green_color = '\033[4;32m'
        underline_yellow_color = '\033[4;33m'
        underline_blue_color = '\033[4;34m'
        underline_magenta_color = '\033[4;35m'
        underline_cyan_color = '\033[4;36m'
        underline_white_color = '\033[4;37m'

        bar = filled_color + '█' * filled_length + empty_color + '█' * empty_length + reset_color

        self.progress_msg = f"""\

{blue_color}Batch No.:           {reset_color}{yellow_color}{self.batch_index}{reset_color}
{blue_color}Saved words:         {reset_color}{magenta_color}{self.wordcount}{reset_color}
{blue_color}Total words:         {red_bold_color}{red_color}{self.total_combinations}{reset_color}
{blue_color}Elapsed time:        {reset_color}{yellow_color}{self.format_time(self.elapsed_time)}{reset_color}
{blue_color}Remaining time:      {reset_color}
    {blue_color}S:{reset_color}{green_color} {self.remaining_time_seconds:.2f}{reset_color}
    {blue_color}M:{reset_color}{yellow_color} {self.remaining_time_minutes:.2f}{reset_color}
    {blue_color}H:{reset_color}{cyan_color} {self.remaining_time_hours:.2f}{reset_color}
    {blue_color}D:{reset_color}{magenta_color} {self.remaining_time_days:.2f}{reset_color}
    {blue_color}M:{reset_color}{red_bold_color} {self.remaining_time_months:.2f}{reset_color}
    {blue_color}Y:{reset_color}{red_color} {self.remaining_time_years:.2f}{reset_color}
{blue_color}Required storage:    {reset_color}{red_bold_color} {self.size_mb:.2f} MB / {self.size_gb:.2f} GB / {self.size_tb:.2f} TB{reset_color}
{blue_color}Used storage:        {reset_color}{magenta_color} {self.used_storage_mb:.2f} MB / {self.used_storage_gb:.2f} GB / {self.used_storage_tb:.2f} TB{reset_color}
{blue_color}[+] New batch        {reset_color}{green_color} {self.filename}{reset_color}

{bar} {progress_percent:08.5f}%


"""

def generate_wordlist(characters, min_length, max_length):
    global wordcount
    global batchcount
    global total_combinations
    global filename
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
                progress.filename = filename
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
    global wordlist_directory
    global filename
    global used_storage
    os.makedirs(wordlist_directory, exist_ok=True)
    filename = f'{wordlist_directory}/{base_filename}_{batch_index}.txt'
    with open(filename, 'w') as file:
        file.write('\n'.join(wordlist))
    used_storage += os.path.getsize(filename)
    sys.stdout.flush()

def clear_memory():
    gc.collect()

if __name__ == "__main__":
    generate_wordlist(characters, min_length, max_length)
