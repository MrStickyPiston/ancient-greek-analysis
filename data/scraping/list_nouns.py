import re

import requests
import urllib.parse
from bs4 import BeautifulSoup

def crawl_page(url, visited):
    # Send a GET request to the URL
    response = requests.get('https://en.wiktionary.org' + url)
    print(f"Crawling {url}")
    visited.append(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the elements with the class 'mw-category-group'
    category_groups = soup.find_all('div', id='mw-pages')

    # Extract all the links within the 'mw-category-group' elements
    link_urls = set()
    for category_group in category_groups:
        links = category_group.find_all('a')
        for link in links:
            link_url = urllib.parse.unquote(link.get('href'))

            if link_url.startswith('/w/index.php') and link_url not in visited:
                link_urls = link_urls.union(crawl_page(link_url, visited))
                visited.append(link_url)
            elif not link_url.startswith('/w/index.php'):
                link_urls.add(link_url)

    return link_urls

def convert_to_filename(text):
    """
    Converts the given text to a valid file name.
    """
    # Remove special characters
    filename = re.sub(r'[^a-zA-Z0-9_\-. ]', '', text)

    filename = filename.replace(' ', '_')

    return filename.lower() + ".txt"

page_url = input("Enter a page url: ").split("https://en.wiktionary.org")[1]

soup = BeautifulSoup(requests.get('https://en.wiktionary.org' + page_url).content, 'html.parser')

outputfile = convert_to_filename(soup.find('span', class_='mw-page-title-main').text)

links = list(crawl_page(page_url, []))
links.sort()

with open(outputfile, 'w') as file:
    for link in links:
        file.write(link.split("/")[2] + "\n")

print(f"Saved to {outputfile}")

