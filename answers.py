from pathlib import Path
from langchain_qdrant import QdrantVectorStore
from embeddings import get_embeddings
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langdetect import detect

DB_PATH = Path(__file__).parent/"qdrant_db"
LANGUAGES = {"de": "German", "en": "English"}
load_dotenv()

store = QdrantVectorStore.from_existing_collection(embedding=get_embeddings(),
                                                   path=str(DB_PATH),collection_name="stvo")
llm = ChatGroq(model="openai/gpt-oss-20b",temperature=0)

def translate_to_german(question):
    prompt = f"""Translate the question to german.
    If it is already german then dont change. 
    Return only the question, no explantion.
    Question:{question}"""
    answer =  llm.invoke(prompt)
    return answer.content.strip()


def search(question,k=3):

    return store.similarity_search_with_score(question,k)

def build_context(docs):

    context = [f"[{doc.metadata['section']}, page {doc.metadata['page']}]\n{doc.page_content}" for doc, score in docs]

    return "\n\n".join(context)

def rewrite_query(question):
    prompt = f"""Rewrite the question as a German question.
    Use the formal legal terms that a German law text like the StVO would use.
    Keep the meaning. Return only the question, no explanation.

    Question: {question}"""
    answer = llm.invoke(prompt)
    return answer.content.strip()

def get_answer(q):
    print("Actual Question", q)
    lang = detect(q)
    german_q = q if lang == "de" else translate_to_german(q)
    #german_q = rewrite_query(q)
    print("Translated Question: ", german_q)
    docs = search(german_q, k=3)
    context = build_context(docs)
    prompt = f"""rules: Answer only using the context below.
                        If you don't find the answer in the context, then say i don't know.
                        write the answer in the language {LANGUAGES.get(lang,"English")}.
                        cite the § and page.
                        Give the answer in 2 to 4 sentences.
        context:{context}
        User Question:{q}
        Answer:"""
    answer = llm.invoke(prompt)
    return answer.content.strip()




if __name__ == "__main__":
    questions = [
        "wer hat an einer kreuzung ohne verkehrszeichen vorfahrt?",
        "who has right of way at a crossing without traffic signs",
        "What is the capital of France?",
    ]
    for q in questions:
        print("Question:", q)
        print("Answer:", get_answer(q))
        print("-" * 60)
    store.client.close()
