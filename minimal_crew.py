"""
BASELINE MINIMAL CREW - SUCCESSFUL RUN CONFIRMED 20 Dec 2025
================================================================
Dual-agent crew (Analyst → Critic) works end-to-end locally with Groq.
- Uses CrewAI + litellm + Groq (free tier)
- Sequential process with context=[task1] for proper handoff
- No OpenAI key required
- Tested on 3-tweet snippet → produced full audited result

Keep this file untouched as proof Phase 2 minimal crew is complete.
"""
import os
import pandas as pd
from crewai import Agent, Task, Crew, LLM

# Groq LLM (free tier)
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.1
)

# Agents
analyst = Agent(
    role="Lead Risk Strategy Consultant",
    goal="Conduct rigorous technical risk assessment of tweet data",
    backstory="PhD data scientist with 20 years in brand communication and market risk",
    verbose=True,
    allow_delegation=False,
    llm=groq_llm
)

critic = Agent(
    role="Chief Risk Compliance Officer",
    goal="Audit risk reports for accuracy, bias, and critical flaws",
    backstory="Senior compliance executive specialized in real-time market anomaly detection",
    verbose=True,
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
    context=[task1]  # Automatically passes task1 output to task2
)

# Crew
crew = Crew(
    agents=[analyst, critic],
    tasks=[task1, task2],
    verbose=True,
    process="sequential"
)

# Tiny test data
test_data = pd.DataFrame({
    "text": [
        "ChatGPT is down again, users furious",
        "Loving the new Groq features from xAI",
        "Brand X just launched a terrible campaign"
    ]
})

# Run
result = crew.kickoff(inputs={"data_snippet": test_data.to_string(index=False)})
print("\n=== FINAL AUDITED RESULT ===\n")
print(result)