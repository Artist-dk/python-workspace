import sys
import time
from wordlist_generator import generate_wordlist
from email_generator import generate_email_list, domains
from progress_msg import ProgressMsg

min_length = 6
max_length = 7
characters = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
wordlist_directory = 'K:/wordlist/temp'

def main():
    generate_emails = False
    if len(sys.argv) > 1 and sys.argv[1] == "--emails":
        generate_emails = True

    progress = ProgressMsg()
    if generate_emails:
        total_combinations = sum(len(characters) ** length for length in range(min_length, max_length + 1))
        progress.total_combinations = total_combinations
        progress.calculate_required_storage_size(min_length, max_length, total_combinations)

        start_time = time.time()
        generate_email_list(characters, min_length, max_length, wordlist_directory, domains, progress)
    else:
        total_combinations = sum(len(characters) ** length for length in range(min_length, max_length + 1))
        progress.total_combinations = total_combinations
        progress.calculate_required_storage_size(min_length, max_length, total_combinations)

        start_time = time.time()
        generate_wordlist(characters, min_length, max_length, wordlist_directory, progress)

    progress.elapsed_time = time.time() - start_time
    progress.update_remaining_time_chunks(
        (progress.elapsed_time / (progress.wordcount / progress.total_combinations)) - progress.elapsed_time
    )
    progress.generate_progress_msg()
    sys.stdout.write('\033[F\033[K' * 25)
    sys.stdout.write(progress.progress_msg)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
