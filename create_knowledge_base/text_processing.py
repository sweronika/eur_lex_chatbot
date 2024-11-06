import re
from typing import List, Dict

from tqdm import tqdm
from bs4 import BeautifulSoup

from utils import flatten_list


def drop_tags(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Removes specific HTML tags from a BeautifulSoup object.

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML content.

    Returns:
    - BeautifulSoup: The modified BeautifulSoup object with specified tags removed.
    """
    tags_to_drop = ['script', 'style', 'meta', 'link', 'a']
    for tag in tags_to_drop:
        for element in soup.find_all(tag):
            element.decompose()
    return soup


def replace_characters(text: str) -> str:
    """
    Replaces specific characters in a string for normalization.

    Parameters:
    - text (str): The input text to process.

    Returns:
    - str: The modified text with specific characters replaced.
    """
    text = re.sub('\xa0', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    return text


def fix_single_signs(lines: List[str]) -> List[str]:
    """
    Fixes lines with specific punctuation characters by merging them with adjacent lines.

    Parameters:
    - lines (List[str]): A list of strings (lines) to be processed.

    Returns:
    - List[str]: The modified list of lines after fixing single punctuation signs.
    """
    ending_characters = [')', ',', ';', '.', ').']
    starting_characters = ['(']

    for i, line in enumerate(lines):
        if line in ending_characters and i > 0:
            lines[i - 1] = lines[i - 1] + line
        elif line in starting_characters and i < len(lines) - 1:
            lines[i + 1] = line + lines[i + 1]

    pattern = r'^[\W]*$'
    lines = [line for line in lines if not re.match(pattern, line)]

    return lines


def concat_short_lines(lines: List[str], threshold: int = 5) -> List[str]:
    """
    Concatenates short lines (those with length less than or equal to the threshold)
    with the following line, then removes lines shorter than or equal to the threshold.

    Parameters:
    - lines (List[str]): A list of strings (lines) to be processed.
    - threshold (int): The length threshold for considering a line as "short" (default is 5).

    Returns:
    - List[str]: The modified list of lines after concatenating and removing short lines.
    """
    for i, line in enumerate(lines[:-1]):  # Avoid index out of range for the last element
        if len(line) <= threshold:
            lines[i + 1] = line + " " + lines[i + 1]

    lines = [line for line in lines if len(line) > threshold]

    return lines


def seperate_by_chapters(lines: List[str]) -> List[str]:
    """
    Separates lines by chapters based on a pattern matching specific chapter headings,
    adding a tab character as a delimiter and formatting the resulting list of lines.

    Parameters:
    - lines (List[str]): A list of strings (lines) to be processed.

    Returns:
    - List[str]: The processed list of lines, with chapters separated and formatted.
    """
    pattern = (
        r'^(Article\s+\d+|'
        r'CHAPTER\s+[IVXLCDM]+|ANNEX\s+[IVXLCDM]+|TITLE\s+[IVXLCDM]+|'
        r'PART\s+[IVXLCDM]+|Section\s+\d+)$'
    )

    newlines = []
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            newlines.append("\t")
        newlines.append(line)

    text = "\n".join(newlines)
    newlines = text.split("\t")
    newlines = [line.replace("\n", " ").strip() for line in newlines]

    return newlines


def create_overlapping_chunks(words: List[str], chunk_size: int = 200, overlap: int = 50) -> List[List[str]]:
    """
    Splits a list of words into overlapping chunks.

    Parameters:
    - words (List[str]): The list of words to be split into chunks.
    - chunk_size (int): The desired size of each chunk (default is 200).
    - overlap (int): The number of overlapping words between consecutive chunks (default is 50).

    Returns:
    - List[List[str]]: A list of overlapping chunks, where each chunk is a list of words.
    """
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(chunk)
        if len(chunk) < chunk_size:
            break
    return chunks


def get_clean_text(soup: BeautifulSoup) -> str:
    """
    Cleans and processes the HTML content in the BeautifulSoup object by removing tags,
    replacing characters, fixing line formatting, and applying other custom transformations.

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML content.

    Returns:
    - str: The cleaned and formatted text extracted from the HTML content.
    """
    soup = drop_tags(soup)

    text = soup.get_text(separator='\n', strip=True)
    text = replace_characters(text)

    lines = text.split("\n")
    lines = fix_single_signs(lines)
    lines = concat_short_lines(lines)
    lines = seperate_by_chapters(lines)
    lines = lines[0:180]
    text = "\n".join(lines)

    return text


def prepare_chunks(text: str) -> List[str]:
    """
    Prepares overlapping chunks of text by splitting the input into lines, then further into
    overlapping word chunks. Each chunk is limited by a specified chunk size and overlap.

    Parameters:
    - text (str): The input text to be split into chunks.

    Returns:
    - List[str]: A list of chunks where each chunk is a string of words.
    """
    newlines = text.split("\n")
    chunks_per_parts = [create_overlapping_chunks(line.split(" "), chunk_size=200, overlap=50) for line in newlines]
    chunks = flatten_list(chunks_per_parts)
    chunks = [" ".join(chunk_list) for chunk_list in chunks]

    return chunks


def encode_chunks(model, chunks: List[str]) -> Dict[str, List[float]]:
    """
    Encodes a list of text chunks using a model and returns a list of tuples containing
    the embeddings and the corresponding chunk.

    Parameters:
    - model: The model used to encode the chunks.
    - chunks (List[str]): A list of text chunks to be encoded.

    Returns:
    - List[Tuple[List[float], str]]: A list of tuples where each tuple contains the
      embedding (a list of floats) and the corresponding text chunk.
    """
    encoded_chunks = []
    for chunk in tqdm(chunks, desc='Create embeddings'):
        embeddings = model.encode(chunk)
        encoded_chunks.append(embeddings)

    encodings_text = dict(zip(chunks, encoded_chunks))

    return encodings_text
