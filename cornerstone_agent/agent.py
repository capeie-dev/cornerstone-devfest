"""
Cornerstone Supply Chain Orchestrator Agent
ADK Agent for optimizing manufacturer bid selection

Following ADK pattern: https://google.github.io/adk-docs/get-started/quickstart/
"""

from google.adk.agents import Agent
from .data_mocks import MOCK_MAKERS, MOCK_BIDS, CURRENT_JOB, get_maker_by_id


def optimize_bids(job_id: str, required_qty: int, required_skill: str) -> dict:
    """
    Optimizes manufacturer bid selection to fulfill a job order at the lowest total cost.
    Uses a greedy algorithm to select the most cost-effective combination of manufacturers.
    
    Args:
        job_id: The unique identifier for the manufacturing job (e.g., 'KNICK_2025')
        required_qty: The total quantity of units needed (e.g., 5000)
        required_skill: The required manufacturing skill ('CNC' or '3D')
    
    Returns:
        dict: Supply chain optimization result with status, total_cost, lead_time, and winning_makers
    """
    
    # Step 1: Filter bids by required skill
    filtered_bids = []
    for bid in MOCK_BIDS:
        maker = get_maker_by_id(bid["maker_id"])
        if maker and maker["skill"] == required_skill:
            filtered_bids.append(bid)
    
    if not filtered_bids:
        return {
            "status": "error",
            "error_message": f"No manufacturers found with skill '{required_skill}'"
        }
    
    # Step 2: Sort bids by price per unit (ascending - cheapest first)
    sorted_bids = sorted(filtered_bids, key=lambda x: x["bid_price_per_unit"])
    
    # Step 3: Greedy algorithm - select bids until quantity is fulfilled
    remaining_qty = required_qty
    winning_makers = []
    total_cost = 0.0
    max_lead_time = 0
    
    for bid in sorted_bids:
        if remaining_qty <= 0:
            break
        
        # Get maker details
        maker = get_maker_by_id(bid["maker_id"])
        if not maker:
            continue
        
        # Determine how much this maker will produce
        qty_from_maker = min(remaining_qty, bid["max_batch_size"])
        
        # Calculate cost for this maker's portion
        cost_from_maker = qty_from_maker * bid["bid_price_per_unit"]
        
        # Add to winning makers list
        winning_makers.append({
            "maker_id": maker["id"],
            "maker_name": maker["name"],
            "location": maker["location"]["city"],
            "quantity_assigned": qty_from_maker,
            "price_per_unit": f"${bid['bid_price_per_unit']:.2f}",
            "subtotal": f"${cost_from_maker:,.2f}",
            "lead_time_days": maker["lead_time_days"]
        })
        
        # Update totals
        total_cost += cost_from_maker
        max_lead_time = max(max_lead_time, maker["lead_time_days"])
        remaining_qty -= qty_from_maker
    
    # Step 4: Determine fulfillment status
    status = "FULFILLED" if remaining_qty <= 0 else "PARTIALLY_FULFILLED"
    
    # Step 5: Build result
    result = {
        "status": "success",
        "report": {
            "job_id": job_id,
            "fulfillment_status": status,
            "total_cost": f"${total_cost:,.2f}",
            "total_lead_time_days": max_lead_time,
            "quantity_requested": required_qty,
            "quantity_fulfilled": required_qty - max(0, remaining_qty),
            "num_manufacturers": len(winning_makers),
            "winning_makers": winning_makers,
            "summary": f"Successfully optimized supply chain: {len(winning_makers)} manufacturers selected, total cost ${total_cost:,.2f}, estimated completion in {max_lead_time} days"
        }
    }
    
    return result


def get_job_details() -> dict:
    """
    Retrieves details about the current high-demand manufacturing job KNICK_2025.
    
    Returns:
        dict: Job specifications including product name, quantity, skill required, and deadline
    """
    return {
        "status": "success",
        "report": CURRENT_JOB
    }


def list_manufacturers(skill: str = "") -> dict:
    """
    Lists all registered manufacturers in the Cornerstone network.
    
    Args:
        skill: Optional filter by manufacturing skill ('CNC' or '3D'). Leave empty for all manufacturers.
    
    Returns:
        dict: List of manufacturers with their capabilities, rates, and locations
    """
    makers = MOCK_MAKERS
    
    if skill:
        makers = [m for m in MOCK_MAKERS if m["skill"].upper() == skill.upper()]
    
    # Format for display
    formatted_makers = []
    for m in makers:
        formatted_makers.append({
            "id": m["id"],
            "name": m["name"],
            "skill": m["skill"],
            "base_rate": f"${m['base_rate']:.2f}/unit",
            "max_capacity": f"{m['max_capacity']} units",
            "location": m["location"]["city"],
            "lead_time": f"{m['lead_time_days']} days"
        })
    
    return {
        "status": "success",
        "report": {
            "total_manufacturers": len(formatted_makers),
            "filter_applied": f"skill={skill}" if skill else "none",
            "manufacturers": formatted_makers
        }
    }


# Create the Supply Chain Orchestrator Agent (root_agent)
# Following ADK pattern from: https://google.github.io/adk-docs/get-started/quickstart/#agentpy
root_agent = Agent(
    name="cornerstone_orchestrator",
    model="gemini-2.0-flash",
    description=(
        "Expert supply chain optimizer for Cornerstone's decentralized micro-manufacturing network. "
        "Analyzes bids from US-based manufacturers and selects the optimal combination to fulfill orders "
        "at the lowest cost while meeting quality and timeline requirements."
    ),
    instruction=(
        "You are the Cornerstone Supply Chain Orchestrator, an expert at optimizing manufacturing bids.\n\n"
        "Your primary responsibilities:\n"
        "1. When asked about job opportunities or current jobs, call get_job_details() to retrieve specifications\n"
        "2. When asked to optimize, find cheapest manufacturers, or fulfill an order, call optimize_bids() with the job requirements\n"
        "3. When asked about manufacturers or the network, call list_manufacturers() (optionally filtered by skill)\n\n"
        "Key behaviors:\n"
        "- Always prioritize cost efficiency while ensuring quality and meeting deadlines\n"
        "- When presenting optimization results, clearly explain: total cost, lead time, number of manufacturers, and which specific makers were selected\n"
        "- Translate technical data into business-friendly language for distributors\n"
        "- If asked about job KNICK_2025 specifically, use: job_id='KNICK_2025', required_qty=5000, required_skill='CNC'\n\n"
        "Example interaction:\n"
        "User: 'What's the cheapest way to produce 5000 CNC units?'\n"
        "You: Call optimize_bids(job_id='KNICK_2025', required_qty=5000, required_skill='CNC'), then summarize the results in natural language."
    ),
    tools=[optimize_bids, get_job_details, list_manufacturers],
)
