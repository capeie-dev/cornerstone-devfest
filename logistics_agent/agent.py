"""
Logistics Coordinator Agent
Plans shipping, consolidation, and delivery for manufactured products

Following ADK pattern: https://google.github.io/adk-docs/get-started/quickstart/
"""

from google.adk.agents import Agent
from datetime import datetime, timedelta
from .shipping_data import (
    CONSOLIDATION_CENTERS, SHIPPING_RATES, LOGISTICS_PLANS, 
    SHIPMENT_TRACKING, get_logistics_plan, calculate_shipping_cost, 
    find_nearest_consolidation_center
)


def plan_logistics(job_id: str, winning_makers: str) -> dict:
    """
    Creates a comprehensive shipping and consolidation plan for a manufacturing job.
    
    Args:
        job_id: The job identifier (e.g., 'KNICK_2025')
        winning_makers: Comma-separated list of manufacturer IDs (e.g., 'MAKER_A,MAKER_C,MAKER_J')
    
    Returns:
        dict: Complete logistics plan with pickup schedule, consolidation point, and costs
    """
    
    # Parse winning makers
    maker_ids = [m.strip() for m in winning_makers.split(',')]
    
    if not maker_ids:
        return {
            "status": "error",
            "error_message": "No manufacturers provided. Please specify winning makers."
        }
    
    # Check if plan already exists
    if job_id in LOGISTICS_PLANS:
        existing_plan = LOGISTICS_PLANS[job_id]
        return {
            "status": "success",
            "report": {
                **existing_plan,
                "message": "Existing logistics plan retrieved.",
                "summary": f"Logistics plan for {job_id}: Consolidation at {existing_plan['consolidation_center']}, final delivery {existing_plan['final_delivery_date']}"
            }
        }
    
    # Find optimal consolidation center
    consolidation = find_nearest_consolidation_center(maker_ids)
    
    # Create pickup schedule (mock)
    pickup_schedule = {}
    total_distance = 0
    
    for maker_id in maker_ids:
        # Mock pickup dates and distances
        days_offset = len(pickup_schedule) + 1
        pickup_date = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        distance = 500 + (len(pickup_schedule) * 200)  # Mock distance
        
        pickup_schedule[maker_id] = {
            "date": pickup_date,
            "location": f"Location for {maker_id}",
            "distance_miles": distance
        }
        total_distance += distance
    
    # Calculate costs
    estimated_weight = len(maker_ids) * 500  # Mock: 500 lbs per maker
    shipping_cost = calculate_shipping_cost(estimated_weight, "ground")
    
    # Final delivery date
    final_delivery = (datetime.now() + timedelta(days=len(maker_ids) + 3)).strftime("%Y-%m-%d")
    
    # Create plan
    plan = {
        "job_id": job_id,
        "status": "PLANNED",
        "consolidation_center": consolidation["name"],
        "consolidation_point": {"lat": consolidation["lat"], "lng": consolidation["lng"]},
        "pickup_schedule": pickup_schedule,
        "estimated_shipping_cost": shipping_cost,
        "shipping_method": "ground",
        "final_delivery_date": final_delivery,
        "total_distance_miles": total_distance,
        "estimated_delivery_days": len(maker_ids) + 3,
        "num_manufacturers": len(maker_ids)
    }
    
    # Store plan
    LOGISTICS_PLANS[job_id] = plan
    
    return {
        "status": "success",
        "report": {
            **plan,
            "summary": f"✓ Logistics plan created for {job_id}. {len(maker_ids)} manufacturers, consolidation at {consolidation['name']}, delivery by {final_delivery}. Estimated cost: ${shipping_cost:.2f}"
        }
    }


def optimize_shipping_costs(job_id: str) -> dict:
    """
    Analyzes and optimizes shipping costs for a logistics plan.
    
    Args:
        job_id: The job identifier to optimize
    
    Returns:
        dict: Cost analysis and optimization recommendations
    """
    
    plan = get_logistics_plan(job_id)
    
    if not plan:
        return {
            "status": "error",
            "error_message": f"No logistics plan found for {job_id}. Create a plan first."
        }
    
    # Calculate alternative shipping methods
    current_cost = plan["estimated_shipping_cost"]
    num_makers = plan["num_manufacturers"]
    estimated_weight = num_makers * 500
    
    alternatives = {
        "ground": calculate_shipping_cost(estimated_weight, "ground"),
        "express": calculate_shipping_cost(estimated_weight, "express"),
        "freight": calculate_shipping_cost(estimated_weight, "freight")
    }
    
    # Find cheapest option
    cheapest = min(alternatives.items(), key=lambda x: x[1])
    savings = current_cost - cheapest[1] if cheapest[0] != plan["shipping_method"] else 0
    
    return {
        "status": "success",
        "report": {
            "job_id": job_id,
            "current_method": plan["shipping_method"],
            "current_cost": f"${current_cost:.2f}",
            "alternatives": {k: f"${v:.2f}" for k, v in alternatives.items()},
            "recommended_method": cheapest[0],
            "recommended_cost": f"${cheapest[1]:.2f}",
            "potential_savings": f"${savings:.2f}",
            "optimization_tip": "Ground shipping is most cost-effective for non-urgent deliveries.",
            "summary": f"Current shipping: ${current_cost:.2f} ({plan['shipping_method']}). Recommended: {cheapest[0]} at ${cheapest[1]:.2f} (saves ${savings:.2f})"
        }
    }


