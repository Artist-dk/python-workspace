import itertools
import os
import time

# Configuration settings
BATCH_SIZE = 1000  # Number of email IDs per batch file
OUTPUT_DIRECTORY = '/home/kernel/Desktop/Wordlist/email'
DOMAINS = ['example.com', 'sample.org']  # List of domains to use for email generation
SEPARATORS = ['', '.', '_']  # List of separators to use between first and last names

class EmailProgressMsg:
    def __init__(self):
        self.batch_index = 0
        self.email_count = 0
        self.total_combinations = 0
        self.elapsed_time = 0
        self.remaining_time_seconds = 0
        self.remaining_time_minutes = 0
        self.remaining_time_hours = 0
        self.remaining_time_days = 0
        self.remaining_time_months = 0
        self.remaining_time_years = 0
        self.used_storage_mb = 0
        self.used_storage_gb = 0
        self.used_storage_tb = 0
        self.filename = ''
        self.progress_msg = ''

    def calculate_total_combinations(self, num_names, domains, separators):
        self.total_combinations = (num_names * (num_names - 1)) * len(domains) * len(separators)

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
        units = [60, 60, 24, 30.44, 12]
        time_values = []
        remaining_time = remaining_seconds
        for unit_size in units:
            time_values.append(remaining_time % unit_size)
            remaining_time //= unit_size
        time_values.append(remaining_time)

        self.remaining_time_seconds, self.remaining_time_minutes, self.remaining_time_hours, \
        self.remaining_time_days, self.remaining_time_months, self.remaining_time_years = time_values

    def generate_progress_msg(self):
        progress_percent = (self.email_count / self.total_combinations) * 100 if self.total_combinations else 0
        bar_length = 40
        filled_length = int(bar_length * self.email_count / self.total_combinations) if self.total_combinations else 0
        empty_length = bar_length - filled_length

        filled_color = '\033[91m'
        empty_color = '\033[90m'
        reset_color = '\033[0m'

        bar = filled_color + '█' * filled_length + empty_color + '█' * empty_length + reset_color

        self.progress_msg = f"""\

Batch No.:           {self.batch_index}
Generated emails:    {self.email_count}
Total combinations:  {self.total_combinations}
Elapsed time:        {self.format_time(self.elapsed_time)}
Remaining time:
    S: {self.remaining_time_seconds:.2f}
    M: {self.remaining_time_minutes:.2f}
    H: {self.remaining_time_hours:.2f}
    D: {self.remaining_time_days:.2f}
    M: {self.remaining_time_months:.2f}
    Y: {self.remaining_time_years:.2f}
Used storage:        {self.used_storage_mb:.2f} MB / {self.used_storage_gb:.2f} GB / {self.used_storage_tb:.2f} TB
[+] Last batch saved: {self.filename}

{bar} {progress_percent:08.5f}%

"""

    def update_progress(self, batch_index, email_count, elapsed_time, remaining_seconds, used_storage, filename):
        self.batch_index = batch_index
        self.email_count = email_count
        self.elapsed_time = elapsed_time
        self.calculate_used_storage(used_storage)
        self.filename = filename
        self.update_remaining_time_chunks(remaining_seconds)
        self.generate_progress_msg()

def generate_email_ids(first_name, last_name, domains, separators):
    for domain in domains:
        for separator in separators:
            yield f"{first_name}{separator}{last_name}@{domain}"

def save_emails_to_file(email_batch, output_directory, batch_index):
    os.makedirs(output_directory, exist_ok=True)
    filename = os.path.join(output_directory, f'emails_{batch_index}.txt')
    with open(filename, 'w') as file:
        file.write('\n'.join(email_batch))
    return filename

def generate_and_save_emails(names_file, batch_size, output_directory, domains, separators):
    """
    Main function to generate and save email IDs.
    """
    progress = EmailProgressMsg()
    
    with open(names_file, 'r') as file:
        names = [line.strip() for line in file if line.strip()]
    
    progress.calculate_total_combinations(len(names), domains, separators)
    
    email_batch = []
    batch_index = 1
    email_count = 0
    start_time = time.time()
    used_storage = 0

    # Using two nested loops to generate combinations without loading all names into memory
    for first_name in names:
        for last_name in names:
            if first_name != last_name:  # Skip same name combinations
                for email in generate_email_ids(first_name, last_name, domains, separators):
                    email_batch.append(email)
                    email_count += 1

                    if len(email_batch) >= batch_size:
                        filename = save_emails_to_file(email_batch, output_directory, batch_index)
                        email_batch = []
                        batch_index += 1
                        used_storage += os.path.getsize(filename)
                        progress.update_progress(batch_index, email_count, time.time() - start_time, 
                                                 (time.time() - start_time) / email_count * (progress.total_combinations - email_count), 
                                                 used_storage, filename)
                        print(progress.progress_msg)
    
    # Save any remaining emails
    if email_batch:
        filename = save_emails_to_file(email_batch, output_directory, batch_index)
        used_storage += os.path.getsize(filename)
        progress.update_progress(batch_index, email_count, time.time() - start_time, 
                                 (time.time() - start_time) / email_count * (progress.total_combinations - email_count), 
                                 used_storage, filename)
        print(progress.progress_msg)

if __name__ == "__main__":
    generate_and_save_emails('./common/names.txt', BATCH_SIZE, OUTPUT_DIRECTORY, DOMAINS, SEPARATORS)
