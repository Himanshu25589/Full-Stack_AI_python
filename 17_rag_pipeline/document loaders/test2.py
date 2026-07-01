from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=1)

data = TextLoader("document loaders/notes.txt")
docs = data.load()
chunks = splitter.split_documents(docs)

print(len(chunks))
print(chunks[0].page_content)

for i in chunks:
    print(i.page_content)
    print()
    print()
    print()
    print()
    
