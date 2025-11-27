import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download("stopwords")
nltk.download("wordnet")

df = pd.read_csv(r"C:\Users\ADMIN\Downloads\1429_1.csv", low_memory=False)

df = df.rename(columns={
    "reviews.text": "review_text",
    "reviews.rating": "rating",
    "categories": "product_category",
    "reviews.date": "review_date"
})

df.drop_duplicates(inplace=True)

df['review_text'] = df['review_text'].fillna("")
df['rating'] = df['rating'].fillna(df['rating'].median())
df['product_category'] = df['product_category'].fillna("Unknown")

df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')
df = df.dropna(subset=['review_date'])
df['review_date'] = df['review_date'].dt.tz_localize(None)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

df['clean_text'] = df['review_text'].astype(str).apply(clean_text)

df.to_csv(r"C:\Users\ADMIN\Downloads\cleaned_reviews.csv", index=False)

print("Total reviews:", len(df))
print("Most common product category:", df['product_category'].value_counts().idxmax())
print("\nAverage rating per category:\n", df.groupby('product_category')['rating'].mean())

from collections import Counter
all_words = " ".join(df['clean_text']).split()
top_words = Counter(all_words).most_common(10)
print("\nTop 10 most frequent words:")
for word, count in top_words:
    print(word, count)

plt.figure(figsize=(8,5))
sns.countplot(data=df, x='rating', hue='rating', palette="viridis", legend=False)
plt.title("Rating Distribution")
plt.tight_layout()
plt.savefig("rating_distribution.png")
plt.show()

df['year_month'] = df['review_date'].dt.to_period('M')
monthly_trend = df.groupby('year_month').size()

plt.figure(figsize=(10,5))
monthly_trend.plot(kind='line', marker='o')
plt.title("Monthly Review Trend")
plt.xlabel("Month")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig("monthly_trend.png")
plt.show()
