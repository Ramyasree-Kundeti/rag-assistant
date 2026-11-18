from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7)
answer = llm.invoke("Explain retrieval-augmented generation in two sentences.")
print(answer.content)