"""
Logistics Coordinator Mock Data
Shipping plans, consolidation centers, and tracking
"""

# Consolidation Centers across US
CONSOLIDATION_CENTERS = [
    {"id": "CDC_CHI", "name": "Chicago Distribution Center", "location": "Chicago, IL", "lat": 41.8781, "lng": -87.6298},
    {"id": "CDC_ATL", "name": "Atlanta Logistics Hub", "location": "Atlanta, GA", "lat": 33.7490, "lng": -84.3880},
    {"id": "CDC_DAL", "name": "Dallas Freight Center", "location": "Dallas, TX", "lat": 32.7767, "lng": -96.7970},
    {"id": "CDC_LA", "name": "Los Angeles Port Hub", "location": "Los Angeles, CA", "lat": 34.0522, "lng": -118.2437}
]

# Shipping Rates (per 100 lbs)
SHIPPING_RATES = {
    "ground": 45.00,
    "express": 85.00,
    "freight": 120.00
}

# Active Logistics Plans
LOGISTICS_PLANS = {
    "KNICK_2025": {
        "job_id": "KNICK_2025",
        "status": "PLANNED",
        "consolidation_center": "Chicago Distribution Center",
        "consolidation_point": {"lat": 41.8781, "lng": -87.6298},
        "pickup_schedule": {
            "MAKER_C": {"date": "2025-11-12", "location": "Houston, TX", "distance_miles": 1080},
            "MAKER_J": {"date": "2025-11-11", "location": "Atlanta, GA", "distance_miles": 715},
            "MAKER_A": {"date": "2025-11-02", "location": "Columbus, OH", "distance_miles": 355}
        },
        "estimated_shipping_cost": 450.00,
        "shipping_method": "ground",
        "final_delivery_date": "2025-11-15",
        "total_distance_miles": 2150,
        "estimated_delivery_days": 3
    }
}

# Shipment Tracking (mock)
SHIPMENT_TRACKING = {
    "KNICK_2025": {
        "MAKER_A": {
            "status": "IN_TRANSIT",
            "current_location": "Indianapolis, IN",
            "last_update": "2025-11-03 14:30:00",
            "eta": "2025-11-04 10:00:00"
        },
        "MAKER_C": {
            "status": "PENDING_PICKUP",
            "current_location": "Houston, TX",
            "scheduled_pickup": "2025-11-12 09:00:00"
        },
        "MAKER_J": {
            "status": "PENDING_PICKUP",
            "current_location": "Atlanta, GA",
            "scheduled_pickup": "2025-11-11 08:00:00"
        }
    }
}

def get_logistics_plan(job_id):
    """Helper to retrieve logistics plan by job_id"""
    return LOGISTICS_PLANS.get(job_id)

def calculate_shipping_cost(total_weight_lbs, method="ground"):
    """Calculate shipping cost based on weight and method"""
    rate = SHIPPING_RATES.get(method, SHIPPING_RATES["ground"])
    units = total_weight_lbs / 100
    return round(rate * units, 2)

def find_nearest_consolidation_center(maker_locations):
    """Find optimal consolidation center based on maker locations"""
    # Simple mock: return Chicago for central US locations
    return CONSOLIDATION_CENTERS[0]
