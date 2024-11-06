from sentence_transformers import SentenceTransformer
from utils import read_file, save_to_pickle
from text_processing import prepare_chunks, encode_chunks

directive_path = './resources/directive.txt'
embeddings_path = '../knowledge_base/embeddings.pickle'


def run():

    text = read_file(directive_path)
    chunks = prepare_chunks(text)

    model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)
    encoded_chunks = encode_chunks(model, chunks)

    save_to_pickle(encoded_chunks, embeddings_path)
