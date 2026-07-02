from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

docs = [
    Document(
        page_content="A vector database stores embeddings and enables semantic search over large collections of documents."
    ),
    Document(
        page_content="ChromaDB is an open-source vector database commonly used in Retrieval-Augmented Generation applications."
    ),
    Document(
        page_content="Embeddings convert text into numerical vectors that capture semantic meaning."
    )
]

embedding_model = MistralAIEmbeddings(
    model="mistral-embed"
)

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)

print("Vector DB Created Successfully!")

result = vectorstore.similarity_search("What is a use for data analysis?", k=2)
for r in result:
    print(r.page_content)
    print(r.metadata)

retreiver = vectorstore.as_retriever()

docs =  retreiver.invoke("explain deep learning")
for d in docs:
    print(d.page_content)
    print(d.metadata)