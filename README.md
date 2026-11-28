# RAG Assistant

A question-answering assistant that answers from your own documents using retrieval-augmented generation (RAG).
The demo uses the German road traffic regulations (StVO): ask in German or English, and it answers from the relevant paragraphs with a § citation, or says "I don't know".


## How it works

1. **Ingest** – `ingest.py` reads the StVO PDF with pypdf, removes page headers and page numbers, and cuts one chunk per § (long sections split at 1200 characters, heading repeated). 225 chunks.
2. **Index** – `build_index.py` embeds the chunks with `intfloat/multilingual-e5-base` and stores them in Qdrant (local mode).
3. **Answer** – `answers.py`:
   - detects the question's language (`langdetect`)
   - translates non-German questions to German (Groq LLM)
   - retrieves the top 3 chunks
   - asks the LLM to answer only from these chunks, in the user's language, citing § and page
   - says "I don't know" if the answer is not in the documents
4. **Evaluate** – `evaluate.py` checks whether the correct chunk is in the top 3 for 12 test questions (German + English) and logs each run to `eval_results.csv`.

## Tech stack

- Python
- LangChain
- Groq (model: openai/gpt-oss-20b)
- Multilingual embeddings: intfloat/multilingual-e5-base (sentence-transformers)
- Qdrant (local mode)
- langdetect
- FastAPI and Streamlit (planned)

## Sample data

`sample_data/StVO.pdf`: Straßenverkehrs-Ordnung (StVO), Bundesministerium der Justiz, https://www.gesetze-im-internet.de. Official work under §5 UrhG.

## How to run

1. `pip install -r requirements.txt`
2. Create a `.env` file with `GROQ_API_KEY=...`
3. `python build_index.py` (once)
4. `python answers.py`
5. `python evaluate.py` (optional)

## Example

**Q:** Who has right of way at a crossing without traffic signs?
**A(shortened):** At a crossing or junction that has no traffic signs, the right of way is given to the vehicle that comes from the right, unless a traffic sign regulates it differently (§ 8 StVO).

**Q:** What is the capital of France?
**A:** I don't know.

## Results

Retrieval hit rate = correct chunk in the top 3.

| Step | Change | Result |
|---|---|---|
| Baseline | e5-small, 500-character chunks | DE rank 1, EN not found (2 questions) |
| 1 | Chunk by § + remove headers | Clean § chunks with page metadata; score unchanged |
| 2 | e5-small → e5-base | EN: not found → rank 7 |
| 3 | Translate question to German before search | EN: rank 7 → rank 1 |
| 4 | 12-question test set | **8/12** |
| 5 | LLM rewrite into legal terms (tested) | 7/12 – helped 3, hurt 3; not kept |

Remaining misses are everyday words vs. legal terms ("Zebrastreifen" vs. "Fußgängerüberweg", "Handy" vs. "elektronisches Gerät").


## Roadmap


Done:
- First LLM call with LangChain and Groq
- Load the PDF and chunk it by paragraph (§), headers removed
- Embeddings and vector search with Qdrant
- Answers from retrieved context, with § and page citations
- German and English questions (language detection + translation)
- Retrieval evaluation with 12 test questions (8/12 in the top 3)

Next:
- Multi-query retrieval and hybrid search for the remaining misses
- Consistent citations in every answer
- Streamlit demo
- REST API with FastAPI, Docker, Azure
