import streamlit as st
import os
import json

# --- CONFIGURATION ---
st.set_page_config(page_title="Clara AI Onboarding Dashboard", layout="wide")
st.title("Clara Answers - Automation Pipeline Dashboard")
st.markdown("This dashboard visualizes the zero-cost onboarding automation pipeline, displaying batch processing metrics and a version-controlled diff viewer.")

# Path to your outputs folder
OUTPUT_DIR = "outputs/accounts"

# --- HELPER FUNCTIONS ---
def load_json(filepath):
    """Safely load a JSON file if it exists."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def get_processed_accounts():
    """Scan the outputs directory for processed accounts."""
    if not os.path.exists(OUTPUT_DIR):
        return []
    return sorted([d for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))])

# --- DATA EXTRACTION & BATCH METRICS ---
accounts = get_processed_accounts()

total_accounts = len(accounts)
v1_completed = 0
v2_completed = 0
total_modifications = 0
account_data = {}

# Process all folders to generate summary metrics
for acc in accounts:
    acc_dir = os.path.join(OUTPUT_DIR, acc)
    v1_memo = load_json(os.path.join(acc_dir, "v1_memo.json"))
    v2_memo = load_json(os.path.join(acc_dir, "v2_memo.json"))
    changelog = load_json(os.path.join(acc_dir, "changelog.json"))
    v2_spec = load_json(os.path.join(acc_dir, "v2_agent_spec.json"))
    
    if v1_memo: v1_completed += 1
    if v2_memo: v2_completed += 1
    
    changes_count = 0
    if changelog:
        # DeepDiff outputs dictionaries categorized by change type (e.g., 'dictionary_item_added')
        for change_type, changes in changelog.items():
            changes_count += len(changes)
        total_modifications += changes_count
        
    account_data[acc] = {
        "v1": v1_memo, 
        "v2": v2_memo, 
        "changelog": changelog, 
        "spec": v2_spec,
        "changes_count": changes_count
    }

# --- RENDER SUMMARY METRICS ---
st.header("Batch Processing Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Accounts Processed", total_accounts)
col2.metric("Demo (v1) Extractions", v1_completed)
col3.metric("Onboarding (v2) Updates", v2_completed)
col4.metric("Total Data Modifications", total_modifications)

st.markdown("---")

# --- UI INTERFACE & DIFF VIEWER ---
st.header("Account Versioning & Diff Viewer")

if total_accounts == 0:
    st.warning("No output data found. Please run your Python batch script first.")
else:
    # Sidebar or dropdown to select specific account
    selected_acc = st.selectbox("Select an Account to inspect changes:", accounts)
    data = account_data[selected_acc]
    
    st.markdown(f"### Highlights for `{selected_acc}`")
    
    # 1. Show the Changelog (The Diff)
    st.caption("Auto-generated JSON Diff (Changelog)")
    if data['changelog']:
        st.success(f"{data['changes_count']} structural changes applied during onboarding.")
        st.json(data['changelog'])
    else:
        st.info("No modifications detected between Demo and Onboarding.")

    # 2. Side-by-Side Diff Viewer
    st.markdown("### JSON Version Comparison")
    colA, colB = st.columns(2)
    
    with colA:
        st.subheader("Version 1 (Demo Memo)")
        if data['v1']:
            st.json(data['v1'])
        else:
            st.error("Missing v1 data.")
            
    with colB:
        st.subheader("Version 2 (Onboarding Memo)")
        if data['v2']:
            st.json(data['v2'])
        else:
            st.warning("Waiting for Onboarding update.")

    # 3. Final Production Asset
    st.markdown("---")
    st.markdown("### Final Retell Agent Specification")
    with st.expander("Click to view the deployable v2 AI Prompt Configuration"):
        if data['spec']:
            st.json(data['spec'])
        else:
            st.write("Agent spec not generated yet.")