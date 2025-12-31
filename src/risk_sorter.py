import pandas as pd
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv

load_dotenv()

# LLM (low temperature for consistent formatting)
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

# Single task – top risks only
task_sort = Task(
    description="""
    Read the full batch-level risk report below.

    Input data (CSV content):
    {report_content}

    Output exactly this format:

    ### Top Technical Risks (prioritized by severity)

    1. [Clear risk description] – Severity: [X]/10
    2. [Clear risk description] – Severity: [X]/10
    3. [Clear risk description] – Severity: [X]/10
    4. [Clear risk description] – Severity: [X]/10
    5. [Clear risk description] – Severity: [X]/10
    6. [Clear risk description] – Severity: [X]/10
    7. [Clear risk description] – Severity: [X]/10
    8. [Clear risk description] – Severity: [X]/10
    9. [Clear risk description] – Severity: [X]/10
    10. [Clear risk description] – Severity: [X]/10

    List the 10 highest-severity risks derived from the data.
    Keep descriptions concise and professional.
    No tables, no batch counts, no additional sections.
    """,
    expected_output="Clean numbered list of top 10 risks by severity",
    agent=sorter
)

crew = Crew(agents=[sorter], tasks=[task_sort], verbose=True)

# Load final report
df = pd.read_csv("outputs/risk_report_5000sample_final.csv")
report_text = df.to_csv(index=False)

# Run sorter
print("\n=== Generating Top 10 Risks Summary ===")
result = crew.kickoff(inputs={"report_content": report_text})

# Save clean result
with open("outputs/executive_risk_summary.md", "w", encoding="utf-8") as f:
    f.write(str(result))

print("\nTop risks summary saved to outputs/executive_risk_summary.md")