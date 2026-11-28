import csv
from datetime import datetime
from pathlib import Path
from answers import store, rewrite_query, translate_to_german
from langdetect import detect


BASE = Path(__file__).parent
RESULTS_FILE = BASE/"eval_results.csv"

# Change this name every time you try something new
#EXPERIMENT = "baseline: e5-small, chunk 500"
#EXPERIMENT = "paragraph chunking (max 1200), headers removed"
#EXPERIMENT = "model changed to intfloat/multilingual-e5-base"
#EXPERIMENT = "12 questions, e5-base, paragraph chunks, query translation"
#EXPERIMENT = "query rewrite to legal German terms"
EXPERIMENT = "translation (re-run, reproducible)"


# Test questions, each with a phrase that only the correct chunk contains
TEST_SET = [
    {
        "question": "Wer hat an einer Kreuzung ohne Verkehrszeichen Vorfahrt?",
        "answer_contains": "hat die Vorfahrt, wer von rechts kommt",
    },
    {
        "question": "Who has right of way at a crossing without traffic signs?",
        "answer_contains": "hat die Vorfahrt, wer von rechts kommt",
    },
    {
        "question": "Wie schnell darf man innerorts fahren?",
        "answer_contains": "geschlossener Ortschaften für alle Kraftfahrzeuge 50 km/h"
    },
    {
        "question": "What is the speed limit in towns?",
        "answer_contains": "geschlossener Ortschaften für alle Kraftfahrzeuge 50 km/h"
    },
    {
        "question": "Wo muss man auf der Fahrbahn fahren?",
        "answer_contains": "möglichst weit rechts zu fahren"
    }, {
        "question": "Which side of the road must you drive on?",
        "answer_contains": "möglichst weit rechts zu fahren"
    },
    {
        "question": "Muss man sich anschnallen?",
        "answer_contains": "Sicherheitsgurte müssen während der Fahrt angelegt sein"
    },
    {
        "question": "Do I have to wear a seatbelt?",
        "answer_contains": "Sicherheitsgurte müssen während der Fahrt angelegt sein"
    },
    {
        "question": "Wer hat am Zebrastreifen Vorrang?",
        "answer_contains": "An Fußgängerüberwegen haben Fahrzeuge"
    }, {
        "question": "Who has priority at a zebra crossing?",
        "answer_contains": "An Fußgängerüberwegen haben Fahrzeuge"
    },
    {
        "question": "Darf ich beim Fahren das Handy benutzen?",
        "answer_contains": "weder aufgenommen noch gehalten"
    },
    {
        "question": "Can I use my phone while driving?",
        "answer_contains": "weder aufgenommen noch gehalten"
    }
]

K = 10  # how many results to look at

def normalise(text):
    return " ".join(text.split()).lower()

def find_rank(store,question,phrase):
    """Return the position (1-10) of the first chunk containing the phrase, or None."""
    lang = detect(question)
    german_q = question if lang == 'de' else translate_to_german(question)
    #german_q = rewrite_query(question)
    print("trsnalated: ",german_q)
    results = store.similarity_search(german_q,k=K)
    for rank, doc in enumerate(results,start=1):
        if normalise(phrase) in normalise(doc.page_content):
            return rank
    return None


rows =[]
for item in TEST_SET:
    rank = find_rank(store,item["question"],item["answer_contains"])
    rows.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "experiment": EXPERIMENT,
        "question": item["question"],
        "rank": rank if rank else "not found",
        "in_top_3": rank is not None and rank <= 3,
    })
    print(f"{str(rank or 'not found'):>10}  {item['question']}")

hits = sum(r["in_top_3"] for r in rows)
print(f"\n{EXPERIMENT}: {hits}/{len(rows)} questions have the answer in the top 3")

# Append this run to the results file
new_file = not RESULTS_FILE.exists()
with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    if new_file:
        writer.writeheader()
    writer.writerows(rows)
store.client.close()