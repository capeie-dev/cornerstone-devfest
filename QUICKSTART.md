# Cornerstone - Quick Start Guide

## Start the Application

```bash
cd /Users/capeie/devfest
source .venv/bin/activate
python backend/app.py
```

## Access the Application

Open your browser to:

**Main Application:**
- Landing Page: http://localhost:5000
- Dashboard: http://localhost:5000/dashboard
- Projects: http://localhost:5000/projects

**API Endpoints:**
- Health Check: http://localhost:5000/api/health
- API Info: http://localhost:5000/api/info

## User Flow

1. **Landing Page** (http://localhost:5000)
   - Click "Get Started" → Goes to signup

2. **Signup** (http://localhost:5000/signup)
   - Fill registration form
   - Click "Create Account" → Goes to dashboard

3. **Dashboard** (http://localhost:5000/dashboard)
   - View KNICK_2025 job opportunity
   - Enter bid price and quantity
   - Click "Submit Bid" → **Calls Flask API** → Shows optimization results

4. **Projects** (http://localhost:5000/projects)
   - Click "Manage Project" on KNICK_2025
   - Chat with Timeline Manager
   - Type: "I need 2 more days"
   - **Calls Flask API** → Bot responds with updated timeline

## Testing the Integration

### Test 1: Bid Submission
1. Go to http://localhost:5000/dashboard
2. Enter price: `2.35`
3. Enter quantity: `2000`
4. Click "Submit Bid"
5. **Expected:** Success message with optimization results

### Test 2: Timeline Manager
1. Go to http://localhost:5000/projects
2. Click "Manage Project"
3. Type in chat: `I need 3 more days`
4. Press Enter
5. **Expected:** Bot responds with updated completion date

## Verify API is Working

Open browser console (F12) and run:

```javascript
// Test optimization
fetch('http://localhost:5000/api/optimize-bids', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({job_id: 'KNICK_2025', required_qty: 5000, required_skill: 'CNC'})
})
.then(r => r.json())
.then(console.log);
```

## Troubleshooting

### "Access denied" or 403 error
- Restart Flask server
- Make sure you're accessing via http://localhost:5000 not file://

### "Failed to connect" in browser
- Check Flask is running: `ps aux | grep python`
- Check port 5000 is available: `lsof -i :5000`

### API calls not working
- Open browser DevTools → Network tab
- Check if requests are being made
- Verify Flask server shows incoming requests in terminal

## File Structure

```
backend/
├── app.py              # Flask server
├── templates/          # HTML pages
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   └── projects.html
└── static/
    └── js/
        └── api.js      # API client
```

## Next Steps

- Test bid submission on dashboard
- Test timeline chat on projects page
- Build admin dashboard (Phase 4)
- Create documentation (Phase 5)
