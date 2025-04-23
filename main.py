import requests
import time
import threading
import os
from flask import Flask

# --- CONFIGURATION ---
# <<< === CHANGE THIS URL === >>>
URL_TO_PING = "https://capricious-dorian-macaroni.glitch.me/wakemeup"
# <<< ===================== >>>

PING_INTERVAL_SECONDS = 60  # 1 minute
REQUEST_TIMEOUT = 10 # Seconds to wait for ping response

# --- PINGER LOGIC (to run in a background thread) ---
def run_pinger():
    print(f"--- Pinger thread started ---")
    print(f"Pinging: {URL_TO_PING}")
    print(f"Interval: {PING_INTERVAL_SECONDS} seconds")
    print("-" * 30)

    while True:
        try:
            # Get the current time for logging
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")

            # Define query parameters
            query_params = {'from': 'render'}

            # Send the GET request with query parameters
            response = requests.get(URL_TO_PING, timeout=REQUEST_TIMEOUT, params=query_params)

            # Check status code
            if response.status_code == 200:
                print(f"{current_time} - PING SUCCESS - Status: {response.status_code} - URL: {response.url}") # Log URL to verify param
            else:
                print(f"{current_time} - PING FAILED  - Status: {response.status_code} - URL: {response.url}") # Log URL to verify param

        except requests.exceptions.Timeout:
            print(f"{current_time} - PING FAILED  - Request Timed Out")
        except requests.exceptions.RequestException as e:
            print(f"{current_time} - PING FAILED  - Request Error: {e}")
        except Exception as e:
             print(f"{current_time} - PING FAILED  - An unexpected error occurred: {e}")

        # Wait for the defined interval before the next ping
        time.sleep(PING_INTERVAL_SECONDS)

# --- WEB SERVER (Flask) ---
# Create Flask app instance
app = Flask(__name__)

# Define a simple route for Render's health checks (and basic access)
@app.route('/')
def hello_world():
    # This will be shown if you access the service's URL in a browser
    return 'Pinger service is running! Check logs for ping status.'

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    # --- Start the pinger in a background thread ---
    # Set daemon=True so the thread exits when the main app exits
    pinger_thread = threading.Thread(target=run_pinger, daemon=True)
    pinger_thread.start()
    print("--- Pinger thread initiated ---")

    # --- Start the Flask web server ---
    # Get port from environment variable or default to 10000
    port = int(os.environ.get('PORT', 10000))
    print(f"--- Starting Flask web server on port {port} ---")
    # Use host='0.0.0.0' to make it accessible externally (required by Render)
    app.run(host='0.0.0.0', port=port)
