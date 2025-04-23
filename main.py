import requests
import time

# --- CONFIGURATION ---
# <<< === CHANGE THIS URL === >>>
URL_TO_PING = "https://capricious-dorian-macaroni.glitch.me/wakemeup"
# <<< ===================== >>>

INTERVAL_SECONDS = 60  # 1 minute

# --- PINGER ---
print(f"--- Simple Pinger Started ---")
print(f"Pinging: {URL_TO_PING}")
print(f"Interval: {INTERVAL_SECONDS} seconds")
print(f"Press CTRL+C to stop.")
print("-" * 30)

while True:
    try:
        # Get the current time for logging
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Send the GET request (wait max 10 seconds for response)
        response = requests.get(URL_TO_PING, timeout=10)

        # Check if the status code is OK (usually 200)
        if response.status_code == 200:
            print(f"{current_time} - SUCCESS - Status: {response.status_code}")
        else:
            # Any other status code is treated as a failure here
            print(f"{current_time} - FAILED  - Status: {response.status_code}")

    except requests.exceptions.Timeout:
        # Specific error if the request takes too long
        print(f"{current_time} - FAILED  - Request Timed Out")
    except requests.exceptions.RequestException as e:
        # Catch other potential errors (connection refused, DNS error, etc.)
        print(f"{current_time} - FAILED  - Request Error: {e}")
    except Exception as e:
        # Catch any other unexpected errors
         print(f"{current_time} - FAILED  - An unexpected error occurred: {e}")


    # Wait for the defined interval before the next ping
    time.sleep(INTERVAL_SECONDS)