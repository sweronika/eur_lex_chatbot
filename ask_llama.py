from processing import LlamaQAModel, get_related_knowledge
from utils import read_file, load_from_pickle


question_path = 'question'
embeddings_path = './knowledge_base/embeddings.pickle'


knowledge_base = load_from_pickle(embeddings_path)
question = read_file(question_path)
related_knowledge = get_related_knowledge(question, knowledge_base)

llama_qa_model = LlamaQAModel(model_name="meta-llama/Llama-3.2-1B")
answear = llama_qa_model.ask_question(knowledge_base=related_knowledge, question=question)
print(answear)