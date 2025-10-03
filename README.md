# Cornerstone - Decentralized Micro-Manufacturing Network

**Powered by Google's Agent Development Kit (ADK)**

Cornerstone connects micro-manufacturers (CNC shops, 3D printing facilities) with high-demand distributors through AI-powered bid optimization and autonomous timeline management.

---

## Architecture

```
┌─────────────────────────────────────────────┐
│           Frontend (HTML/JS)                │
│  - dashboard.html                           │
│  - projects.html                            │
│  - admin.html (new)                         │
│  - demo.html (new)                          │
└──────────────┬──────────────────────────────┘
               │ HTTP Requests
               ↓
┌─────────────────────────────────────────────┐
│      Flask Backend (app.py)                 │
│  - /api/analyze-demand                      │
│  - /api/create-bid                          │
│  - /api/submit-bid                          │
│  - /api/close-bid                           │
│  - /api/update-timeline                     │
│  - /api/plan-logistics                      │
└──────────────┬──────────────────────────────┘
               │ Python imports
               ↓
┌─────────────────────────────────────────────┐
│         ADK Agents (5 total)                │
│  1. demand_agent                            │
│  2. bid_coordinator_agent                   │
│  3. cornerstone_agent                       │
│  4. timeline_agent                          │
│  5. logistics_agent                         │
│  6. master_orchestrator (SequentialAgent)   │
└──────────────┬──────────────────────────────┘
               │ Tool calls
               ↓
┌─────────────────────────────────────────────┐
│      Business Logic & Mock Data             │
│  - analyze_market_trends()                  │
│  - create_bid_window()                      │
│  - optimize_bids()                          │
│  - update_timeline()                        │
│  - plan_logistics()                         │
└─────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/capeie/devfest
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Up Google API Key

Create `.env` file:

```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

Get your API key from: https://aistudio.google.com/apikey

### 3. Start the Application

```bash
python backend/app.py
```

Open browser to: **http://localhost:5001**

---

## Features

### 🤖 **5 Specialized ADK Agents**

1. **Demand Analyzer** - Analyzes market trends from social media, forums, search data
2. **Bid Coordinator** - Manages bid windows, tracks participation, notifies winners
3. **Cornerstone Optimizer** - AI-powered bid selection to minimize costs
4. **Timeline Manager** - Handles manufacturer schedule updates and delays
5. **Logistics Coordinator** - Plans shipping routes and consolidation

### **17 Custom Tools**

**Demand Agent (3 tools):**
- `analyze_market_trends()` - Scrapes social media, forums, search trends for high-demand products
- `get_product_recommendations()` - Returns top products by demand score
- `calculate_demand_forecast()` - Predicts demand over 30/60/90 day timeframes

**Bid Coordinator Agent (4 tools):**
- `create_bid_window()` - Opens rolling bid window for a job
- `get_bid_status()` - Returns current bids and window status
- `close_bid_window()` - Closes window and prepares for optimization
- `notify_winners()` - Sends notifications to selected manufacturers

**Cornerstone Optimizer Agent (3 tools):**
- `optimize_bids()` - AI-powered selection of optimal manufacturer combination
- `get_job_details()` - Returns job specifications and requirements
- `list_manufacturers()` - Shows all registered manufacturers and capabilities

**Timeline Manager Agent (3 tools):**
- `update_timeline()` - Handles manufacturer schedule changes and delays
- `get_timeline_status()` - Returns current project timelines
- `send_message_to_manufacturer()` - Sends notifications about timeline updates

**Logistics Coordinator Agent (4 tools):**
- `plan_logistics()` - Creates shipping routes and consolidation plans
- `optimize_shipping_costs()` - Finds cheapest shipping combination
- `track_shipments()` - Returns real-time shipment tracking
- `coordinate_consolidation()` - Plans multi-manufacturer consolidation at distribution centers

### **Multi-Agent Orchestration**

**SequentialAgent Workflow:**
- `master_orchestrator_agent` uses ADK's `SequentialAgent` class
- Executes all 5 agents in sequence autonomously
- Agents share state via `InvocationContext`
- Demonstrates true multi-agent collaboration

---

## Testing

### Test Individual Agents (ADK Web UI)

```bash
adk web
```

Open http://localhost:8000 and select any agent:
- **demand_agent**: "What products are trending?"
- **bid_coordinator_agent**: "Open a bid for Widget Bracket, 5000 units, CNC"
- **cornerstone_agent**: "Optimize bids for KNICK_2025"
- **timeline_agent**: "MAKER_A needs 2 more days"
- **logistics_agent**: "Plan logistics for KNICK_2025 with MAKER_A, MAKER_C, MAKER_J"
- **master_orchestrator_agent**: "Execute complete workflow"

### Test Flask API

```bash
# Health check
curl http://localhost:5001/api/health

# Optimize bids
curl -X POST http://localhost:5001/api/optimize-bids \
  -H "Content-Type: application/json" \
  -d '{"job_id": "KNICK_2025", "required_qty": 5000, "required_skill": "CNC"}'

# Update timeline
curl -X POST http://localhost:5001/api/update-timeline \
  -H "Content-Type: application/json" \
  -d '{"maker_id": "MAKER_A", "new_completion_date": "2025-11-04", "reason": "equipment delay"}'

# Complete workflow (Flask orchestration)
curl -X POST http://localhost:5001/api/complete-workflow-flask

# Complete workflow (ADK SequentialAgent)
curl -X POST http://localhost:5001/api/complete-workflow-adk
```

### Test Frontend Integration

1. **Dashboard** (http://localhost:5001/dashboard)
   - Enter bid price and quantity
   - Click "Submit Bid"
   - See optimization results from API

2. **Projects** (http://localhost:5001/projects)
   - Click "Manage Project"
   - Type: "I need 2 more days"
   - See Timeline Manager response from API

---

## Project Structure

```
devfest/
├── backend/
│   ├── app.py                      # Flask server (18 endpoints)
│   ├── templates/                  # HTML pages
│   │   ├── index.html             # Landing page
│   │   ├── signup.html            # Registration
│   │   ├── login.html             # Login
│   │   ├── dashboard.html         # Bid submission (integrated)
│   │   └── projects.html          # Timeline Manager (integrated)
│   └── static/
│       └── js/
│           └── api.js             # API client library
├── demand_agent/                   # Market trend analysis
│   ├── agent.py                   # 3 tools
│   └── trend_data.py              # Mock trending products
├── bid_coordinator_agent/          # Bid lifecycle management
│   ├── agent.py                   # 4 tools
│   └── bid_windows.py             # Mock bid windows
├── cornerstone_agent/              # Bid optimization
│   ├── agent.py                   # 3 tools
│   └── data_mocks.py              # Mock manufacturers & bids
├── timeline_agent/                 # Schedule management
│   ├── agent.py                   # 3 tools
│   └── timeline_data.py           # Mock timelines
├── logistics_agent/                # Shipping & consolidation
│   ├── agent.py                   # 4 tools
│   └── shipping_data.py           # Mock logistics data
├── master_orchestrator_agent/      # SequentialAgent workflow
│   └── agent.py                   # Orchestrates all 5 agents
├── .env                           # GOOGLE_API_KEY
├── requirements.txt               # Dependencies
└── start.sh                       # Startup script
```

---

## License

MIT License - Built for Google ADK Hackathon 2025

## Contact

For questions or demo requests, see repository issues.
