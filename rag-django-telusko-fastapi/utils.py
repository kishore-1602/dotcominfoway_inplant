import os
import json


DATA_DIR = os.getenv("DATA_DIR", "data")




def load_metadata(path=None):
p = path or os.path.join(DATA_DIR, "metadata.json")
with open(p, "r", encoding="utf-8") as f:
return json.load(f)