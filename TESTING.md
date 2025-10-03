# Cornerstone ADK Testing Guide

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Edit `.env` file and add your Google AI Studio API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

Get your API key from: https://aistudio.google.com/apikey

---

## Testing with ADK Web UI (Recommended)

### Launch the Dev UI
```bash
adk web
```

This will start the server at `http://localhost:8000`

### Test Cornerstone Orchestrator Agent

1. **Select Agent**: In the dropdown, choose `cornerstone_agent`

2. **Test Prompts**:

**Prompt 1 - Job Details:**
```
What's the current job opportunity?
```
Expected: Agent calls `get_job_details()` and describes KNICK_2025

**Prompt 2 - Bid Optimization (Main Demo):**
```
What's the cheapest way to fulfill job KNICK_2025?
```
Expected: Agent calls `optimize_bids(job_id='KNICK_2025', required_qty=5000, required_skill='CNC')` and summarizes:
- Total cost (~$11,875)
- 3 manufacturers selected (MAKER_C, MAKER_J, MAKER_A)
- Lead time (12 days)

**Prompt 3 - Manufacturer Listing:**
```
Show me all CNC manufacturers in the network
```
Expected: Agent calls `list_manufacturers(skill='CNC')` and lists 7 CNC makers

### Test Timeline Manager Agent

1. **Select Agent**: In the dropdown, choose `timeline_agent`

2. **Test Prompts**:

**Prompt 1 - Timeline Update (Main Demo):**
```
Maker_A has a delay, need 2 more days for KNICK_2025
```
Expected: Agent calls `update_timeline(maker_id='MAKER_A', new_completion_date='2025-11-04', reason='2-day delay')` and confirms update

**Prompt 2 - Status Check:**
```
What's the status of all manufacturers?
```
Expected: Agent calls `get_timeline_status()` and summarizes all timelines

**Prompt 3 - Communication:**
```
Send a message to MAKER_C asking about material availability
```
Expected: Agent calls `send_message_to_manufacturer()` and confirms delivery

---

## Testing with CLI

### Test Cornerstone Orchestrator
```bash
echo "Optimize bids for KNICK_2025" | adk run cornerstone_agent
```

### Test Timeline Manager
```bash
echo "Maker_A needs 2 extra days" | adk run timeline_agent
```

---

## Viewing Agent Execution Traces

In the ADK Web UI:
1. Click the **Events** tab on the left
2. See each function call with parameters
3. Click **Trace** button to see latency details

This proves the agent is calling your custom tools!

---

## Expected Optimization Results

For job KNICK_2025 (5000 CNC units):

**Winning Bids** (greedy algorithm, sorted by price):
1. **MAKER_C** (Texas CNC Works): 2,500 units @ $2.20/unit = $5,500
2. **MAKER_J** (Atlanta Rapid Proto): 2,000 units @ $2.35/unit = $4,700
3. **MAKER_A** (Precision CNC Ohio): 500 units @ $2.45/unit = $1,225

**Total Cost**: $11,425
**Lead Time**: 12 days (max of all selected makers)
**Manufacturers**: 3

---

## Troubleshooting

### "Agent not found in dropdown"
- Ensure you're running `adk web` from `/Users/capeie/devfest` (parent folder)
- Check that `__init__.py` files exist in both agent folders

### "API key error"
- Verify `.env` file has correct `GOOGLE_API_KEY`
- Get key from https://aistudio.google.com/apikey

### "Tool not being called"
- Check the Events tab to see agent reasoning
- Try more explicit prompts like "Call the optimize_bids tool for job KNICK_2025"
