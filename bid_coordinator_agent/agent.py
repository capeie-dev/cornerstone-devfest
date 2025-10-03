"""
Bid Coordinator Agent
Manages bid lifecycle from opening to closing and winner notification

Following ADK pattern: https://google.github.io/adk-docs/get-started/quickstart/
"""

from google.adk.agents import Agent
from datetime import datetime, timedelta
from .bid_windows import BID_WINDOWS, NOTIFICATIONS, get_bid_window, calculate_time_remaining


def create_bid_window(job_id: str, product_name: str, required_qty: int, required_skill: str, duration_hours: int = 96) -> dict:
    """
    Creates and opens a new bid window for manufacturers to submit bids.
    
    Args:
        job_id: Unique job identifier (e.g., 'KNICK_2025')
        product_name: Name of the product to manufacture
        required_qty: Total quantity needed
        required_skill: Required manufacturing skill ('CNC', '3D', etc.)
        duration_hours: How long the bid window stays open (default 96 hours / 4 days)
    
    Returns:
        dict: Bid window details and notification confirmation
    """
    
    # Check if bid window already exists
    if job_id in BID_WINDOWS:
        existing = BID_WINDOWS[job_id]
        return {
            "status": "error",
            "error_message": f"Bid window for {job_id} already exists with status: {existing['status']}"
        }
    
    # Create timestamps
    opened_at = datetime.now()
    closes_at = opened_at + timedelta(hours=duration_hours)
    
    # Create new bid window
    new_window = {
        "job_id": job_id,
        "product_name": product_name,
        "status": "OPEN",
        "opened_at": opened_at.strftime("%Y-%m-%d %H:%M:%S"),
        "closes_at": closes_at.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_hours": duration_hours,
        "required_qty": required_qty,
        "required_skill": required_skill,
        "total_bids": 0,
        "participating_manufacturers": [],
        "participation_rate": "0%"
    }
    
    # Store in database (mock)
    BID_WINDOWS[job_id] = new_window
    
    # Prepare notification
    notification = NOTIFICATIONS["bid_opened"]["message"].format(
        job_id=job_id,
        product_name=product_name,
        required_qty=required_qty,
        required_skill=required_skill,
        closes_at=closes_at.strftime("%B %d, %Y at %I:%M %p")
    )
    
    return {
        "status": "success",
        "report": {
            "job_id": job_id,
            "bid_window_status": "OPEN",
            "opened_at": new_window["opened_at"],
            "closes_at": new_window["closes_at"],
            "duration": f"{duration_hours} hours ({duration_hours/24:.1f} days)",
            "manufacturers_notified": 10,
            "notification_sent": notification,
            "summary": f"✓ Bid window opened for {job_id}. {10} manufacturers notified. Window closes {closes_at.strftime('%B %d at %I:%M %p')}."
        }
    }


def get_bid_status(job_id: str) -> dict:
    """
    Retrieves current status of a bid window including participation and competition stats.
    
    Args:
        job_id: The job identifier to check
    
    Returns:
        dict: Bid window status, participation stats, and time remaining
    """
    
    window = get_bid_window(job_id)
    
    if not window:
        return {
            "status": "error",
            "error_message": f"Bid window {job_id} not found."
        }
    
    # Calculate time remaining if still open
    time_remaining = None
    if window["status"] == "OPEN":
        hours_left = calculate_time_remaining(window["closes_at"])
        time_remaining = f"{hours_left:.1f} hours"
    
    return {
        "status": "success",
        "report": {
            "job_id": job_id,
            "product_name": window["product_name"],
            "window_status": window["status"],
            "opened_at": window["opened_at"],
            "closes_at": window["closes_at"],
            "time_remaining": time_remaining,
            "total_bids_received": window["total_bids"],
            "participating_manufacturers": window.get("participating_manufacturers", []),
            "participation_rate": window.get("participation_rate", "0%"),
            "competition_stats": {
                "lowest_bid": f"${window.get('lowest_bid', 0):.2f}" if "lowest_bid" in window else "N/A",
                "highest_bid": f"${window.get('highest_bid', 0):.2f}" if "highest_bid" in window else "N/A",
                "average_bid": f"${window.get('average_bid', 0):.2f}" if "average_bid" in window else "N/A"
            },
            "summary": f"{job_id} is {window['status']}. {window['total_bids']} bids received from {window.get('participation_rate', '0%')} of manufacturers."
        }
    }


