import os
import pandas as pd
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
from datetime import datetime
import time
import litellm
import re

# Load API key securely from .env
load_dotenv()

# Groq LLM with built-in retries
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.1,
    max_retries=5  # CrewAI handles basic retries
)

# Agents
analyst = Agent(
    role="Lead Risk Strategy Consultant",
    goal="Assess technical and brand risk in tweets",
    backstory="PhD data scientist with 20 years in market risk and brand communication",
    verbose=False,
    allow_delegation=False,
    llm=groq_llm
)

critic = Agent(
    role="Chief Risk Compliance Officer",
    goal="Audit reports for accuracy, bias, and completeness",
    backstory="Senior compliance expert in real-time anomaly detection",
    verbose=False,
    allow_delegation=False,
    llm=groq_llm
)

# Tasks
task1 = Task(
    description="""Analyze this batch of tweets for technical risk, brand communication effectiveness, and market anomalies.
Data:
{data_snippet}

Output exactly this format:
- TECHNICAL RISK IDENTIFIED: 
- SEVERITY SCORE (1-10): 
- EVIDENCE: 
- STRATEGIC IMPACT:""",
    expected_output="Structured risk report in exact format",
    agent=analyst
)

task2 = Task(
    description="""Audit the analyst report above for accuracy, bias, completeness, and critical flaws.

Output exactly this format:
- AUDIT VERDICT: (Pass/Fail/Requires Revision)
- CRITICAL FLAWS:
- FINAL STRENGTHENED ASSESSMENT: (concise single paragraph)""",
    expected_output="Audit verdict and strengthened assessment",
    agent=critic,
    context=[task1]
)

# Crew
crew = Crew(
    agents=[analyst, critic],
    tasks=[task1, task2],
    verbose=False,
    process="sequential"
)

# Load and sample data
df = pd.read_csv("data/raw/chatgpt_daily_tweets.csv")
sample_df = df.sample(n=5000, random_state=42).reset_index(drop=True)

# Config
batch_size = 20
checkpoint_file = "outputs/risk_report_5000sample_checkpoint.csv"
final_file = "outputs/risk_report_5000sample_final.csv"

# Load existing progress if any
results = []
start_idx = 0
if os.path.exists(checkpoint_file):
    checkpoint_df = pd.read_csv(checkpoint_file)
    results = checkpoint_df.to_dict('records')
    start_idx = len(results) * batch_size
    print(f"Resuming from batch {len(results) + 1} (row {start_idx})")

# Process batches
for i in range(start_idx, len(sample_df), batch_size):
    batch = sample_df.iloc[i:i+batch_size]
    snippet = batch[['tweet_created', 'text']].to_string(index=False)
    
    batch_num = len(results) + 1
    
    while True:
        try:
            result = crew.kickoff(inputs={"data_snippet": snippet})
            results.append({
                "Batch": f"Rows {i}-{min(i+batch_size-1, len(sample_df)-1)}",
                "Batch_Number": batch_num,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Refined_Analysis": str(result)
            })
            
            # Save checkpoint after every successful batch
            pd.DataFrame(results).to_csv(checkpoint_file, index=False)
            print(f"Batch {batch_num} complete — checkpoint saved")
            time.sleep(15)  # Polite delay
            break
            
        except litellm.RateLimitError as e:
            msg = str(e).lower()
            if "tokens per day" in msg or "tpd" in msg:
                wait_match = re.search(r"try again in ([\d\.]+[hm])", msg)
                wait = wait_match.group(1) if wait_match else "several hours"
                print(f"Daily token limit reached — pausing. Resume in {wait}.")
                print("Progress saved in checkpoint — safe to stop.")
                exit()
            else:
                wait_match = re.search(r"try again in ([\d\.]+)s", msg)
                wait_time = float(wait_match.group(1)) if wait_match else 20.0
                wait_time = min(wait_time + 10, 120)  # Progressive backoff
                print(f"Rate limit hit — pausing {wait_time:.0f}s...")
                time.sleep(wait_time)
                
        except Exception as e:
            print(f"Unexpected error on batch {batch_num}: {e}")
            pd.DataFrame(results).to_csv(checkpoint_file, index=False)
            raise

# Final save
pd.DataFrame(results).to_csv(final_file, index=False)
os.remove(checkpoint_file) if os.path.exists(checkpoint_file) else None  # Clean up
print(f"\nDone — {len(results)} batches processed")
print(f"Final report saved: {final_file}")