import os
import json
import time
from deepdiff import DeepDiff
from prompts import MEMO_EXTRACTION_PROMPT, AGENT_SPEC_PROMPT
from llm_client import call_local_llm

OUTPUT_DIR = "../outputs/accounts"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def process_transcript(account_id, transcript_text, stage):
    print(f"Processing {stage} for Account: {account_id}")
    account_dir = os.path.join(OUTPUT_DIR, account_id)
    ensure_dir(account_dir)
    
    version = "v1" if stage == "demo" else "v2"
    
    # TRUNCATION SAFEGUARD: Keep the transcript under ~12,000 words to avoid API crashes
    max_chars = 60000 
    if len(transcript_text) > max_chars:
        print(f"   [*] Transcript is massive. Truncating to fit free-tier limits...")
        transcript_text = transcript_text[:max_chars]
    
    # 1. Extract Memo
    prompt = MEMO_EXTRACTION_PROMPT.replace("{transcript}", transcript_text)
    memo_data = call_local_llm(prompt)
    
    if not isinstance(memo_data, dict):
        memo_data = {}
        
    memo_data["account_id"] = account_id
    
    # Merge v2 with v1 and create changelog
    if stage == "onboarding":
        v1_memo = load_json(os.path.join(account_dir, "v1_memo.json"))
        if v1_memo:
            diff = DeepDiff(v1_memo, memo_data, ignore_order=True)
            changelog = json.loads(diff.to_json())
            save_json(os.path.join(account_dir, "changelog.json"), changelog)
            
            for k, v in memo_data.items():
                if not v and v1_memo.get(k):
                    memo_data[k] = v1_memo[k]

    # Save Memo
    save_json(os.path.join(account_dir, f"{version}_memo.json"), memo_data)
    
    # 2. Generate Agent Spec
    spec_prompt = AGENT_SPEC_PROMPT.replace("{memo}", json.dumps(memo_data)).replace("{version}", version)
    agent_spec = call_local_llm(spec_prompt)
    
    # Save Agent Spec
    save_json(os.path.join(account_dir, f"{version}_agent_spec.json"), agent_spec)
    print(f"Saved {version} assets for {account_id}")
    
    # RATE LIMIT SAFEGUARD: Pause slightly between files so we don't spam the API
    time.sleep(3)