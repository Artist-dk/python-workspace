import os

def merge_txt_files(input_directory, output_directory, output_file_prefix, max_size_gb=5):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    max_size_bytes = max_size_gb * 1024 * 1024 * 1024
    current_size = 0
    batch_count = 1

    output_file = os.path.join(output_directory, f"{output_file_prefix}_{batch_count}.txt")
    outfile = open(output_file, 'w')

    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            file_size = os.path.getsize(file_path)
            if current_size + file_size > max_size_bytes:
                outfile.close()
                print(f"Finished batch {batch_count}, size: {current_size / (1024 * 1024 * 1024):.2f}GB")
                batch_count += 1
                current_size = 0
                output_file = os.path.join(output_directory, f"{output_file_prefix}_{batch_count}.txt")
                outfile = open(output_file, 'w')
                
            with open(file_path, 'r') as infile:
                content = infile.read()
                outfile.write(content)
                
            current_size += file_size
            os.remove(file_path)
            print(f"[+] Added and deleted {filename}\n[_]Current batch size: {current_size / (1024 * 1024 * 1024):.2f}GB\n---")

    outfile.close()
    print(f"Finished merging files. Total batches: {batch_count}")

input_directory = os.path.join(os.getcwd(), 'wordlists')
output_directory = os.path.join(os.getcwd(), 'wordlists5gb')
output_file_prefix = 'wordlist'
merge_txt_files(input_directory, output_directory, output_file_prefix)
