import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt

# Load final report
df = pd.read_csv("outputs/risk_report_5000sample_final.csv")

# Extract AUDIT VERDICT
def get_verdict(text):
    match = re.search(r'AUDIT VERDICT:\s*(Pass|Fail|Requires Revision)', text, re.IGNORECASE)
    return match.group(1).title() if match else 'Unknown'

# Extract TECHNICAL RISK IDENTIFIED (cleaned)
def get_risk_type(text):
    match = re.search(r'TECHNICAL RISK IDENTIFIED:\s*(.+?)(?=\n- SEVERITY SCORE|\Z)', text, re.DOTALL | re.IGNORECASE)
    if match:
        risk = match.group(1).strip()
        risk = re.sub(r'\n+', ' ', risk).strip(' -*')
        return risk if risk else 'No specific risk identified'
    return 'No specific risk identified'

df['Verdict'] = df['Refined_Analysis'].apply(get_verdict)
df['Risk_Type'] = df['Refined_Analysis'].apply(get_risk_type)

# Overall summary (for reference)
print("=== Overall Audit Verdict Counts ===")
print(df['Verdict'].value_counts())

# Focus: Passed verdicts only
passed_df = df[df['Verdict'] == 'Pass']
print(f"\n=== Passed Verdicts Only ({len(passed_df)} out of 250 batches) ===")
print("Top 15 Risk Types in Passed Batches:")
passed_risks = passed_df['Risk_Type'].value_counts().head(15)
print(passed_risks)

print(f"\nUnique risk types in Passed batches: {len(passed_df['Risk_Type'].unique())}")

# Charts for Passed only
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Passed risk types bar
passed_risks.plot(kind='barh', ax=axs[0], color='seagreen')
axs[0].set_title('Top 15 Risk Types in Passed Batches')
axs[0].set_xlabel('Number of Batches')
axs[0].invert_yaxis()

# Verdict pie (overall for context)
df['Verdict'].value_counts().plot(kind='pie', ax=axs[1], autopct='%1.1f%%', startangle=90)
axs[1].set_title('Overall Verdict Distribution')
axs[1].set_ylabel('')

plt.tight_layout()
plt.show()