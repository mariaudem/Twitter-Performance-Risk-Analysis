# Autonomous Agentic Risk Intelligence: Twitter Analysis

Transition from manual monitoring to autonomous risk discovery using multi-agent AI on unstructured Twitter data.

## Strategic Mission
How can autonomous agents reduce manual overhead in social media monitoring while maintaining high precision in risk detection?

## Agent Architecture
- Hunter: High-recall anomaly detection across tweet batches
- Critic: Precision audit with severity scoring (1-10)
- Sorter: Dynamic prioritization across the full report

## Quick Start (Free & Local)
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install crewai crewai[tools] pandas python-dotenv litellm
cp .env.example .env           # Add your Groq API key 
python minimal_crew.py
python risk_sorter.py
```

## Tech Stack
- CrewAI multi-agent orchestration
- Groq Llama-3.3-70B (free tier + <€2 paid for rate limits)
- Python 3.12 + Pandas
- Processed 5,000-tweet Kaggle sample in ~20 minutes (~90% reduction vs. manual deep analysis)

## Key Outcomes
- Full audited report: outputs/risk_report_5000sample_final.csv
- Top 10 prioritized risks: [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
- Sample batch outputs: [SAMPLE_INSIGHTS.md](SAMPLE_INSIGHTS.md)

---
## Process Flow

```mermaid
flowchart TD
    A[Raw CSV] --> B[Load & Batch 20 tweets]
    B --> C[Hunter → Critic]
    C --> D[Audited Batch Report]
    D --> E[Checkpoint & Resume]
    E --> F{All batches complete?}
    F -->|No| B
    F -->|Yes| G[Save Final Report]
    G --> H[Risk Sorter Agent]
    H --> I[Executive Top-10 Summary]
```

---
## Skills Demonstrated
| Skill | Impact |
| :--- | :--- |
| **Agentic AI Orchestration** | Designing multi-agent workflows for complex analytical tasks. |
| **AI Governance** | Implementing self-correction loops to ensure data integrity. |
| **Cognitive Data Processing** | Transforming unstructured noise into structured, prioritized metrics. |
| **Scalable Risk Modeling** | Developing AI-driven frameworks for business-critical oversight. |

Star/fork if you're building agentic systems. Issues & PRs welcome!
