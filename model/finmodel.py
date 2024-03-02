from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import os

os.environ['OPENAI_API_KEY'] = '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'


def FinModel(pdf_file):
    # Create a directory reader
    reader = SimpleDirectoryReader(input_files=[pdf_file]).load_data()
    # Create a vector store index
    index = VectorStoreIndex.from_documents(reader)
    
    # Return the index
    return index