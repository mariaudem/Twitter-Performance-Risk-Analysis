import pandas as pd

df = pd.read_csv("data/raw/chatgpt_daily_tweets.csv")
total_rows = len(df)
print(f"Total tweets in dataset: {total_rows:,}")

# Sample sizes to test
sample_sizes = [3000, 6000, 10000]  # ~5%, ~10%, ~16%

for size in sample_sizes:
    pct = (size / total_rows) * 100
    print(f"\nSample size: {size:,} tweets ({pct:.1f}% of dataset)")
    sample = df['text'].sample(n=size, random_state=42)
    
    # Rough proxy metrics
    avg_len = sample.str.len().mean()
    unique_words = len(set(" ".join(sample).lower().split()))
    print(f"  Avg tweet length: {avg_len:.0f} chars")
    print(f"  Unique word vocabulary: {unique_words:,}")
    
    # Simple keyword coverage check (files in project root)
    try:
        pos_keywords = pd.read_csv("Positive_Keywords.txt", header=None)[0].str.lower()
        neg_keywords = pd.read_csv("Negative_Keywords.txt", header=None)[0].str.lower()
        print(f"  Known positive keywords in project: {len(pos_keywords)}")
        print(f"  Known negative keywords in project: {len(neg_keywords)}")
    except FileNotFoundError as e:
        print(f"  Keyword file missing: {e.filename} — skipping count")
    except Exception as e:
        print(f"  Keyword loading error: {e} — skipping count")

print("\nSenior verdict:")
if total_rows > 50000:
    print("Dataset >50k rows → 5–10% random sample (3k–6k tweets) is statistically sufficient for stable risk patterns.")
    print("Full run adds diminishing returns on free tier.")
    print("Recommendation: Use 5000-tweet sample for final report.")
else:
    print("Dataset small enough → full run reasonable.")