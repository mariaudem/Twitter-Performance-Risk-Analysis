import pandas as pd

df = pd.read_csv("outputs/risk_report_5000sample_final.csv")

# Filter for strong, readable outputs
candidates = df[
    (df['Refined_Analysis'].str.contains('Pass|Requires Revision', case=False)) &
    (df['Refined_Analysis'].str.len() > 200) &
    (df['Refined_Analysis'].str.len() < 3000)
]

# Prefer Passed first, then Requires Revision
passed = candidates[candidates['Refined_Analysis'].str.contains('Pass', case=False)]
revision = candidates[candidates['Refined_Analysis'].str.contains('Requires Revision', case=False)]

samples = []
if len(passed) >= 2:
    samples.extend(passed.sample(n=2, random_state=42).index.tolist())
if len(revision) >= 1:
    samples.extend(revision.sample(n=1, random_state=42).index.tolist())
if len(samples) < 3 and len(candidates) > len(samples):
    samples.extend(candidates.drop(samples).sample(n=3-len(samples), random_state=42).index.tolist())

samples = samples[:3]  # Exactly 3

print("=== COPY THESE 3 SAMPLES INTO README ===")
for i, idx in enumerate(samples, 1):
    batch = df.loc[idx, 'Batch']
    analysis = df.loc[idx, 'Refined_Analysis']
    verdict = 'Passed' if 'Pass' in analysis else 'Requires Revision'
    print(f"\n{i}. **Batch {batch} – {verdict}**")
    print("   ```")
    print(analysis.strip())
    print("   ```")