# Clara Answers - Zero-Cost Onboarding Automation Pipeline

## Overview
This repository contains a zero-cost, end-to-end Python automation pipeline built for Clara AI. It converts messy, real-world customer conversations into deployable Retell AI Voice Agents. The system processes 6 demo calls (Version 1) and 6 onboarding calls (Version 2), calculates structural JSON diffs, and presents the metrics and version history via a Streamlit web dashboard.

This project was engineered to strictly adhere to a **zero-spend** constraint while maintaining high reliability, fast inference, and robust edge-case handling (such as truncating massive hour-long transcripts to respect free-tier API limits).

## Architecture and Data Flow
1. **Ingest & Normalize**: Reads raw text transcripts from local data directories. Massive transcripts are safely truncated to remain within free-tier API token limits without crashing.
2. **Extraction**: Uses the Groq Cloud API (`llama-3.1-8b-instant`) to securely extract structured Account Memos. Strict prompt hygiene prevents the AI from hallucinating missing information.
3. **Drafting**: Transforms the extracted operational memos into deployable Retell Agent Spec JSONs, strictly adhering to required business-hours and after-hours conversational flows.
4. **Versioning (Diff & Patch)**: Onboarding calls trigger a merge of new data, generating a `v2` memo, an updated `v2` agent spec, and computing a strict structural JSON diff (`changelog.json`).
5. **Dashboard UI**: A Streamlit web interface visualizes batch metrics and provides a side-by-side diff viewer for implementation teams to review changes.

## Directory Structure
```text
clara-onboarding-pipeline/
│
├── data/
│   ├── demo_transcripts/        # Place demo files here
│   └── onboarding_transcripts/  # Place onboarding files here
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
├── workflows/
│   └── n8n_workflow.json        # Orchestrator export for batch execution
│
├── app.py                       # Streamlit Dashboard UI
├── requirements.txt             # Project dependencies
└── README.md                    # Setup and architecture documentation
