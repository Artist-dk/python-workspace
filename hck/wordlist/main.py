# main.py
from progress_msg import ProgressMsg
from wordlist_generator import generate_wordlist
from email_generator import generate_emails
import config  # Import the configuration variables from config.py

def main():
    progress = ProgressMsg()

    print("Select the type of list you want to generate:")
    print("1. Passwords")
    print("2. Email IDs")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        print("Generating Passwords...")
        generate_wordlist(config.characters, config.min_length, config.max_length, config.wordlist_directory, progress)
    elif choice == "2":
        print("Generating Email IDs...")
        generate_emails(config.characters, config.min_length, config.max_length, config.wordlist_directory, progress)
    else:
        print("Invalid choice. Please run the program again and select a valid option.")

if __name__ == "__main__":
    main()
