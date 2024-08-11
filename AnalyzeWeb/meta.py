import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

# Function to analyze the website
def analyze_website(url):
    try:
        # Fetch the website content
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        html_content = response.text
        
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title
        title = soup.title.string if soup.title else 'No title found'
        
        # Extract meta description
        meta_description = ''
        if soup.find('meta', attrs={'name': 'description'}):
            meta_description = soup.find('meta', attrs={'name': 'description'})['content']
        else:
            meta_description = 'No meta description found'
        
        # Extract all links
        links = [a['href'] for a in soup.find_all('a', href=True)]
        
        # Count the number of images
        num_images = len(soup.find_all('img'))
        
        # Count the number of scripts
        num_scripts = len(soup.find_all('script'))
        
        # Count the number of stylesheets
        num_stylesheets = len(soup.find_all('link', rel='stylesheet'))
        
        # Extract and analyze text content
        text_content = soup.get_text()
        words = re.findall(r'\b\w+\b', text_content.lower())
        word_count = Counter(words)
        
        # Output the analysis
        print(f"Website Title: {title}")
        print(f"Meta Description: {meta_description}")
        print(f"Number of Images: {num_images}")
        print(f"Number of Scripts: {num_scripts}")
        print(f"Number of Stylesheets: {num_stylesheets}")
        print(f"Total Number of Links: {len(links)}")
        print("Top 10 Most Common Words:")
        for word, count in word_count.most_common(10):
            print(f"{word}: {count}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")

# Example usage:
url = input("Enter url:")
analyze_website(url)
