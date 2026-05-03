import socket
import queue
import threading
import argparse
import sys

def get_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        
        try:
            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            if banner:
                s.close()
                return banner
                
        except socket.timeout:
            try:
                s.send(b"GET / HTTP/1.1\r\n\r\n")
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                s.close()
                return banner
            except Exception:
                pass 
        
        s.close()
    except Exception:
        pass
        
    return "Unknown Service"

def worker(ip, q):
    while True:
        item = q.get()
        if item is None:  
            break
        try:
            s = socket.create_connection((ip, item), timeout=1)
            s.close()
            banner = get_banner(ip, item)
            clean_banner = banner.split('\n')[0] if banner else "Unknown Service"
            print(f"Port {item} is OPEN - Service: {clean_banner}")
        except OSError:
            pass
        finally:
            q.task_done()

def main():
    
    parser = argparse.ArgumentParser(description="Fast Multithreaded TCP Port Scanner with Banner Grabbing")
    parser.add_argument("target", help="The target IP address or hostname (e.g., scanme.nmap.org)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Number of threads (default: 50)")

    args = parser.parse_args()

    
    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"[-] Error: Could not resolve hostname {args.target}")
        sys.exit()

    print(f"[*] Scanning target {ip} (Ports {args.start} to {args.end}) with {args.threads} threads...\n")

    
    q = queue.Queue()
    threads = []

    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(ip, q))
        t.start()
        threads.append(t)

    
    for port in range(args.start, args.end + 1):
        q.put(port)

    
    q.join()

   
    for _ in range(args.threads):
        q.put(None)

    for t in threads:
        t.join()

    print("\n[*] Scan completed.")

if __name__ == "__main__":
    main()