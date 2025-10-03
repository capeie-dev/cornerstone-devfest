"""
Cornerstone Flask Backend
Bridges frontend UI with ADK agents
Supports both direct tool calls AND SequentialAgent orchestration
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import agents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import agent tools directly
from demand_agent.agent import analyze_market_trends, get_product_recommendations, calculate_demand_forecast
from bid_coordinator_agent.agent import create_bid_window, get_bid_status, close_bid_window, notify_winners
from cornerstone_agent.agent import optimize_bids, get_job_details, list_manufacturers
from timeline_agent.agent import update_timeline, get_timeline_status, send_message_to_manufacturer
from logistics_agent.agent import plan_logistics, optimize_shipping_costs, track_shipments, coordinate_consolidation

# Import Master Orchestrator for sequential workflow
from master_orchestrator_agent.agent import root_agent as master_orchestrator
from google.adk.runners import Runner

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests


# ============================================================================
# FRONTEND ROUTES
# ============================================================================

@app.route('/')
def home():
    """Landing page"""
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    """Redirect old index.html links"""
    return render_template('index.html')

@app.route('/signup')
def signup():
    """Signup page"""
    return render_template('signup.html')

@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/projects')
def projects():
    """Projects page"""
    return render_template('projects.html')


# ============================================================================
# DEMAND ANALYSIS ENDPOINTS
# ============================================================================

@app.route('/api/analyze-demand', methods=['POST'])
def api_analyze_demand():
    """Analyze market trends for products"""
    data = request.json or {}
    category = data.get('category', '')
    
    result = analyze_market_trends(category)
    return jsonify(result)


@app.route('/api/recommendations', methods=['GET'])
def api_get_recommendations():
    """Get product recommendations"""
    min_score = float(request.args.get('min_score', 7.0))
    
    result = get_product_recommendations(min_score)
    return jsonify(result)


@app.route('/api/forecast', methods=['POST'])
def api_forecast():
    """Get demand forecast for a product"""
    data = request.json or {}
    product_id = data.get('product_id', 'PROD_001')
    timeframe = data.get('timeframe', '30_days')
    
    result = calculate_demand_forecast(product_id, timeframe)
    return jsonify(result)


# ============================================================================
# BID COORDINATION ENDPOINTS
# ============================================================================

@app.route('/api/create-bid', methods=['POST'])
def api_create_bid():
    """Create a new bid window"""
    data = request.json or {}
    
    result = create_bid_window(
        job_id=data.get('job_id'),
        product_name=data.get('product_name'),
        required_qty=data.get('required_qty'),
        required_skill=data.get('required_skill'),
        duration_hours=data.get('duration_hours', 96)
    )
    return jsonify(result)


@app.route('/api/bid-status/<job_id>', methods=['GET'])
def api_bid_status(job_id):
    """Get bid window status"""
    result = get_bid_status(job_id)
    return jsonify(result)


@app.route('/api/close-bid', methods=['POST'])
def api_close_bid():
    """Close a bid window"""
    data = request.json or {}
    job_id = data.get('job_id')
    
    result = close_bid_window(job_id)
    return jsonify(result)


@app.route('/api/notify-winners', methods=['POST'])
def api_notify_winners():
    """Notify winning manufacturers"""
    data = request.json or {}
    job_id = data.get('job_id')
    winning_maker_ids = data.get('winning_maker_ids')  # Comma-separated string
    
    result = notify_winners(job_id, winning_maker_ids)
    return jsonify(result)


# ============================================================================
# BID OPTIMIZATION ENDPOINTS
# ============================================================================

@app.route('/api/optimize-bids', methods=['POST'])
def api_optimize_bids():
    """Optimize bid selection"""
    data = request.json or {}
    
    result = optimize_bids(
        job_id=data.get('job_id', 'KNICK_2025'),
        required_qty=data.get('required_qty', 5000),
        required_skill=data.get('required_skill', 'CNC')
    )
    return jsonify(result)


@app.route('/api/job-details', methods=['GET'])
def api_job_details():
    """Get current job details"""
    result = get_job_details()
    return jsonify(result)


@app.route('/api/manufacturers', methods=['GET'])
def api_manufacturers():
    """List manufacturers"""
    skill = request.args.get('skill', '')
    
    result = list_manufacturers(skill)
    return jsonify(result)


# ============================================================================
# TIMELINE MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/update-timeline', methods=['POST'])
def api_update_timeline():
    """Update manufacturer timeline"""
    data = request.json or {}
    
    result = update_timeline(
        maker_id=data.get('maker_id'),
        new_completion_date=data.get('new_completion_date'),
        reason=data.get('reason', '')
    )
    return jsonify(result)


@app.route('/api/timeline-status', methods=['GET'])
def api_timeline_status():
    """Get timeline status"""
    maker_id = request.args.get('maker_id', '')
    
    result = get_timeline_status(maker_id)
    return jsonify(result)


@app.route('/api/send-message', methods=['POST'])
def api_send_message():
    """Send message to manufacturer"""
    data = request.json or {}
    
    result = send_message_to_manufacturer(
        maker_id=data.get('maker_id'),
        message=data.get('message')
    )
    return jsonify(result)


# ============================================================================
# LOGISTICS ENDPOINTS
# ============================================================================

@app.route('/api/plan-logistics', methods=['POST'])
def api_plan_logistics():
    """Plan logistics for a job"""
    data = request.json or {}
    
    result = plan_logistics(
        job_id=data.get('job_id'),
        winning_makers=data.get('winning_makers')  # Comma-separated
    )
    return jsonify(result)


@app.route('/api/optimize-shipping', methods=['POST'])
def api_optimize_shipping():
    """Optimize shipping costs"""
    data = request.json or {}
    job_id = data.get('job_id')
    
    result = optimize_shipping_costs(job_id)
    return jsonify(result)


@app.route('/api/track-shipments/<job_id>', methods=['GET'])
def api_track_shipments(job_id):
    """Track shipments for a job"""
    result = track_shipments(job_id)
    return jsonify(result)


@app.route('/api/coordinate-consolidation', methods=['POST'])
def api_coordinate_consolidation():
    """Coordinate consolidation"""
    data = request.json or {}
    job_id = data.get('job_id')
    
    result = coordinate_consolidation(job_id)
    return jsonify(result)


# ============================================================================
# ORCHESTRATED WORKFLOWS
# ============================================================================

@app.route('/api/complete-workflow-flask', methods=['POST'])
def api_complete_workflow_flask():
    """
    Execute complete manufacturing workflow using Flask orchestration:
    Demand → Bid → Optimize → Logistics
    (Flask calls each tool sequentially)
    """
    try:
        # Step 1: Analyze demand
        demand_result = analyze_market_trends('')
        if demand_result['status'] != 'success':
            return jsonify({'error': 'Demand analysis failed'}), 500
        
        top_product = demand_result['report']['trending_products'][0]
        
        # Step 2: Create bid window
        bid_result = create_bid_window(
            job_id=f"JOB_{top_product['product_id']}",
            product_name=top_product['name'],
            required_qty=top_product['estimated_volume'],
            required_skill='CNC',
            duration_hours=96
        )
        
        if bid_result['status'] != 'success':
            return jsonify({'error': 'Bid creation failed'}), 500
        
        job_id = bid_result['report']['job_id']
        
        # Step 3: Close bid (simulate)
        close_result = close_bid_window(job_id)
        
        # Step 4: Optimize bids
        optimize_result = optimize_bids(
            job_id=job_id,
            required_qty=top_product['estimated_volume'],
            required_skill='CNC'
        )
        
        if optimize_result['status'] != 'success':
            return jsonify({'error': 'Optimization failed'}), 500
        
        # Step 5: Plan logistics
        winning_makers = ','.join([m['maker_id'] for m in optimize_result['report']['winning_makers']])
        logistics_result = plan_logistics(job_id, winning_makers)
        
        # Compile complete workflow result
        workflow = {
            'status': 'success',
            'orchestration_method': 'flask',
            'workflow': {
                'step_1_demand': {
                    'product': top_product['name'],
                    'demand_score': top_product['demand_score'],
                    'estimated_volume': top_product['estimated_volume']
                },
                'step_2_bid': {
                    'job_id': job_id,
                    'status': 'CLOSED',
                    'total_bids': 8
                },
                'step_3_optimization': {
                    'total_cost': optimize_result['report']['total_cost'],
                    'manufacturers': len(optimize_result['report']['winning_makers']),
                    'lead_time': optimize_result['report']['total_lead_time_days']
                },
                'step_4_logistics': {
                    'consolidation_center': logistics_result['report']['consolidation_center'],
                    'shipping_cost': f"${logistics_result['report']['estimated_shipping_cost']:.2f}",
                    'delivery_date': logistics_result['report']['final_delivery_date']
                },
                'summary': f"Complete workflow executed via Flask: {top_product['name']} manufacturing planned. Total cost: {optimize_result['report']['total_cost']}, Delivery: {logistics_result['report']['final_delivery_date']}"
            }
        }
        
        return jsonify(workflow)
        
    except Exception as e:
        return jsonify({'status': 'error', 'error_message': str(e)}), 500


@app.route('/api/complete-workflow-adk', methods=['POST'])
def api_complete_workflow_adk():
    """
    Execute complete manufacturing workflow using ADK SequentialAgent:
    Demonstrates true multi-agent orchestration
    (Master Orchestrator calls all 5 agents sequentially)
    """
    try:
        # Use ADK Runner to execute SequentialAgent
        runner = Runner(master_orchestrator)
        
        # Execute the workflow
        result = runner.run("Execute the complete manufacturing workflow for the top trending product")
        
        return jsonify({
            'status': 'success',
            'orchestration_method': 'adk_sequential_agent',
            'result': result.output,
            'summary': 'Workflow executed via ADK SequentialAgent - all 5 agents orchestrated autonomously'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'error_message': str(e)}), 500


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agents': {
            'demand_agent': 'active',
            'bid_coordinator': 'active',
            'cornerstone_optimizer': 'active',
            'timeline_manager': 'active',
            'logistics_coordinator': 'active',
            'master_orchestrator': 'active'
        },
        'total_agents': 6,
        'total_tools': 17
    })


@app.route('/api/info', methods=['GET'])
def api_info():
    """API documentation"""
    return jsonify({
        'name': 'Cornerstone API',
        'version': '1.0.0',
        'description': 'Backend API for Cornerstone manufacturing network',
        'endpoints': {
            'demand': ['/api/analyze-demand', '/api/recommendations', '/api/forecast'],
            'bidding': ['/api/create-bid', '/api/bid-status/<job_id>', '/api/close-bid', '/api/notify-winners'],
            'optimization': ['/api/optimize-bids', '/api/job-details', '/api/manufacturers'],
            'timeline': ['/api/update-timeline', '/api/timeline-status', '/api/send-message'],
            'logistics': ['/api/plan-logistics', '/api/optimize-shipping', '/api/track-shipments/<job_id>', '/api/coordinate-consolidation'],
            'workflows': ['/api/complete-workflow-flask', '/api/complete-workflow-adk']
        },
        'documentation': 'See README.md for usage examples'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("CORNERSTONE BACKEND API SERVER")
    print("=" * 60)
    print("Frontend: http://localhost:5001")
    print("Dashboard: http://localhost:5001/dashboard")
    print("Projects: http://localhost:5001/projects")
    print("API Info: http://localhost:5001/api/info")
    print("Health Check: http://localhost:5001/api/health")
    print("=" * 60)
    app.run(debug=True, port=5001)
