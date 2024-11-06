from typing import Optional, Any, List, Dict
import pickle


def read_file(path: str) -> str:
    """
    Reads the contents of a file and returns it as a string.

    Parameters:
    - path (str): The path to the file to be read.

    Returns:
    - str: The contents of the file.
    """
    with open(path, "r", encoding="utf-8") as file:
        output = file.read()
    return output


def save_file(txt: str, path: str) -> None:
    """
    Saves the given text to a file at the specified path.

    Parameters:
    - txt (str): The text content to be saved to the file.
    - path (str): The path where the file should be saved.
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(txt)


def flatten_list(list_to_flatten: List[List]) -> List:
    """
    Flattens a list of lists into a single list.

    Parameters:
    - list_to_flatten (List[List]): A list of lists to be flattened.

    Returns:
    - List: A single flattened list containing all elements from the sublists.
    """
    flattened_list = [item for sublist in list_to_flatten for item in sublist]
    return flattened_list


def save_to_pickle(data: Dict, file_path: str) -> None:
    """Serializes a Python object and saves it to a pickle file.

    Args:
        data (Any): The Python object to serialize and save.
        file_path (str): The path to the file where the pickle data will be saved.
    """

    with open(file_path, "wb") as file:
        pickle.dump(data, file)


def load_from_pickle(file_path: str) -> Optional[Any]:
    """Loads a Python object from a pickle file.

    Args:
        file_path (str): The path to the file containing the pickled data.

    Returns:
        Optional[Any]: The deserialized Python object if successful, None otherwise.
    """

    with open(file_path, "rb") as file:
        data = pickle.load(file)

    return data
