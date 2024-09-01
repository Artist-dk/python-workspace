import csv

# File paths
input_csv = 'data.csv'
output_names = 'names.txt'
output_genders = 'genders.txt'
output_races = 'races.txt'

# Open the CSV file and read its contents
with open(input_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Skip the header row
    next(csvreader)

    # Open the output files
    with open(output_names, 'w') as namesfile, \
         open(output_genders, 'w') as gendersfile, \
         open(output_races, 'w') as racesfile:

        # Write data to respective files
        for row in csvreader:
            name, gender, race = row
            namesfile.write(name + '\n')
            gendersfile.write(gender + '\n')
            racesfile.write(race + '\n')

print("Data has been separated into three files.")
