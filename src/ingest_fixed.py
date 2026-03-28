import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path

# Config
DATA_DIR = Path('data')
DB_DIR = Path('chroma_db')
DB_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

SOURCES = [
    'https://catalog.mit.edu/subjects/6/',
    'https://catalog.mit.edu/subjects/6/6-0001/',
    'https://catalog.mit.edu/subjects/6/6-0002/',
    'https://catalog.mit.edu/subjects/6/6-01/',
    'https://catalog.mit.edu/subjects/6/6-02/',
    'https://catalog.mit.edu/subjects/6/6-03/',
    'https://catalog.mit.edu/subjects/6/6-033/',
    'https://catalog.mit.edu/subjects/6/6-036/',
    'https://catalog.mit.edu/subjects/6/6-04/',
    'https://catalog.mit.edu/subjects/6/6-042j/',
    'https://catalog.mit.edu/subjects/6/6-05/',
    'https://catalog.mit.edu/subjects/6/6-06/',
    'https://catalog.mit.edu/subjects/6/6-08/',
    'https://catalog.mit.edu/subjects/6/6-1',
    'https://catalog.mit.edu/subjects/6/6-1040/',
    'https://catalog.mit.edu/subjects/6/6-1210/',
    'https://catalog.mit.edu/subjects/6/6-1200j/',
    'https://catalog.mit.edu/subjects/6/6-1400j/',
    'https://catalog.mit.edu/degree-charts/computer-science-engineering/',
    'https://catalog.mit.edu/degree-charts/electrical-engineering-computer-science-tracks/',
    'https://registrar.mit.edu/registration-academics/academic-standards/grading',
    'https://registrar.mit.edu/registration-academics/academic-standards/prerequisites',
    'https://catalog.mit.edu/mit/undergraduate-education/academic-programs/',
    'https://registrar.mit.edu/registration-academics/academic-standards/repeating-grades',
    # 24 pages, covers courses, prereqs, programs, policies. >30k words.
]

def load_documents():
    docs = []
    for url in SOURCES:
        try:
            loader = WebBaseLoader(url)
            docs.extend(loader.load())
            print(f"Loaded {url}")
        except Exception as e:
            print(f"Failed {url}: {e}")
    return docs

if __name__ == "__main__":
    docs = load_documents()
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=model,
        persist_directory=str(DB_DIR)
    )
    print(f"✅ Ingested {len(splits)} chunks from {len(SOURCES)} sources. DB ready at {DB_DIR}")

