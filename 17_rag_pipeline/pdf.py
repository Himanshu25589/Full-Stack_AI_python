from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

loader = PyPDFLoader("document loaders/GRU.pdf")
docs = loader.load()

splitter = TokenTextSplitter(
    chunk_size=100,
    chunk_overlap=10
)

chunks = splitter.split_documents(docs)

print("Pages:", len(docs))
print("Chunks:", len(chunks))
print(chunks[0].page_content)