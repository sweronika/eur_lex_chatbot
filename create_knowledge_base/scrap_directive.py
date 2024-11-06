import requests
import logging
from typing import Optional

website_url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32018L1972"
directive_path = './resources/directive.html'

logging.basicConfig(level=logging.INFO)


class Website:

    def __init__(self, url):
        self.url = url
        self.website_content = self.get_web_html_content()

    def get_web_html_content(self) -> Optional[str]:
        """Fetches the HTML content of a given URL.

        Args:
            self: The object instance that contains the URL to retrieve.

        Returns:
            Optional[str]: The HTML content of the page if successful, None otherwise.
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return response.text

        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving page {self.url}: {str(e)}")
            return None

    def save_to_file(self, dest_path: str) -> None:
        """Saves the website content to a file.

        Args:
            dest_path (str): The destination path where the content will be saved.
        """
        if not self.website_content:
            logging.warning("No content to save. Website content is empty or None.")
            return

        try:
            with open(dest_path, "w", encoding="utf-8") as file:
                file.write(self.website_content)
            logging.info(f"Content successfully saved to {dest_path}")

        except (IOError, OSError) as e:
            logging.error(f"Failed to write to {dest_path}. Error: {str(e)}")


def run():
    web = Website(website_url)
    web.get_web_html_content()
    web.save_to_file(directive_path)
