#!/usr/bin/env python3
"""
Weather Alerts Monitor
Polls the NWS API every 10 seconds and displays total active alerts.
"""

import requests
import time
from datetime import datetime

REQUEST_TIMEOUT = 5  # seconds
POLL_INTERVAL = 10  # seconds
URL = "https://api.weather.gov/alerts/active/count"

def get_active_alerts():
    """Fetch and display the total count of active weather alerts."""
    
    try:
        response = requests.get(URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        #Extract the 'total' value (or use 'N/A' if missing)
        total = data.get('total', 'N/A')
        
        timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        print(f"{timestamp} – Total {total} active alerts")
        
    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        print(f"{timestamp} – Error fetching alerts: {e}")
    except (KeyError, ValueError) as e:
        timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        print(f"{timestamp} – Error parsing response: {e}")

def main():
    """Main loop that runs every 10 seconds."""
    print("Weather Alerts Monitor Started")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            get_active_alerts()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\n\nMonitor stopped by user")

if __name__ == "__main__":
    main()
