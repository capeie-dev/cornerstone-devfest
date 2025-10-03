# Integration Testing Guide - Hybrid Orchestration

## Architecture Overview

We now have **TWO orchestration methods**:

### **Method 1: ADK SequentialAgent** (Pure ADK)
- `master_orchestrator_agent` uses ADK's `SequentialAgent`
- Executes 5 agents in sequence autonomously
- Agents share state via `InvocationContext`
- **Use for:** Demo to judges, showing ADK expertise

### **Method 2: Flask Orchestration** (Practical)
- Flask backend calls agent tools directly
- Full control over workflow logic
- Can add validation, error handling, business logic
- **Use for:** Frontend integration, production-ready

---

## Testing Method 1: ADK SequentialAgent

### **Via ADK Web UI:**

```bash
cd /Users/capeie/devfest
adk web
```

1. Open `http://localhost:8000`
2. Select `master_orchestrator_agent` from dropdown
3. Type prompt:
```
Execute the complete manufacturing workflow
```

**What happens:**
- demand_agent analyzes trends → outputs top product
- bid_coordinator_agent opens bid window → outputs job_id
- cornerstone_agent optimizes bids → outputs winners
- timeline_agent checks schedules → outputs timelines
- logistics_agent plans shipping → outputs delivery plan

**Check Events tab** to see all 5 agents executing in sequence!

---

## Testing Method 2: Flask Orchestration

### **Step 1: Install Flask Dependencies**

```bash
cd /Users/capeie/devfest
pip install flask flask-cors
```

### **Step 2: Start Flask Server**

```bash
python backend/app.py
```

Should see:
```
CORNERSTONE BACKEND API SERVER
Starting Flask server on http://localhost:5000
```

### **Step 3: Test Health Check**

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "agents": {
    "demand_agent": "active",
    "bid_coordinator": "active",
    "cornerstone_optimizer": "active",
    "timeline_manager": "active",
    "logistics_coordinator": "active",
    "master_orchestrator": "active"
  },
  "total_agents": 6,
  "total_tools": 17
}
```

### **Step 4: Test Individual Endpoints**

**Demand Analysis:**
```bash
curl -X POST http://localhost:5000/api/analyze-demand \
  -H "Content-Type: application/json" \
  -d '{"category": ""}'
```

**Bid Status:**
```bash
curl http://localhost:5000/api/bid-status/KNICK_2025
```

**Optimize Bids:**
```bash
curl -X POST http://localhost:5000/api/optimize-bids \
  -H "Content-Type: application/json" \
  -d '{"job_id": "KNICK_2025", "required_qty": 5000, "required_skill": "CNC"}'
```

**Update Timeline:**
```bash
curl -X POST http://localhost:5000/api/update-timeline \
  -H "Content-Type: application/json" \
  -d '{"maker_id": "MAKER_A", "new_completion_date": "2025-11-04", "reason": "equipment delay"}'
```

**Plan Logistics:**
```bash
curl -X POST http://localhost:5000/api/plan-logistics \
  -H "Content-Type: application/json" \
  -d '{"job_id": "KNICK_2025", "winning_makers": "MAKER_A,MAKER_C,MAKER_J"}'
```

### **Step 5: Test Complete Workflows**

**Flask Orchestration:**
```bash
curl -X POST http://localhost:5000/api/complete-workflow-flask
```

Expected: Step-by-step workflow execution with results from each stage

**ADK SequentialAgent Orchestration:**
```bash
curl -X POST http://localhost:5000/api/complete-workflow-adk
```

Expected: Result from SequentialAgent executing all 5 agents

---

## Comparing Both Methods

### **Test Side-by-Side:**

**Terminal 1:**
```bash
# Flask orchestration
curl -X POST http://localhost:5000/api/complete-workflow-flask
```

**Terminal 2:**
```bash
# ADK orchestration
curl -X POST http://localhost:5000/api/complete-workflow-adk
```

**Compare:**
- Flask: Returns structured workflow with clear steps
- ADK: Returns agent output (more conversational)

---

## Frontend Integration Test

### **Step 1: Update HTML to Include API Client**

Add to any page's `<head>`:
```html
<script src="/static/js/api.js"></script>
```

### **Step 2: Test from Browser Console**

Open `dashboard.html` in browser, open DevTools Console:

```javascript
// Test demand analysis
const demand = await analyzeDemand('');
console.log(demand);

// Test bid optimization
const optimize = await optimizeBids('KNICK_2025', 5000, 'CNC');
console.log(optimize);

// Test Flask workflow
const workflowFlask = await executeCompleteWorkflowFlask();
console.log(workflowFlask);

// Test ADK workflow
const workflowADK = await executeCompleteWorkflowADK();
console.log(workflowADK);
```

---

## Demo Script for Hackathon Judges

### **Part 1: Show ADK Multi-Agent Orchestration (2 min)**

```bash
adk web
```

1. Select `master_orchestrator_agent`
2. Prompt: "Execute complete workflow"
3. Show Events tab - point out 5 agents executing
4. Explain: "This is ADK's SequentialAgent orchestrating 5 specialized agents autonomously"

### **Part 2: Show Flask Backend (1 min)**

```bash
python backend/app.py
```

1. Show terminal with Flask running
2. Explain: "Flask provides REST API for frontend integration"
3. Show: `curl http://localhost:5000/api/health`
4. Explain: "17 endpoints, can call agents individually or trigger complete workflow"

### **Part 3: Show Frontend Integration (2 min)**

1. Open `dashboard.html` in browser
2. Click "Submit Bid" → Shows API call in DevTools Network tab
3. Open `projects.html`
4. Chat with Timeline Manager → Shows API call
5. Explain: "Frontend calls Flask, Flask calls agents, results display in real-time"

---

## Key Points to Emphasize

✅ **Two orchestration methods** - Shows deep ADK understanding  
✅ **SequentialAgent** - Proper multi-agent workflow pattern  
✅ **Flask integration** - Production-ready architecture  
✅ **5 specialized agents** - Each handles specific domain  
✅ **17 tools total** - Comprehensive business logic  

---

## Troubleshooting

### Flask won't start
```bash
pip install flask flask-cors
```

### CORS errors in browser
- Flask has `CORS(app)` enabled
- Check Flask is running on port 5000

### ADK SequentialAgent not working
- Verify all 5 agents work individually first
- Check `master_orchestrator_agent/__init__.py` exists

---

## Next Steps

After testing both methods:
1. ✅ Verify SequentialAgent works
2. ✅ Verify Flask endpoints work
3. → Integrate frontend pages with Flask API
4. → Build admin dashboard with both workflow buttons
5. → Create automated demo page

Ready to proceed with frontend integration?
