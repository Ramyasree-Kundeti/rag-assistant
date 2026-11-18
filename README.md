# RAG Assistant

A question-answering assistant that answers from your own documents using retrieval-augmented generation (RAG).

## What it will do

1. Load documents (PDFs) and split them into chunks
2. Turn the chunks into embeddings and store them in a vector database (Qdrant)
3. For each question, find the most relevant chunks
4. Send the question and those chunks to an LLM, which answers only from them

## Tech stack

- Python
- LangChain
- Groq (hosted Llama and open-source models)
- Qdrant (planned)
- FastAPI and Streamlit (planned)

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate          # on Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project folder:

```
GROQ_API_KEY=your_key_here
```

Then run:

```bash
python hello_llm.py
```

## Roadmap

-  First LLM call with LangChain and Groq
-  Load and chunk PDF documents
-  Embeddings and vector search with Qdrant
-  Answer questions from retrieved context
-  Evaluation of answer quality
-  REST API with FastAPI and a Streamlit demo
