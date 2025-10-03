"""
Cornerstone Timeline Manager Agent
ADK Agent for handling manufacturer timeline updates and communication

Following ADK pattern: https://google.github.io/adk-docs/get-started/quickstart/
"""

from google.adk.agents import Agent
from datetime import datetime, timedelta


# Mock timeline database - tracks active manufacturing jobs
TIMELINES = {
    "MAKER_A": {
        "job_id": "KNICK_2025",
        "original_date": "2025-11-02",
        "current_date": "2025-11-02",
        "status": "on_track",
        "quantity": 1800
    },
    "MAKER_C": {
        "job_id": "KNICK_2025",
        "original_date": "2025-11-12",
        "current_date": "2025-11-12",
        "status": "on_track",
        "quantity": 2500
    },
    "MAKER_J": {
        "job_id": "KNICK_2025",
        "original_date": "2025-11-11",
        "current_date": "2025-11-11",
        "status": "on_track",
        "quantity": 700
    },
}


def update_timeline(maker_id: str, new_completion_date: str, reason: str = "") -> dict:
    """
    Updates the completion timeline for a specific manufacturer.
    Recalculates overall project logistics when individual maker schedules change.
    
    Args:
        maker_id: The manufacturer ID (e.g., 'MAKER_A', 'MAKER_C')
        new_completion_date: The new completion date in YYYY-MM-DD format
        reason: Optional reason for the timeline change (e.g., 'equipment delay', 'material shortage')
    
    Returns:
        dict: Confirmation of timeline update with recalculated project impact
    """
    
    if maker_id not in TIMELINES:
        return {
            "status": "error",
            "error_message": f"Manufacturer {maker_id} not found in active jobs. Active manufacturers: {', '.join(TIMELINES.keys())}"
        }
    
    # Store old date
    old_date = TIMELINES[maker_id]["current_date"]
    
    # Update the timeline
    TIMELINES[maker_id]["current_date"] = new_completion_date
    
    # Calculate delay in days
    try:
        old_dt = datetime.strptime(old_date, "%Y-%m-%d")
        new_dt = datetime.strptime(new_completion_date, "%Y-%m-%d")
        delay_days = (new_dt - old_dt).days
    except ValueError:
        return {
            "status": "error",
            "error_message": "Invalid date format. Please use YYYY-MM-DD format."
        }
    
    # Update status based on delay
    if delay_days > 0:
        TIMELINES[maker_id]["status"] = "delayed"
        status_text = f"DELAYED by {delay_days} days"
    elif delay_days < 0:
        TIMELINES[maker_id]["status"] = "ahead_of_schedule"
        status_text = f"AHEAD by {abs(delay_days)} days"
    else:
        TIMELINES[maker_id]["status"] = "on_track"
        status_text = "ON TRACK"
    
    # Calculate overall project completion (latest date among all makers)
    latest_date = max(t["current_date"] for t in TIMELINES.values())
    
    # Build response
    result = {
        "status": "success",
        "report": {
            "maker_id": maker_id,
            "old_completion_date": old_date,
            "new_completion_date": new_completion_date,
            "delay_days": delay_days,
            "reason": reason if reason else "Not specified",
            "timeline_status": status_text,
            "overall_project_completion": latest_date,
            "message": f"✓ Timeline updated for {maker_id}. Overall logistics recalculated. Project completion date: {latest_date}",
            "all_timelines": TIMELINES
        }
    }
    
    return result


