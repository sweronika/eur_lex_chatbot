import scrap_directive
import process_directive
import encode_directive
import logging

logging.basicConfig(level=logging.INFO)


def get_knowledge_base():
    logging.info('Scraping directive...')
    scrap_directive.run()

    logging.info('Processing directive...')
    process_directive.run()

    logging.info('Encoding directive...')
    encode_directive.run()

    logging.info('Getting knowledge base finished with success.')


if __name__ == "__main__":
    get_knowledge_base()
