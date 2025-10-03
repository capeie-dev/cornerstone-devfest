# Phase 1 Agent Testing Guide

## Setup

```bash
cd /Users/capeie/devfest
source .venv/bin/activate
adk web
```

Open browser to `http://localhost:8000`

---

## Agent 1: Demand Analyzer

**Select:** `demand_agent` from dropdown

### Test 1: Analyze Market Trends
**Prompt:**
```
What products are trending right now?
```

**Expected:**
- Agent calls `analyze_market_trends()`
- Shows 5 trending products
- Displays demand scores (0-10)
- Top recommendation: "Precision Widget Bracket" (9.2 score)

### Test 2: Get Recommendations
**Prompt:**
```
Give me product recommendations with demand score above 8
```

**Expected:**
- Agent calls `get_product_recommendations(min_demand_score=8.0)`
- Returns 3 products (Widget Bracket, Cable Organizer, Key Holder)
- Explains why each is recommended

### Test 3: Demand Forecast
**Prompt:**
```
What's the 60-day forecast for PROD_001?
```

**Expected:**
- Agent calls `calculate_demand_forecast(product_id='PROD_001', timeframe='60_days')`
- Shows forecasted volume: 8,500 units
- Confidence: 85%
- Recommendation: MANUFACTURE

---

## Agent 2: Bid Coordinator

**Select:** `bid_coordinator_agent` from dropdown

### Test 1: Create Bid Window
**Prompt:**
```
Open a bid window for Widget Bracket, 5000 units, CNC skill, 96 hours
```

**Expected:**
- Agent calls `create_bid_window()`
- Confirms bid window opened
- Shows closing date/time
- Reports 10 manufacturers notified

### Test 2: Check Bid Status
**Prompt:**
```
What's the status of KNICK_2025?
```

**Expected:**
- Agent calls `get_bid_status(job_id='KNICK_2025')`
- Shows: OPEN status
- 8 bids received
- 80% participation rate
- Competition stats (lowest: $2.20, highest: $3.20)

### Test 3: Close Bid Window
**Prompt:**
```
Close the bid window for KNICK_2025
```

**Expected:**
- Agent calls `close_bid_window(job_id='KNICK_2025')`
- Changes status to CLOSED
- Reports 8 total bids
- Says "Ready for optimization"

### Test 4: Notify Winners
**Prompt:**
```
Notify winners for KNICK_2025: MAKER_A got 1800 units at $2.45, MAKER_C got 2500 units at $2.20
```

**Expected:**
- Agent calls `notify_winners()`
- Sends notifications to 2 manufacturers
- Shows notification messages
- Confirms production can begin

---

## Agent 3: Logistics Coordinator

**Select:** `logistics_agent` from dropdown

### Test 1: Plan Logistics
**Prompt:**
```
Plan logistics for KNICK_2025 with manufacturers MAKER_A, MAKER_C, MAKER_J
```

**Expected:**
- Agent calls `plan_logistics(job_id='KNICK_2025', winning_makers='MAKER_A,MAKER_C,MAKER_J')`
- Shows consolidation center: Chicago
- Pickup schedule for 3 manufacturers
- Estimated cost: ~$450
- Final delivery date

### Test 2: Optimize Shipping Costs
**Prompt:**
```
Can we reduce shipping costs for KNICK_2025?
```

**Expected:**
- Agent calls `optimize_shipping_costs(job_id='KNICK_2025')`
- Shows current method and cost
- Compares ground, express, freight options
- Recommends cheapest option
- Shows potential savings

### Test 3: Track Shipments
**Prompt:**
```
Where are the shipments for KNICK_2025?
```

**Expected:**
- Agent calls `track_shipments(job_id='KNICK_2025')`
- Shows status for each manufacturer:
  - MAKER_A: IN_TRANSIT (Indianapolis)
  - MAKER_C: PENDING_PICKUP (Houston)
  - MAKER_J: PENDING_PICKUP (Atlanta)
- Reports 1 in transit, 2 pending

### Test 4: Coordinate Consolidation
**Prompt:**
```
When will all parts arrive at the consolidation center?
```

**Expected:**
- Agent calls `coordinate_consolidation(job_id='KNICK_2025')`
- Shows consolidation center location
- Lists all pickup dates
- Reports when consolidation completes
- Gives final delivery date

---

## Multi-Agent Workflow Test

Test the complete flow across all agents:

### Step 1: Demand Analysis
**Agent:** `demand_agent`
**Prompt:** "What should we manufacture next?"
**Result:** Recommends Widget Bracket (PROD_001)

### Step 2: Open Bid
**Agent:** `bid_coordinator_agent`
**Prompt:** "Create a bid for Widget Bracket, 5000 units, CNC"
**Result:** Bid window KNICK_2025 opened

### Step 3: Check Participation
**Agent:** `bid_coordinator_agent`
**Prompt:** "How many bids for KNICK_2025?"
**Result:** 8 bids, 80% participation

### Step 4: Close & Optimize
**Agent:** `bid_coordinator_agent`
**Prompt:** "Close KNICK_2025"
**Result:** Bid closed, ready for optimization

**Switch to:** `cornerstone_agent`
**Prompt:** "Optimize bids for KNICK_2025"
**Result:** 3 manufacturers selected, $11,425 total

### Step 5: Plan Logistics
**Agent:** `logistics_agent`
**Prompt:** "Plan shipping for KNICK_2025 with MAKER_A, MAKER_C, MAKER_J"
**Result:** Logistics plan created

### Step 6: Handle Delay
**Agent:** `timeline_agent`
**Prompt:** "MAKER_A needs 2 extra days"
**Result:** Timeline updated to Nov 4

**Back to:** `logistics_agent`
**Prompt:** "Update logistics for the delay"
**Result:** Adjusted consolidation schedule

---

## Viewing Tool Calls

In ADK Web UI:
1. Click **Events** tab (left sidebar)
2. See each function call with parameters
3. Click **Trace** to see execution time
4. Verify tools are being called correctly

---

## Expected Results Summary

| Agent | Tools | Test Status |
|-------|-------|-------------|
| demand_analyzer | 3 tools (analyze, recommend, forecast) | ✅ Ready to test |
| bid_coordinator_agent | 4 tools (create, status, close, notify) | ✅ Ready to test |
| logistics_agent | 4 tools (plan, optimize, track, consolidate) | ✅ Ready to test |
| cornerstone_agent | 3 tools (optimize, job details, list makers) | ✅ Already working |
| timeline_agent | 3 tools (update, status, message) | ✅ Already working |

**Total:** 5 agents, 17 tools

---

## Troubleshooting

### Agent not in dropdown
- Ensure you're in `/Users/capeie/devfest` when running `adk web`
- Check `__init__.py` exists in agent folder

### Tool not being called
- Check Events tab for errors
- Try more explicit prompts
- Verify tool function signatures match ADK requirements

### "Default value not supported" error
- Use empty string `""` instead of `None` for optional string parameters
- Already fixed in all agents

---

## Next Steps After Testing

Once all agents work:
1. ✅ Phase 1 complete
2. → Move to Phase 2: Flask backend integration
3. → Connect agents to frontend
4. → Build admin dashboard
5. → Create automated demo

