# This file was used to download and parse the Webster dictionary from The Gutenberg Project

from pathlib import Path
import requests
import bs4

def get_dictionary():
    # Check if we have the dictionary we are working in, and if we don't download it and put it in websters.txt
    if not Path('websters.txt').exists():
        websters_dictionary = requests.get('https://www.gutenberg.org/cache/epub/29765/pg29765.txt').text
        dictionary_file = Path('websters.txt')
        dictionary_file.write_text(websters_dictionary)

if __name__ == '__main__':
    get_dictionary()