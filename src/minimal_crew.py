import os
import pandas as pd
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
from datetime import datetime
import time
import litellm
import re

load_dotenv()

# Groq LLM with auto-retries
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.1,
    max_retries=5
)

# Agents
analyst = Agent(role="Lead Risk Strategy Consultant", goal="Assess technical and brand risk in tweets", backstory="PhD data scientist, 20y market risk", verbose=False, allow_delegation=False, llm=groq_llm)
critic = Agent(role="Chief Risk Compliance Officer", goal="Audit reports for accuracy and bias", backstory="Senior compliance expert", verbose=False, allow_delegation=False, llm=groq_llm)

# Tasks
task1 = Task(description="""Analyze this batch of tweets for technical risk, brand communication, and anomalies.
Data: {data_snippet}
Output exactly:
- TECHNICAL RISK IDENTIFIED: 
- SEVERITY SCORE (1-10): 
- EVIDENCE: 
- STRATEGIC IMPACT:""", expected_output="Structured report", agent=analyst)

task2 = Task(description="""Audit the analyst report for accuracy, bias, completeness.
Output exactly:
- AUDIT VERDICT: (Pass/Fail/Requires Revision)
- CRITICAL FLAWS:
- FINAL STRENGTHENED ASSESSMENT: (concise paragraph)""", expected_output="Audit verdict", agent=critic, context=[task1])

crew = Crew(agents=[analyst, critic], tasks=[task1, task2], verbose=False, process="sequential")

# 5000-tweet sample
df = pd.read_csv("data/raw/chatgpt_daily_tweets.csv")
sample_df = df.sample(n=5000, random_state=42).reset_index(drop=True)

# Batching
batch_size = 20
checkpoint = "outputs/risk_report_5000sample_checkpoint.csv"
final = "outputs/risk_report_5000sample_final.csv"
results = []

if os.path.exists(checkpoint):
    results = pd.read_csv(checkpoint).to_dict('records')
    start = len(results) * batch_size
else:
    start = 0

for i in range(start, len(sample_df), batch_size):
    batch = sample_df.iloc[i:i+batch_size]
    snippet = batch[['tweet_created', 'text']].to_string(index=False)
    
    while True:
        try:
            result = crew.kickoff(inputs={"data_snippet": snippet})
            results.append({"Batch": f"{i}-{i+batch_size-1}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "Refined_Analysis": result.raw})
            pd.DataFrame(results).to_csv(checkpoint, index=False)
            print(f"Batch {len(results)} complete — checkpoint saved")
            time.sleep(15)
            break
        except litellm.RateLimitError as e:
            msg = str(e)
            if "tokens per day" in msg or "TPD" in msg:
                wait_match = re.search(r"try again in ([\d\.]+[hm])", msg)
                wait = wait_match.group(1) if wait_match else "several hours"
                print(f"Daily token limit reached — pausing. Resume in {wait}.")
                print("Progress saved in checkpoint — safe to stop.")
                exit()
            else:
                wait_match = re.search(r"try again in ([\d\.]+)s", msg)
                wait_time = float(wait_match.group(1)) if wait_match else 15.0
                wait_time = min(wait_time + 5, 60)
                print(f"Rate limit — pausing {wait_time:.0f}s...")
                time.sleep(wait_time)
        except Exception as e:
            print(f"Unexpected error: {e}")
            pd.DataFrame(results).to_csv(checkpoint, index=False)
            raise

pd.DataFrame(results).to_csv(final, index=False)
print(f"Done — final report: {final} ({len(results)} batches)")