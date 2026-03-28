import os
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from urllib.parse import urljoin, urlparse
import pypdf
from pathlib import Path

# Config
DATA_DIR = Path('data')
DB_DIR = Path('chroma_db')
DB_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

SOURCES = [
    # MIT EECS Courses (example URLs - replace with actual public catalogs)
    {'type': 'pdf', 'url': 'https://catalog.mit.edu/subjects/6/'},  # Placeholder; use actual PDF links
    {'type': 'pdf', 'url': 'https://catalog.mit.edu/degree-charts/electrical-engineering-computer-science-tracks/'},
    {'type': 'pdf', 'url': 'https://registrar.mit.edu/registration-academics/academic-standards/grading'},
    # Add 20+ course PDFs, program reqs. Manual download initially.
    # Example: {'type': 'html', 'url': 'https://catalog.mit.edu/subjects/6/6-01/'},
]

def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        path = DATA_DIR / filename
        path.write_bytes(response.content)
        return str(path)
    return None

def load_documents():
    docs = []
    for i, source in enumerate(SOURCES):
        if source['type'] == 'pdf':
            filename = f"mit_catalog_{i}.pdf"
            pdf_path = download_pdf(source['url'], filename)
            if pdf_path:
                loader = PyPDFLoader(pdf_path)
                docs.extend(loader.load())
        elif source['type'] == 'html':
            loader = WebBaseLoader(source['url'])
            docs.extend(loader.load())
    return docs

if __name__ == "__main__":
    docs = load_documents()
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=model,
        persist_directory=str(DB_DIR)
    )
    print(f"Ingested {len(splits)} chunks. DB at {DB_DIR}")

