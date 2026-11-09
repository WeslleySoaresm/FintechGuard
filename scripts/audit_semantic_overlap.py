
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/fintechguard_train.csv")

df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
df = df.dropna(subset=["text", "intent"])

# Analisa apenas as três categorias envolvidas
# na falha de classificação.
selected = df[
    df["intent"].isin([
        "billing inquiry",
        "refund request",
        "cancellation request"
    ])
].drop_duplicates(subset=["text"]).reset_index(drop=True)

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    sublinear_tf=True
)

matrix = vectorizer.fit_transform(selected["text"])

similarity = cosine_similarity(matrix)

results = []

for i in range(len(selected)):
    for j in range(i + 1, len(selected)):
        if selected.iloc[i]["intent"] == selected.iloc[j]["intent"]:
            continue

        score = similarity[i, j]

        if score >= 0.65:
            results.append({
                "similarity": round(float(score), 3),
                "intent_a": selected.iloc[i]["intent"],
                "text_a": selected.iloc[i]["text"],
                "intent_b": selected.iloc[j]["intent"],
                "text_b": selected.iloc[j]["text"],
            })

results.sort(
    key=lambda item: item["similarity"],
    reverse=True
)

print("\n=== SOBREPOSIÇÃO ENTRE CATEGORIAS ===")
print(f"Pares encontrados: {len(results)}")

for item in results[:20]:
    print("\n" + "=" * 70)
    print("Similaridade:", item["similarity"])
    print(f"[{item['intent_a']}] {item['text_a']}")
    print(f"[{item['intent_b']}] {item['text_b']}")
