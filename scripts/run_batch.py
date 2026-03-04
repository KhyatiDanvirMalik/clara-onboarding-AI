import os
from pipeline import process_transcript

DEMO_DIR = "../data/demo_transcripts"
ONBOARDING_DIR = "../data/onboarding_transcripts"

def run_batch():
    # 1. Process all demos (v1)
    if os.path.exists(DEMO_DIR):
        for filename in os.listdir(DEMO_DIR):
            if filename.endswith(".txt"):
                account_id = filename.split(".")[0] # Assumes file is named account123.txt
                with open(os.path.join(DEMO_DIR, filename), 'r') as f:
                    process_transcript(account_id, f.read(), "demo")
                    
    # 2. Process all onboarding (v2)
    if os.path.exists(ONBOARDING_DIR):
        for filename in os.listdir(ONBOARDING_DIR):
            if filename.endswith(".txt"):
                account_id = filename.split(".")[0]
                with open(os.path.join(ONBOARDING_DIR, filename), 'r') as f:
                    process_transcript(account_id, f.read(), "onboarding")

if __name__ == "__main__":
    run_batch()