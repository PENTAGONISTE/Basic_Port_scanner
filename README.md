# 🔍 TCP Port Scanner

A fast, multithreaded TCP port scanner with banner grabbing built in Python.  
Designed for network reconnaissance and security auditing on systems you own or have explicit permission to test.

---

## Features

- **Multithreaded scanning** — configurable thread count for fast results
- **Banner grabbing** — identifies the service running on each open port, with HTTP fallback
- **Flexible CLI** — custom port ranges, thread count, and hostname or IP as target
- **Hostname resolution** — accepts both IPs and domain names (e.g. `scanme.nmap.org`)

---

## Requirements

- Python 3.x
- No external libraries — uses the standard library only

---

## Usage

```bash
python scanner.py <target> [options]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `target` | IP address or hostname to scan | required |
| `-s`, `--start` | Start port | 1 |
| `-e`, `--end` | End port | 1024 |
| `-t`, `--threads` | Number of threads | 50 |

### Examples

```bash
# Basic scan (ports 1–1024)
python scanner.py 192.168.1.1

# Full port scan with more threads
python scanner.py 192.168.1.1 -s 1 -e 65535 -t 100

# Scan a hostname
python scanner.py scanme.nmap.org -s 20 -e 443
```

---

## Example Output

```
[*] Scanning target 45.33.32.156 (Ports 1 to 1024) with 50 threads...

Port 22  is OPEN - Service: SSH-2.0-OpenSSH_6.6.1p1
Port 80  is OPEN - Service: HTTP/1.1 200 OK
Port 443 is OPEN - Service: Unknown Service

[*] Scan completed.
```

---

## How It Works

1. Spawns N worker threads that pull ports from a shared queue
2. Each thread attempts a TCP connection to the target port
3. On success, opens a second connection to grab the service banner
4. Falls back to an HTTP GET request if no banner is returned passively
5. Results are printed as open ports are discovered

---

## Disclaimer

> This tool is intended for educational purposes and authorized security testing only.  
> Only use it on systems you own or have explicit written permission to scan.  
> Unauthorized port scanning may be illegal in your jurisdiction.

---

## Author

**Elhyani Abderrahman**  
1st year Engineering Student — Cybersecurity, ENSAM Casablanca  
[LinkedIn](https://www.linkedin.com/in/abderrahman-el-hyani-b2a393398/) · [GitHub](https://github.com/PENTAGONISTE)