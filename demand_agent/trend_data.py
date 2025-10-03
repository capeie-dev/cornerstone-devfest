"""
Demand Analyzer Mock Data
Market trend signals and demand forecasts
"""

# Trending Products from Market Analysis
TRENDING_PRODUCTS = [
    {
        "product_id": "PROD_001",
        "name": "Precision Widget Bracket",
        "category": "Electronics Components",
        "demand_score": 9.2,
        "trend": "rising",
        "estimated_volume": 5000,
        "price_range": "$2.20 - $3.20",
        "signals": ["Reddit mentions +45%", "Amazon searches +32%", "YouTube reviews +28%"]
    },
    {
        "product_id": "PROD_002",
        "name": "Adjustable Phone Stand",
        "category": "Mobile Accessories",
        "demand_score": 7.8,
        "trend": "stable",
        "estimated_volume": 3500,
        "price_range": "$1.80 - $2.50",
        "signals": ["TikTok videos +15%", "Etsy searches +12%"]
    },
    {
        "product_id": "PROD_003",
        "name": "Cable Organizer Clip",
        "category": "Office Supplies",
        "demand_score": 8.5,
        "trend": "rising",
        "estimated_volume": 7000,
        "price_range": "$0.80 - $1.20",
        "signals": ["Pinterest pins +38%", "Twitter mentions +22%"]
    },
    {
        "product_id": "PROD_004",
        "name": "Laptop Cooling Stand",
        "category": "Computer Accessories",
        "demand_score": 6.9,
        "trend": "declining",
        "estimated_volume": 2000,
        "price_range": "$3.50 - $5.00",
        "signals": ["Google Trends -8%", "Amazon reviews stable"]
    },
    {
        "product_id": "PROD_005",
        "name": "Custom Key Holder",
        "category": "Home Organization",
        "demand_score": 8.1,
        "trend": "rising",
        "estimated_volume": 4500,
        "price_range": "$1.50 - $2.20",
        "signals": ["Instagram posts +42%", "Home Depot searches +18%"]
    }
]

# Market Signals by Category
MARKET_SIGNALS = {
    "Electronics Components": {
        "overall_trend": "strong_growth",
        "consumer_sentiment": "positive",
        "competition_level": "medium",
        "profit_margin": "high"
    },
    "Mobile Accessories": {
        "overall_trend": "stable",
        "consumer_sentiment": "neutral",
        "competition_level": "high",
        "profit_margin": "medium"
    },
    "Office Supplies": {
        "overall_trend": "growth",
        "consumer_sentiment": "positive",
        "competition_level": "low",
        "profit_margin": "medium"
    }
}

# Demand Forecasts
DEMAND_FORECASTS = {
    "PROD_001": {
        "30_days": {"volume": 5000, "confidence": 0.92},
        "60_days": {"volume": 8500, "confidence": 0.85},
        "90_days": {"volume": 12000, "confidence": 0.78}
    },
    "PROD_002": {
        "30_days": {"volume": 3500, "confidence": 0.88},
        "60_days": {"volume": 3800, "confidence": 0.82},
        "90_days": {"volume": 4000, "confidence": 0.75}
    },
    "PROD_003": {
        "30_days": {"volume": 7000, "confidence": 0.90},
        "60_days": {"volume": 9500, "confidence": 0.83},
        "90_days": {"volume": 11000, "confidence": 0.76}
    }
}

def get_product_by_id(product_id):
    """Helper to retrieve product by ID"""
    for product in TRENDING_PRODUCTS:
        if product["product_id"] == product_id:
            return product
    return None