def close_bid_window(job_id: str) -> dict:
    """
    Closes a bid window and prepares for optimization.
    
    Args:
        job_id: The job identifier to close
    
    Returns:
        dict: Confirmation of closure and next steps
    """
    
    window = get_bid_window(job_id)
    
    if not window:
        return {
            "status": "error",
            "error_message": f"Bid window {job_id} not found."
        }
    
    if window["status"] == "CLOSED":
        return {
            "status": "error",
            "error_message": f"Bid window {job_id} is already closed."
        }
    
    # Close the window
    closed_at = datetime.now()
    window["status"] = "CLOSED"
    window["closed_at"] = closed_at.strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "status": "success",
        "report": {
            "job_id": job_id,
            "window_status": "CLOSED",
            "closed_at": window["closed_at"],
            "total_bids_received": window["total_bids"],
            "next_step": "BID_OPTIMIZATION",
            "message": f"✓ Bid window closed for {job_id}. {window['total_bids']} bids received. Ready for optimization by Cornerstone Orchestrator.",
            "summary": f"Bid window {job_id} successfully closed with {window['total_bids']} submissions. Proceeding to bid optimization."
        }
    }


def notify_winners(job_id: str, winning_maker_ids: str) -> dict:
    """
    Sends notifications to winning manufacturers.
    
    Args:
        job_id: The job identifier
        winning_maker_ids: Comma-separated list of winning manufacturer IDs (e.g., 'MAKER_A,MAKER_C,MAKER_J')
    
    Returns:
        dict: Confirmation of notifications sent
    """
    
    window = get_bid_window(job_id)
    
    if not window:
        return {
            "status": "error",
            "error_message": f"Bid window {job_id} not found."
        }
    
    # Parse maker IDs
    maker_ids = [m.strip() for m in winning_maker_ids.split(',')]
    
    notifications_sent = []
    
    for maker_id in maker_ids:
        notification = NOTIFICATIONS["winner_notification"]["message"].format(
            job_id=job_id,
            quantity="TBD",
            price="TBD",
            total="TBD",
            deadline="30 days"
        )
        
        notifications_sent.append({
            "maker_id": maker_id,
            "notification": notification,
            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Update window with winners
    window["winning_manufacturers"] = maker_ids
    
    return {
        "status": "success",
        "report": {
            "job_id": job_id,
            "winners_notified": len(notifications_sent),
            "notifications": notifications_sent,
            "summary": f"✓ {len(notifications_sent)} winning manufacturers notified for {job_id}. Production can begin."
        }
    }


# Create the Bid Coordinator Agent (root_agent)
root_agent = Agent(
    name="bid_coordinator",
    model="gemini-2.0-flash",
    description=(
        "Bid lifecycle manager for Cornerstone's manufacturing network. "
        "Opens bid windows, tracks participation, closes bids, and notifies winners. "
        "Coordinates the transition from bidding to production."
    ),
    instruction=(
        "You are the Cornerstone Bid Coordinator, responsible for managing the entire bid process.\n\n"
        "Your primary responsibilities:\n"
        "1. When asked to create or open a bid, call create_bid_window() with job details\n"
        "2. When asked about bid status or participation, call get_bid_status() for current stats\n"
        "3. When it's time to close bidding, call close_bid_window() to seal bids\n"
        "4. After optimization is complete, call notify_winners() to inform selected manufacturers\n\n"
        "Key behaviors:\n"
        "- Always confirm when bid windows are opened/closed\n"
        "- Report participation rates and competition stats\n"
        "- Explain the next steps after each action\n"
        "- Be encouraging to manufacturers about future opportunities\n\n"
        "Workflow:\n"
        "1. Demand Analyzer identifies product → You open bid window\n"
        "2. Manufacturers submit bids → You track participation\n"
        "3. Window closes → You trigger Cornerstone Orchestrator for optimization\n"
        "4. Winners selected → You notify manufacturers\n\n"
        "Example interactions:\n"
        "User: 'Open a bid for Widget Bracket, 5000 units, CNC skill'\n"
        "You: Call create_bid_window(job_id='KNICK_2025', product_name='Widget Bracket', required_qty=5000, required_skill='CNC'), then confirm opening.\n\n"
        "User: 'How many bids do we have for KNICK_2025?'\n"
        "You: Call get_bid_status(job_id='KNICK_2025'), then report participation stats."
    ),
    tools=[create_bid_window, get_bid_status, close_bid_window, notify_winners],
)
