from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import os

os.environ['GEMINI_API_KEY'] = ''

def GeminiModel(pdf_file):
    # Create a directory reader
    reader = SimpleDirectoryReader(input_files=[pdf_file]).load_data()
    # Create a vector store index
    index = VectorStoreIndex.from_documents(reader)
    
    # Return the index
    return index