import os
chunk_text = full[start:end].strip()

chunks.append({"text": chunk_text, "start": None})
start += chunk_size - overlap
return chunks




def main(playlist_url, output_dir):
os.makedirs(output_dir, exist_ok=True)
vids = get_playlist_video_ids(playlist_url)
print(f"Found {len(vids)} videos in playlist.")
embedder = SentenceTransformer(EMBED_MODEL)


vectors = []
metadata = []


for v in vids:
vid = v["id"]
title = v["title"]
url = v["webpage_url"]
print("Processing:", title)
transcript = fetch_transcript(vid)
if not transcript:
print(" - skipping (no transcript)")
continue
chunks = transcript_to_chunks(transcript)
texts = [c["text"] for c in chunks]
if not texts:
continue
embeddings = embedder.encode(texts, show_progress_bar=True)
for idx, emb in enumerate(embeddings):
vectors.append(emb)
metadata.append({
"video_id": vid,
"video_title": title,
"video_url": url,
"chunk_index": idx,
"text": texts[idx],
"start": chunks[idx]["start"]
})


if not vectors:
print("No vectors created. Exiting.")
return


vectors = np.vstack(vectors).astype("float32")
d = vectors.shape[1]
index = faiss.IndexFlatL2(d)
index.add(vectors)


faiss_path = os.path.join(output_dir, "faiss_index.bin")
meta_path = os.path.join(output_dir, "metadata.json")
faiss.write_index(index, faiss_path)
with open(meta_path, "w", encoding="utf-8") as f:
json.dump(metadata, f, ensure_ascii=False, indent=2)


print("Saved FAISS index to:", faiss_path)
print("Saved metadata to:", meta_path)




if __name__ == "__main__":
parser = argparse.ArgumentParser()
parser.add_argument("--playlist_url", required=True)
parser.add_argument("--output_dir", default="data")
args = parser.parse_args()
main(args.playlist_url, args.output_dir)