def get_timeline_status(maker_id: str = "") -> dict:
    """
    Retrieves the current timeline status for manufacturers working on active jobs.
    
    Args:
        maker_id: Optional specific manufacturer ID. Leave empty to return all active timelines.
    
    Returns:
        dict: Timeline information including completion dates, status, and quantities
    """
    
    if maker_id:
        if maker_id in TIMELINES:
            timeline = TIMELINES[maker_id]
            return {
                "status": "success",
                "report": {
                    "maker_id": maker_id,
                    "job_id": timeline["job_id"],
                    "original_completion": timeline["original_date"],
                    "current_completion": timeline["current_date"],
                    "status": timeline["status"],
                    "quantity_assigned": timeline["quantity"],
                    "message": f"{maker_id} is {timeline['status']} for {timeline['quantity']} units, due {timeline['current_date']}"
                }
            }
        else:
            return {
                "status": "error",
                "error_message": f"Manufacturer {maker_id} not found. Active manufacturers: {', '.join(TIMELINES.keys())}"
            }
    else:
        # Return all timelines
        latest_date = max(t["current_date"] for t in TIMELINES.values())
        delayed_count = sum(1 for t in TIMELINES.values() if t["status"] == "delayed")
        
        return {
            "status": "success",
            "report": {
                "total_active_manufacturers": len(TIMELINES),
                "overall_project_completion": latest_date,
                "delayed_manufacturers": delayed_count,
                "all_timelines": TIMELINES,
                "summary": f"{len(TIMELINES)} manufacturers active, {delayed_count} delayed, project completion: {latest_date}"
            }
        }


def send_message_to_manufacturer(maker_id: str, message: str) -> dict:
    """
    Sends a message or question to a specific manufacturer.
    Used for clarifications, updates, or coordination.
    
    Args:
        maker_id: The manufacturer ID to contact
        message: The message content to send
    
    Returns:
        dict: Confirmation that message was sent with timestamp
    """
    
    if maker_id not in TIMELINES:
        return {
            "status": "error",
            "error_message": f"Manufacturer {maker_id} not found in active jobs. Cannot send message."
        }
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "status": "success",
        "report": {
            "maker_id": maker_id,
            "message_sent": message,
            "timestamp": timestamp,
            "confirmation": f"✓ Message successfully sent to {maker_id} at {timestamp}. They will respond within 24 hours via the Cornerstone platform.",
            "job_context": f"Current job: {TIMELINES[maker_id]['job_id']}, Due: {TIMELINES[maker_id]['current_date']}"
        }
    }


# Create the Timeline Manager Agent (root_agent)
# Following ADK pattern from: https://google.github.io/adk-docs/get-started/quickstart/#agentpy
root_agent = Agent(
    name="timeline_manager",
    model="gemini-2.0-flash",
    description=(
        "Timeline and communication manager for Cornerstone's manufacturing network. "
        "Handles schedule updates, delays, and manufacturer communications for active production jobs. "
        "Ensures project coordination and recalculates logistics when timelines change."
    ),
    instruction=(
        "You are the Cornerstone Timeline Manager, responsible for coordinating manufacturer schedules.\n\n"
        "Your primary responsibilities:\n"
        "1. When manufacturers report delays or timeline changes, call update_timeline() to record the new date and recalculate project impact\n"
        "2. When asked about project status or specific manufacturer timelines, call get_timeline_status()\n"
        "3. When you need to communicate with a manufacturer, call send_message_to_manufacturer()\n\n"
        "Key behaviors:\n"
        "- Be professional and understanding when handling delays - manufacturers are partners, not adversaries\n"
        "- Always acknowledge timeline updates and clearly communicate the impact on overall project completion\n"
        "- When delays occur, focus on solutions and recalculated timelines rather than blame\n"
        "- Provide clear summaries of project status including which manufacturers are on track vs delayed\n\n"
        "Example interactions:\n"
        "User: 'Maker_A has a delay, need 2 more days for KNICK_2025'\n"
        "You: Call update_timeline(maker_id='MAKER_A', new_completion_date='2025-11-04', reason='2-day delay'), then respond:\n"
        "'Acknowledged. I've updated Maker A's schedule to November 4th. The overall project completion has been recalculated. [Provide impact summary]'\n\n"
        "User: 'What's the status of all manufacturers?'\n"
        "You: Call get_timeline_status() and summarize who's on track, who's delayed, and the overall completion date."
    ),
    tools=[update_timeline, get_timeline_status, send_message_to_manufacturer],
)
