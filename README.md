# Clara Answers - Zero-Cost Onboarding Automation Pipeline

## Overview
[cite_start]This repository contains a zero-cost, end-to-end Python automation pipeline built for Clara AI[cite: 2]. [cite_start]It converts messy, real-world customer conversations into deployable Retell AI Voice Agents[cite: 5, 274, 275]. [cite_start]The system processes 6 demo calls (Version 1) and 6 onboarding calls (Version 2) [cite: 62, 63, 231, 253][cite_start], calculates structural JSON diffs[cite: 29], and presents the metrics and version history via a Streamlit web dashboard.

[cite_start]This project was engineered to strictly adhere to a **zero-spend** constraint while maintaining high reliability, fast inference, and robust edge-case handling (such as truncating massive hour-long transcripts to respect free-tier API limits)[cite: 32].

## Architecture and Data Flow
1. [cite_start]**Ingest & Normalize**: Reads raw text transcripts from local data directories[cite: 129]. Massive transcripts are safely truncated to remain within free-tier API token limits without crashing.
2. [cite_start]**Extraction**: Uses the Groq Cloud API (`llama-3.1-8b-instant`) to securely extract structured Account Memos[cite: 20]. [cite_start]Strict prompt hygiene prevents the AI from hallucinating missing information[cite: 114, 117].
3. [cite_start]**Drafting**: Transforms the extracted operational memos into deployable Retell Agent Spec JSONs, strictly adhering to required business-hours and after-hours conversational flows[cite: 21, 118, 119, 120].
4. [cite_start]**Versioning (Diff & Patch)**: Onboarding calls trigger a merge of new data, generating a `v2` memo, a updated `v2` agent spec, and computing a strict structural JSON diff (`changelog.json`)[cite: 27, 28, 29, 97].
5. [cite_start]**Dashboard UI**: A Streamlit web interface visualizes batch metrics and provides a side-by-side diff viewer for implementation teams to review changes[cite: 172, 173, 174].

## Directory Structure
```text
clara-onboarding-pipeline/
│
├── data/
│   ├── demo_transcripts/        
│   └── onboarding_transcripts/ 
│
├── outputs/
│   └── accounts/                # Generated JSONs, specs, and diffs are saved here
│
├── scripts/
│   ├── prompts.py               # Enforces strict prompt hygiene and JSON schemas
│   ├── llm_client.py            # API integration with Groq (Zero-cost LLM execution)
│   ├── pipeline.py              # Core logic for extraction, merging, and versioning
│   └── run_batch.py             # Idempotent batch processor for all accounts
│
├── app.py                       # Streamlit Dashboard UI
├── requirements.txt             # Project dependencies
└── README.md                    # Setup and architecture documentation

```
Setup InstructionsEnsure Python 3.10+ is installed on your system.Clone this repository and navigate into the root directory.Create and activate a virtual environment:Bashpython -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
Install the required dependencies:Bashpip install -r requirements.txt
Set your Groq API key as an environment variable (Required to execute the free-tier LLM calls):Bashexport GROQ_API_KEY="gsk_your_key_here" # Mac/Linux
$env:GROQ_API_KEY="gsk_your_key_here"   # Windows PowerShell
How to Plug in the Dataset FilesPlace the 6 demo transcripts (.txt files) in /data/demo_transcripts/.Place the 6 onboarding transcripts in /data/onboarding_transcripts/.Important: The filenames must exactly match across both folders to act as the account_id primary key (e.g., apexfire.txt in both folders).Execution: How to Run Locally1. Run the Batch ProcessorTo execute the pipeline end-to-end on the entire dataset, run:Bashcd scripts
python run_batch.py
Outputs are deterministically generated and stored in /outputs/accounts/<account_id>/. Inside each account folder, you will find v1_memo.json, v2_memo.json, changelog.json, and the final v2_agent_spec.json.2. Launch the UI DashboardTo view the structural diffs, versioning, and summary metrics via the web UI:Bash# Ensure you are in the root project directory
streamlit run app.py

