"""
Bid Coordinator Mock Data
Bid windows, status tracking, and notifications
"""

from datetime import datetime, timedelta

# Active and Historical Bid Windows
BID_WINDOWS = {
    "KNICK_2025": {
        "job_id": "KNICK_2025",
        "product_name": "Precision Widget Bracket",
        "status": "OPEN",
        "opened_at": "2025-10-01 09:00:00",
        "closes_at": "2025-10-05 17:00:00",
        "duration_hours": 104,
        "required_qty": 5000,
        "required_skill": "CNC",
        "total_bids": 8,
        "participating_manufacturers": ["MAKER_A", "MAKER_C", "MAKER_D", "MAKER_E", "MAKER_G", "MAKER_H", "MAKER_J", "MAKER_B"],
        "participation_rate": "80%",
        "lowest_bid": 2.20,
        "highest_bid": 3.20,
        "average_bid": 2.65
    },
    "WIDGET_2024": {
        "job_id": "WIDGET_2024",
        "product_name": "Aluminum Housing",
        "status": "CLOSED",
        "opened_at": "2025-09-15 10:00:00",
        "closes_at": "2025-09-20 18:00:00",
        "closed_at": "2025-09-20 18:00:00",
        "duration_hours": 128,
        "required_qty": 3000,
        "required_skill": "CNC",
        "total_bids": 6,
        "participating_manufacturers": ["MAKER_A", "MAKER_C", "MAKER_F", "MAKER_H", "MAKER_I", "MAKER_J"],
        "participation_rate": "60%",
        "winning_manufacturers": ["MAKER_C", "MAKER_H"],
        "final_cost": "$8,000"
    }
}

# Notification Templates
NOTIFICATIONS = {
    "bid_opened": {
        "subject": "New Bid Opportunity: {job_id}",
        "message": "A new bid window has opened for {product_name}. Required: {required_qty} units ({required_skill}). Submit your bid before {closes_at}."
    },
    "bid_closing_soon": {
        "subject": "Bid Closing Soon: {job_id}",
        "message": "The bid window for {job_id} closes in 24 hours. Submit your bid now!"
    },
    "bid_closed": {
        "subject": "Bid Window Closed: {job_id}",
        "message": "The bid window for {job_id} is now closed. Winners will be notified within 24 hours."
    },
    "winner_notification": {
        "subject": "Congratulations! You Won Bid {job_id}",
        "message": "You've been selected for {job_id}! Quantity: {quantity} units at ${price}/unit. Total value: ${total}. Production deadline: {deadline}."
    },
    "not_selected": {
        "subject": "Bid Result: {job_id}",
        "message": "Thank you for participating in {job_id}. Unfortunately, your bid was not selected this time. Keep bidding to win future opportunities!"
    }
}

def get_bid_window(job_id):
    """Helper to retrieve bid window by job_id"""
    return BID_WINDOWS.get(job_id)

def calculate_time_remaining(closes_at_str):
    """Calculate hours remaining until bid closes"""
    closes_at = datetime.strptime(closes_at_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    delta = closes_at - now
    hours_remaining = max(0, delta.total_seconds() / 3600)
    return round(hours_remaining, 1)