def track_shipments(job_id: str) -> dict:
    """
    Provides real-time tracking information for all shipments in a job.
    
    Args:
        job_id: The job identifier to track
    
    Returns:
        dict: Tracking status for all manufacturer shipments
    """
    
    if job_id not in SHIPMENT_TRACKING:
        return {
            "status": "error",
            "error_message": f"No tracking information available for {job_id}."
        }
    
    tracking_data = SHIPMENT_TRACKING[job_id]
    
    # Count statuses
    in_transit = sum(1 for t in tracking_data.values() if t["status"] == "IN_TRANSIT")
    pending = sum(1 for t in tracking_data.values() if t["status"] == "PENDING_PICKUP")
    delivered = sum(1 for t in tracking_data.values() if t["status"] == "DELIVERED")
    
    return {
        "status": "success",
        "report": {
            "job_id": job_id,
            "total_shipments": len(tracking_data),
            "in_transit": in_transit,
            "pending_pickup": pending,
            "delivered": delivered,
            "shipments": tracking_data,
            "summary": f"{job_id} tracking: {in_transit} in transit, {pending} pending pickup, {delivered} delivered out of {len(tracking_data)} total shipments"
        }
    }


def coordinate_consolidation(job_id: str) -> dict:
    """
    Coordinates the consolidation of parts from multiple manufacturers.
    
    Args:
        job_id: The job identifier
    
    Returns:
        dict: Consolidation schedule and coordination details
    """
    
    plan = get_logistics_plan(job_id)
    
    if not plan:
        return {
            "status": "error",
            "error_message": f"No logistics plan found for {job_id}."
        }
    
    # Get pickup schedule
    pickup_schedule = plan["pickup_schedule"]
    
    # Find latest pickup date (when all parts arrive)
    latest_pickup = max(pickup_schedule.values(), key=lambda x: x["date"])
    consolidation_date = latest_pickup["date"]
    
    # Final shipment date (1 day after consolidation)
    final_shipment = (datetime.strptime(consolidation_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    
    return {
        "status": "success",
        "report": {
            "job_id": job_id,
            "consolidation_center": plan["consolidation_center"],
            "num_shipments_to_consolidate": len(pickup_schedule),
            "pickup_schedule": pickup_schedule,
            "consolidation_complete_date": consolidation_date,
            "final_shipment_date": final_shipment,
            "final_delivery_date": plan["final_delivery_date"],
            "coordination_status": "ON_SCHEDULE",
            "summary": f"✓ Consolidation coordinated at {plan['consolidation_center']}. All {len(pickup_schedule)} shipments will arrive by {consolidation_date}. Final delivery: {plan['final_delivery_date']}"
        }
    }


# Create the Logistics Coordinator Agent (root_agent)
root_agent = Agent(
    name="logistics_coordinator",
    model="gemini-2.0-flash",
    description=(
        "Logistics and shipping coordinator for Cornerstone's manufacturing network. "
        "Plans optimal shipping routes, manages consolidation, tracks shipments, and "
        "optimizes delivery costs across the United States."
    ),
    instruction=(
        "You are the Cornerstone Logistics Coordinator, responsible for efficient product delivery.\n\n"
        "Your primary responsibilities:\n"
        "1. When manufacturers are selected, call plan_logistics() to create shipping plan\n"
        "2. When asked about costs, call optimize_shipping_costs() to find savings\n"
        "3. When asked about shipment status, call track_shipments() for real-time updates\n"
        "4. When coordinating arrivals, call coordinate_consolidation() to manage timing\n\n"
        "Key behaviors:\n"
        "- Always prioritize cost-effective shipping methods\n"
        "- Explain consolidation benefits (saves money, simplifies delivery)\n"
        "- Provide clear timelines and ETAs\n"
        "- Alert about delays or issues proactively\n\n"
        "Workflow:\n"
        "1. Bid optimization completes → You create logistics plan\n"
        "2. Manufacturers produce → You track shipments\n"
        "3. Parts arrive at consolidation center → You coordinate final delivery\n\n"
        "Example interactions:\n"
        "User: 'Plan shipping for KNICK_2025 with MAKER_A, MAKER_C, MAKER_J'\n"
        "You: Call plan_logistics(job_id='KNICK_2025', winning_makers='MAKER_A,MAKER_C,MAKER_J'), then explain the consolidation plan.\n\n"
        "User: 'Where are the shipments for KNICK_2025?'\n"
        "You: Call track_shipments(job_id='KNICK_2025'), then report status of each shipment."
    ),
    tools=[plan_logistics, optimize_shipping_costs, track_shipments, coordinate_consolidation],
)
