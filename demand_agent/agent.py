"""
Demand Analyzer Agent
Analyzes market trends and identifies high-demand products for manufacturing

Following ADK pattern: https://google.github.io/adk-docs/get-started/quickstart/
"""

from google.adk.agents import Agent
from .trend_data import TRENDING_PRODUCTS, MARKET_SIGNALS, DEMAND_FORECASTS, get_product_by_id


def analyze_market_trends(product_category: str = "") -> dict:
    """
    Analyzes market trends to identify high-demand products in a category.
    
    Args:
        product_category: Optional category filter (e.g., 'Electronics Components', 'Mobile Accessories').
                         Leave empty to see all trending products.
    
    Returns:
        dict: Market analysis with trending products, demand scores, and signals
    """
    
    products = TRENDING_PRODUCTS
    
    # Filter by category if specified
    if product_category:
        products = [p for p in TRENDING_PRODUCTS if p["category"].lower() == product_category.lower()]
    
    # Sort by demand score (descending)
    products_sorted = sorted(products, key=lambda x: x["demand_score"], reverse=True)
    
    # Get category signals if specified
    category_signal = None
    if product_category and product_category in MARKET_SIGNALS:
        category_signal = MARKET_SIGNALS[product_category]
    
    return {
        "status": "success",
        "report": {
            "total_products_analyzed": len(products_sorted),
            "category_filter": product_category if product_category else "All Categories",
            "trending_products": products_sorted,
            "category_insights": category_signal,
            "recommendation": products_sorted[0] if products_sorted else None,
            "summary": f"Analyzed {len(products_sorted)} products. Top recommendation: {products_sorted[0]['name'] if products_sorted else 'None'} with demand score {products_sorted[0]['demand_score'] if products_sorted else 0}"
        }
    }


def get_product_recommendations(min_demand_score: float = 7.0) -> dict:
    """
    Gets product recommendations based on minimum demand threshold.
    
    Args:
        min_demand_score: Minimum demand score (0-10). Default is 7.0.
    
    Returns:
        dict: List of recommended products above the threshold
    """
    
    # Filter products above threshold
    recommended = [p for p in TRENDING_PRODUCTS if p["demand_score"] >= min_demand_score]
    
    # Sort by demand score
    recommended_sorted = sorted(recommended, key=lambda x: x["demand_score"], reverse=True)
    
    return {
        "status": "success",
        "report": {
            "threshold": min_demand_score,
            "total_recommendations": len(recommended_sorted),
            "products": recommended_sorted,
            "top_pick": recommended_sorted[0] if recommended_sorted else None,
            "summary": f"Found {len(recommended_sorted)} products above demand score {min_demand_score}. Top pick: {recommended_sorted[0]['name'] if recommended_sorted else 'None'}"
        }
    }


def calculate_demand_forecast(product_id: str, timeframe: str = "30_days") -> dict:
    """
    Calculates demand forecast for a specific product over a timeframe.
    
    Args:
        product_id: The product identifier (e.g., 'PROD_001')
        timeframe: Forecast period - '30_days', '60_days', or '90_days'. Default is '30_days'.
    
    Returns:
        dict: Demand forecast with volume estimates and confidence levels
    """
    
    # Get product details
    product = get_product_by_id(product_id)
    
    if not product:
        return {
            "status": "error",
            "error_message": f"Product {product_id} not found in trend database."
        }
    
    # Get forecast data
    if product_id not in DEMAND_FORECASTS:
        return {
            "status": "error",
            "error_message": f"No forecast data available for {product_id}."
        }
    
    forecast_data = DEMAND_FORECASTS[product_id]
    
    # Validate timeframe
    if timeframe not in forecast_data:
        return {
            "status": "error",
            "error_message": f"Invalid timeframe. Use '30_days', '60_days', or '90_days'."
        }
    
    forecast = forecast_data[timeframe]
    
    return {
        "status": "success",
        "report": {
            "product_id": product_id,
            "product_name": product["name"],
            "current_demand_score": product["demand_score"],
            "timeframe": timeframe,
            "forecasted_volume": forecast["volume"],
            "confidence_level": f"{forecast['confidence'] * 100:.0f}%",
            "trend": product["trend"],
            "recommendation": "MANUFACTURE" if forecast["confidence"] > 0.80 else "MONITOR",
            "summary": f"{product['name']}: Forecasted {forecast['volume']} units over {timeframe.replace('_', ' ')} with {forecast['confidence']*100:.0f}% confidence"
        }
    }


# Create the Demand Analyzer Agent (root_agent)
root_agent = Agent(
    name="demand_analyzer",
    model="gemini-2.0-flash",
    description=(
        "Market trend analyzer for Cornerstone's manufacturing network. "
        "Analyzes social media signals, search trends, and consumer behavior to identify "
        "high-demand products worth manufacturing. Provides demand forecasts and recommendations."
    ),
    instruction=(
        "You are the Cornerstone Demand Analyzer, an expert at identifying market opportunities.\n\n"
        "Your primary responsibilities:\n"
        "1. When asked about market trends or what to manufacture, call analyze_market_trends() to show trending products\n"
        "2. When asked for recommendations, call get_product_recommendations() with appropriate threshold\n"
        "3. When asked about future demand or forecasts, call calculate_demand_forecast() for specific products\n\n"
        "Key behaviors:\n"
        "- Always explain demand scores (0-10 scale, higher is better)\n"
        "- Highlight market signals (social media mentions, search trends)\n"
        "- Recommend products with demand score > 8.0 for immediate manufacturing\n"
        "- Explain confidence levels in forecasts\n"
        "- Translate data into actionable business recommendations\n\n"
        "Example interactions:\n"
        "User: 'What products are trending right now?'\n"
        "You: Call analyze_market_trends(), then summarize top 3 products with their demand scores and signals.\n\n"
        "User: 'Should we manufacture the Widget Bracket?'\n"
        "You: Call calculate_demand_forecast(product_id='PROD_001', timeframe='30_days'), then provide recommendation based on forecast."
    ),
    tools=[analyze_market_trends, get_product_recommendations, calculate_demand_forecast],
)
