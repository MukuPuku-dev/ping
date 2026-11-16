import requests
import time
import threading
import os
from flask import Flask

# --- CONFIGURATION ---
# <<< === ORIGINAL URL (DO NOT CHANGE) === >>>
URL_TO_PING = "https://capricious-dorian-macaroni.glitch.me/wakemeup"
# <<< ================================== >>>

PING_INTERVAL_SECONDS = 120  # 2 minutes for the original URL

# --- NEW URL CONFIGURATION ---
NEW_URL_TO_PING = "https://mukesh-4e2a.onrender.com/wakemeup"
NEW_URL_PING_INTERVAL_SECONDS = 5 * 60  # 5 minutes for the new URL

# --- MESSENGER DEMO URL CONFIGURATION ---
MESSENGER_DEMO_URL = "https://mukesh-v8c1.onrender.com/wakemeup" 
MESSENGER_PING_INTERVAL_SECONDS = 5 * 60  # 5 minutes for the Messenger Demo

REQUEST_TIMEOUT = 10 # Seconds to wait for ping response

# --- PINGER LOGIC (to run in background threads) ---

# This function will ping the original URL
def run_original_pinger():
    print(f"--- Original Pinger thread started ---")
    print(f"Pinging: {URL_TO_PING}")
    print(f"Interval: {PING_INTERVAL_SECONDS} seconds")
    print("-" * 30)

    while True:
        try:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            query_params = {'from': 'render-original-pinger'}

            response = requests.get(URL_TO_PING, timeout=REQUEST_TIMEOUT, params=query_params)

            if response.status_code == 200:
                print(f"{current_time} - ORIGINAL PING SUCCESS - Status: {response.status_code} - URL: {response.url}")
            else:
                print(f"{current_time} - ORIGINAL PING FAILED  - Status: {response.status_code} - URL: {response.url}")

        except requests.exceptions.Timeout:
            print(f"{current_time} - ORIGINAL PING FAILED  - Request Timed Out")
        except requests.exceptions.RequestException as e:
            print(f"{current_time} - ORIGINAL PING FAILED  - Request Error: {e}")
        except Exception as e:
            print(f"{current_time} - ORIGINAL PING FAILED  - An unexpected error occurred: {e}")

        time.sleep(PING_INTERVAL_SECONDS)

# This function will ping the new URL
def run_new_pinger():
    print(f"--- New Pinger thread started ---")
    print(f"Pinging: {NEW_URL_TO_PING}")
    print(f"Interval: {NEW_URL_PING_INTERVAL_SECONDS} seconds")
    print("-" * 30)

    while True:
        try:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            query_params = {'from': 'render-new-pinger'}

            response = requests.get(NEW_URL_TO_PING, timeout=REQUEST_TIMEOUT, params=query_params)

            if response.status_code == 200:
                print(f"{current_time} - NEW PING SUCCESS - Status: {response.status_code} - URL: {response.url}")
            else:
                print(f"{current_time} - NEW PING FAILED  - Status: {response.status_code} - URL: {response.url}")

        except requests.exceptions.Timeout:
            print(f"{current_time} - NEW PING FAILED  - Request Timed Out")
        except requests.exceptions.RequestException as e:
            print(f"{current_time} - NEW PING FAILED  - Request Error: {e}")
        except Exception as e:
            print(f"{current_time} - NEW PING FAILED  - An unexpected error occurred: {e}")

        time.sleep(NEW_URL_PING_INTERVAL_SECONDS)

# This function will ping the Messenger Demo URL
def run_messenger_pinger():
    print(f"--- Messenger Demo Pinger thread started ---")
    print(f"Pinging: {MESSENGER_DEMO_URL}")
    print(f"Interval: {MESSENGER_PING_INTERVAL_SECONDS} seconds")
    print("-" * 30)

    while True:
        try:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            query_params = {'from': 'render-messenger-pinger'}

            response = requests.get(MESSENGER_DEMO_URL, timeout=REQUEST_TIMEOUT, params=query_params)

            if response.status_code == 200:
                print(f"{current_time} - MESSENGER PING SUCCESS - Status: {response.status_code} - URL: {response.url}")
            else:
                print(f"{current_time} - MESSENGER PING FAILED  - Status: {response.status_code} - URL: {response.url}")

        except requests.exceptions.Timeout:
            print(f"{current_time} - MESSENGER PING FAILED  - Request Timed Out")
        except requests.exceptions.RequestException as e:
            print(f"{current_time} - MESSENGER PING FAILED  - Request Error: {e}")
        except Exception as e:
            print(f"{current_time} - MESSENGER PING FAILED  - An unexpected error occurred: {e}")

        time.sleep(MESSENGER_PING_INTERVAL_SECONDS)


# --- WEB SERVER (Flask) ---
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Pinger service is running! Check logs for ping status.'

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    # --- Start the original pinger in a background thread ---
    original_pinger_thread = threading.Thread(target=run_original_pinger, daemon=True)
    original_pinger_thread.start()
    print("--- Original Pinger thread initiated ---")

    # --- Start the new pinger in a separate background thread ---
    new_pinger_thread = threading.Thread(target=run_new_pinger, daemon=True)
    new_pinger_thread.start()
    print("--- New Pinger thread initiated ---")

    # --- Start the Messenger Demo pinger in a separate background thread ---
    messenger_pinger_thread = threading.Thread(target=run_messenger_pinger, daemon=True)
    messenger_pinger_thread.start()
    print("--- Messenger Demo Pinger thread initiated ---")

    # --- Start the Flask web server ---
    port = int(os.environ.get('PORT', 10000))
    print(f"--- Starting Flask web server on port {port} ---")
    app.run(host='0.0.0.0', port=port)
