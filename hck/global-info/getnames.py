import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://example.com/names'  # Replace with the actual URL

# Send an HTTP GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find all elements that contain names
# This will depend on the specific HTML structure of the page
# For example, if names are in <li> tags with a class 'name-item':
names_elements = soup.find_all('li', class_='name-item')

# Extract the text from each element
names = [name.get_text(strip=True) for name in names_elements]

# Specify the filename
filename = 'scraped_names.txt'

# Write names to the file
with open(filename, 'w') as file:
    for name in names:
        file.write(name + '\n')

print(f"File '{filename}' created successfully with names.")
