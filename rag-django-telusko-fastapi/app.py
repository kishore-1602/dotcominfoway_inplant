from fastapi import FastAPI, HTTPException, Query




def format_sources(knn_indices, scores):
sources = []
for i, idx in enumerate(knn_indices):
m = metadata[idx]
sources.append({
"video_title": m["video_title"],
"video_url": m["video_url"],
"chunk_index": m.get("chunk_index"),
"start": m.get("start"),
"text_snippet": m.get("text")[:320],
"score": float(scores[i])
})
return sources




def simple_generate_answer(question, retrieved_snippets):
ctx = "\n\n".join([f"- {s['text'][:300]}" for s in retrieved_snippets])
answer = f"Answer (based on Telusko Django tutorial snippets):\n\n{ctx}\n\nQ: {question}\n\nShort summary: This is a synthesized answer from the retrieved Telusko snippets. (Replace with an actual LLM for high-quality answers.)"
return answer




@app.post("/query")
def query(payload: QueryPayload):
q = payload.q
top_k = payload.top_k or K
q_emb = embedder.encode([q]).astype("float32")
D, I = index.search(q_emb, top_k)
indices = I[0].tolist()
dists = D[0].tolist()
retrieved = [metadata[idx] for idx in indices]
answer = simple_generate_answer(q, retrieved)
sources = format_sources(indices, dists)


# simple related topics: most common longer words
combined = " ".join([r["text"] for r in retrieved])
words = [w.lower().strip(".,()[]") for w in combined.split() if len(w) > 4]
from collections import Counter
top = [w for w, _ in Counter(words).most_common(6)]


return {
"question": q,
"answer": answer,
"sources": sources,
"related_topics": top
}




@app.get("/speak")
def speak(text: str = Query(..., min_length=1)):
tts = gTTS(text)
tmp_file = os.path.join(tempfile.gettempdir(), f"tts_{uuid.uuid4().hex}.mp3")
tts.save(tmp_file)
return FileResponse(tmp_file, media_type="audio/mpeg", filename="answer.mp3")