import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

load_dotenv()


class QuoteScraper:
    def __init__(self, input_url, output_file_jsonl, output_file_txt):
        self.url = input_url
        self.page_num = 1
        self.output_file_jsonl = output_file_jsonl
        self.output_file_txt = output_file_txt

    def parse_page(self):
        while True:
            url = f"{self.url}{self.page_num}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes_divs = soup.find_all('div', class_='quote')

            for quote_div in quotes_divs:
                text = quote_div.find('span', class_='text').get_text(strip=True)
                text = text.replace('\u201c', '').replace('\u201d', '')

                author = quote_div.find('small', class_='author').get_text(strip=True)

                tags = [tag.get_text(strip=True) for tag in quote_div.find('div', class_='tags').find_all('a')]

                quote_dict = {"text": text, "author": author, "tags": tags}
                quote_json = json.dumps(quote_dict, indent=4) + ",\n"

                with open(self.output_file_jsonl, 'a') as jsonl_file:
                    jsonl_file.write(quote_json + '\n')

                with open(self.output_file_txt, 'a') as txt_file:
                    txt_file.write(f"Text: {text}\nAuthor: {author}\nTags: {', '.join(tags)}\n\n")

            if soup.find(class_='next') is None:
                break
            else:
                self.page_num += 1


input_url = os.getenv('INPUT_URL')
output_file_jsonl = os.getenv('OUTPUT_FILE_JSONL')
output_file_txt = os.getenv('OUTPUT_FILE_TXT')


scraper = QuoteScraper(input_url, output_file_jsonl, output_file_txt)
scraper.parse_page()

with open(output_file_jsonl, 'r') as jsonl_file, open(output_file_txt, 'w') as txt_file:
    quotes = jsonl_file.readlines()
    txt_file.writelines(quotes)
