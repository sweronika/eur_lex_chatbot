from bs4 import BeautifulSoup

from utils import read_file, save_file
from text_processing import get_clean_text


directive_path = './resources/directive.html'
txt_output_path = './resources/directive.txt'


def run():

    website_content = read_file(directive_path)
    soup = BeautifulSoup(website_content, "html.parser")
    text = get_clean_text(soup)

    save_file(text, txt_output_path)
