from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

model = ChatMistralAI(
    model="mistral-large-latest"
)

response = model.invoke("What is the capital of France?")

print(response.content)