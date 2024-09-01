# email_progress.py

import os
import time

class EmailProgressMsg:
    def __init__(self):
        self.total_combinations = 0
        self.wordcount = 0
        self.batch_index = 0
        self.elapsed_time = 0
        self.remaining_time_chunks = 0
        self.filename = ""
        self.used_storage = 0
        self.progress_msg = ""

    def update_remaining_time_chunks(self, remaining_time):
        self.remaining_time_chunks = remaining_time

    def calculate_used_storage(self, file_size):
        self.used_storage += file_size / (1024 * 1024)  # Convert to MB

    def generate_progress_msg(self):
        completed_percentage = (self.wordcount / self.total_combinations) * 100 if self.total_combinations > 0 else 0
        self.progress_msg = (
            f"Batch: {self.batch_index}\n"
            f"Generated Email IDs: {self.wordcount}\n"
            f"Progress: {completed_percentage:.2f}%\n"
            f"Elapsed Time: {self.elapsed_time:.2f} seconds\n"
            f"Estimated Remaining Time: {self.remaining_time_chunks:.2f} seconds\n"
            f"Current Batch File: {self.filename}\n"
            f"Total Used Storage: {self.used_storage:.2f} MB\n"
            "----------------------\n"
        )

    def print_progress(self):
        print(self.progress_msg, end='\r')


if __name__ == "__main__":
    # Example usage:
    progress = EmailProgressMsg()
    progress.total_combinations = 1000000  # Example total combinations
    progress.wordcount = 500000  # Example wordcount
    progress.batch_index = 1
    progress.elapsed_time = 100.5
    progress.remaining_time_chunks = 200.0
    progress.filename = "emails_1.txt"
    progress.calculate_used_storage(1024 * 1024)  # Example file size in bytes

    progress.generate_progress_msg()
    progress.print_progress()
