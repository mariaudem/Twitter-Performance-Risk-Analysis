import pandas as pd
from crewai import Agent, Task, Crew, LLM
import os
from datetime import datetime

# Groq LLM
groq_llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.1)

# Agents (same as baseline)
analyst = Agent(
    role="Lead Risk Strategy Consultant",
    goal="Conduct rigorous technical risk assessment of tweet data",
    backstory="PhD data scientist with 20 years in brand communication and market risk",
    verbose=False,  # quieter for real batch
    allow_delegation=False,
    llm=groq_llm
)

critic = Agent(
    role="Chief Risk Compliance Officer",
    goal="Audit risk reports for accuracy, bias, and critical flaws",
    backstory="Senior compliance executive specialized in real-time market anomaly detection",
    verbose=False,
    allow_delegation=False,
    llm=groq_llm
)

# Tasks
task1 = Task(
    description="""
    Analyze these tweet texts for technical risk, brand communication effectiveness, and market anomalies.
    Data:
    {data_snippet}
    
    Output exactly:
    - TECHNICAL RISK IDENTIFIED: 
    - SEVERITY SCORE (1-10): 
    - EVIDENCE: 
    - STRATEGIC IMPACT:
    """,
    expected_output="Structured risk report in exact format",
    agent=analyst
)

task2 = Task(
    description="""
    Audit the following analyst report for accuracy, bias, completeness, and critical flaws.
    Use the previous task output as the report to audit.
    
    Output exactly:
    - AUDIT VERDICT: (Pass/Fail/Requires Revision)
    - CRITICAL FLAWS:
    - FINAL STRENGTHENED ASSESSMENT: (concise single paragraph)
    """,
    expected_output="Audit verdict and strengthened assessment",
    agent=critic,
    context=[task1]
)

crew = Crew(agents=[analyst, critic], tasks=[task1, task2], verbose=False, process="sequential")

# Load real data
df = pd.read_csv("chatgpt_daily_tweets.csv")
batch = df['text'].sample(n=50, random_state=42)

# Run
result = crew.kickoff(inputs={"data_snippet": batch.to_string(index=False)})

# Save checkpoint
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
filename = f"risk_report_batch50_{timestamp}.csv"
pd.DataFrame([{"batch_size": 50, "timestamp": timestamp, "full_audited_report": result}]).to_csv(filename, index=False)

print(f"\n=== BATCH COMPLETE ===\nSaved to: {filename}")
print(result)