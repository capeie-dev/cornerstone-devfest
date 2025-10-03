"""
Cornerstone Data Mocks
Hardcoded data for ADK Hackathon Demo
"""

# Mock Manufacturers Database - 10 US-based micro-manufacturers
MOCK_MAKERS = [
    {
        "id": "MAKER_A",
        "name": "Precision CNC Ohio",
        "skill": "CNC",
        "base_rate": 2.50,
        "max_capacity": 2000,
        "location": {"lat": 39.9612, "lng": -82.9988, "city": "Columbus, OH"},
        "lead_time_days": 10
    },
    {
        "id": "MAKER_B",
        "name": "Detroit 3D Prints",
        "skill": "3D",
        "base_rate": 3.00,
        "max_capacity": 1500,
        "location": {"lat": 42.3314, "lng": -83.0458, "city": "Detroit, MI"},
        "lead_time_days": 8
    },
    {
        "id": "MAKER_C",
        "name": "Texas CNC Works",
        "skill": "CNC",
        "base_rate": 2.25,
        "max_capacity": 3000,
        "location": {"lat": 29.7604, "lng": -95.3698, "city": "Houston, TX"},
        "lead_time_days": 12
    },
    {
        "id": "MAKER_D",
        "name": "Carolina Fabrication",
        "skill": "CNC",
        "base_rate": 2.75,
        "max_capacity": 1800,
        "location": {"lat": 35.2271, "lng": -80.8431, "city": "Charlotte, NC"},
        "lead_time_days": 9
    },
    {
        "id": "MAKER_E",
        "name": "Portland Precision",
        "skill": "CNC",
        "base_rate": 3.10,
        "max_capacity": 1200,
        "location": {"lat": 45.5152, "lng": -122.6784, "city": "Portland, OR"},
        "lead_time_days": 11
    },
    {
        "id": "MAKER_F",
        "name": "Phoenix 3D Hub",
        "skill": "3D",
        "base_rate": 2.80,
        "max_capacity": 2500,
        "location": {"lat": 33.4484, "lng": -112.0740, "city": "Phoenix, AZ"},
        "lead_time_days": 7
    },
    {
        "id": "MAKER_G",
        "name": "Boston Manufacturing Co",
        "skill": "CNC",
        "base_rate": 3.25,
        "max_capacity": 1000,
        "location": {"lat": 42.3601, "lng": -71.0589, "city": "Boston, MA"},
        "lead_time_days": 10
    },
    {
        "id": "MAKER_H",
        "name": "Denver Micro-Mfg",
        "skill": "CNC",
        "base_rate": 2.60,
        "max_capacity": 2200,
        "location": {"lat": 39.7392, "lng": -104.9903, "city": "Denver, CO"},
        "lead_time_days": 9
    },
    {
        "id": "MAKER_I",
        "name": "Seattle Makers Guild",
        "skill": "3D",
        "base_rate": 3.15,
        "max_capacity": 1600,
        "location": {"lat": 47.6062, "lng": -122.3321, "city": "Seattle, WA"},
        "lead_time_days": 8
    },
    {
        "id": "MAKER_J",
        "name": "Atlanta Rapid Proto",
        "skill": "CNC",
        "base_rate": 2.40,
        "max_capacity": 2800,
        "location": {"lat": 33.7490, "lng": -84.3880, "city": "Atlanta, GA"},
        "lead_time_days": 11
    }
]

# Mock Bids for Current Job (KNICK_2025) - 8 bids submitted
MOCK_BIDS = [
    {
        "bid_id": "BID_001",
        "maker_id": "MAKER_C",
        "bid_price_per_unit": 2.20,
        "max_batch_size": 2500
    },
    {
        "bid_id": "BID_002",
        "maker_id": "MAKER_A",
        "bid_price_per_unit": 2.45,
        "max_batch_size": 1800
    },
    {
        "bid_id": "BID_003",
        "maker_id": "MAKER_J",
        "bid_price_per_unit": 2.35,
        "max_batch_size": 2000
    },
    {
        "bid_id": "BID_004",
        "maker_id": "MAKER_H",
        "bid_price_per_unit": 2.55,
        "max_batch_size": 1500
    },
    {
        "bid_id": "BID_005",
        "maker_id": "MAKER_D",
        "bid_price_per_unit": 2.70,
        "max_batch_size": 1200
    },
    {
        "bid_id": "BID_006",
        "maker_id": "MAKER_G",
        "bid_price_per_unit": 3.20,
        "max_batch_size": 800
    },
    {
        "bid_id": "BID_007",
        "maker_id": "MAKER_E",
        "bid_price_per_unit": 3.05,
        "max_batch_size": 1000
    },
    {
        "bid_id": "BID_008",
        "maker_id": "MAKER_B",
        "bid_price_per_unit": 2.95,
        "max_batch_size": 1400
    }
]

# Current High-Demand Product Job Specification
CURRENT_JOB = {
    "job_id": "KNICK_2025",
    "product_name": "Precision Widget Bracket",
    "required_qty": 5000,
    "required_skill": "CNC",
    "deadline_days": 30,
    "description": "High-demand CNC-machined bracket for consumer electronics assembly",
    "estimated_price_range": "$2.20 - $3.20 per unit"
}


def get_maker_by_id(maker_id: str):
    """Helper function to retrieve maker details from MOCK_MAKERS by ID"""
    for maker in MOCK_MAKERS:
        if maker["id"] == maker_id:
            return maker
    return None
