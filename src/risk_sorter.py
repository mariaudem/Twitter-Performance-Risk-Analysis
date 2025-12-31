import pandas as pd
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv

load_dotenv()

# LLM - zero temperature for strict formatting
sorter_llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.0)

# Risk Sorter Agent
sorter = Agent(
    role="Risk Intelligence Aggregator",
    goal="Synthesize and prioritize technical risks across the full report",
    backstory="Senior risk analyst expert at distilling hundreds of findings into executive priorities",
    verbose=False,
    allow_delegation=False,
    llm=sorter_llm
)

# Task - clean list with short intro and closing
task_sort = Task(
    description="""
    You are an executive risk summarizer. Extract and rank the 10 most severe technical risks from the full report below.

    Input data (CSV content):
    {report_content}

    Output exactly this format and nothing else:

    The top 10 technical risks associated with ChatGPT are:

    1. [Concise risk description] – Severity: X/10
    2. [Concise risk description] – Severity: X/10
    3. [Concise risk description] – Severity: X/10
    4. [Concise risk description] – Severity: X/10
    5. [Concise risk description] – Severity: X/10
    6. [Concise risk description] – Severity: X/10
    7. [Concise risk description] – Severity: X/10
    8. [Concise risk description] – Severity: X/10
    9. [Concise risk description] – Severity: X/10
    10. [Concise risk description] – Severity: X/10

    These risks have significant strategic implications for individuals, organizations, and society as a whole, and it is essential to develop strategies to mitigate them and ensure the safe and responsible use of ChatGPT.

    No extra text, thoughts, headings, or repetition.
    """,
    expected_output="Intro sentence + single numbered list + closing sentence",
    agent=sorter
)

crew = Crew(agents=[sorter], tasks=[task_sort], verbose=True)

# Load final report
df = pd.read_csv("outputs/risk_report_5000sample_final.csv")
report_text = df.to_csv(index=False)

# Run sorter
print("\n=== Generating Executive Summary ===")
result = crew.kickoff(inputs={"report_content": report_text})

# Save to EXECUTIVE_SUMMARY.md (overwrite old one)
with open("EXECUTIVE_SUMMARY.md", "w", encoding="utf-8") as f:
    f.write(str(result))

print("\nExecutive summary saved to EXECUTIVE_SUMMARY.md")