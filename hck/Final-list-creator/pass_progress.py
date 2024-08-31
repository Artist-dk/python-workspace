import time

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

        blue_color = '\033[34m'
        yellow_color = '\033[33m'
        magenta_color = '\033[35m'
        green_color = '\033[32m'
        red_bold_color = '\033[31m'
        cyan_color = '\033[36m'

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
