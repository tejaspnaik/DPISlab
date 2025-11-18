
#ARP-poisoning/sniffing attack

#server.py(run first)

import socket
from collections import defaultdict

H, P = "127.0.0.1", 6000
seen = defaultdict(set)

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((H, P)); s.listen(1)
    print(f"[S] listening on {H}:{P} — waiting for client...")
    c, addr = s.accept()
    print("[S] client connected:", addr)
    with c:
        while True:
            d = c.recv(1024)
            if not d:
                break
            m = d.decode().strip()
            print("[S] recv:", m)

            if m.startswith("ARP:"):
                # split into at most 3 parts to mirror original robustness
                _, ip, mac = (m.split(":", 2) + ["", ""])[:3]
                mac = mac.lower()
                prev = set(seen[ip])
                seen[ip].add(mac)
                c.sendall(f"ACK {ip}->{mac}".encode())
                if len(seen[ip]) > 1 and mac not in prev:
                    print("!!! ALERT: IP", ip, "seen with MACs", ", ".join(sorted(seen[ip])))
            elif m.lower() in ("quit", "exit"):
                c.sendall(b"bye")
                break
            else:
                c.sendall(f"ECHO:{m}".encode())

print("[S] server stopped")
#client(run second)

# client_min.py
import socket, time

H, P = "127.0.0.1", 6000

msgs = [
    "ARP:10.0.0.1:aa:aa:aa:01",
    "ARP:10.0.0.2:aa:aa:aa:02",
    "HELLO",
    "ARP:10.0.0.1:aa:aa:aa:01",
    "ARP:10.0.0.1:02:bb:cc:03",  # simulated conflict
    "quit"
]

with socket.create_connection((H, P)) as c:
    for m in msgs:
        print("[C] send:", m)
        c.sendall(m.encode())
        try:
            r = c.recv(1024).decode().strip()
            print("[C] reply:", r)
        except Exception:
            print("[C] no reply")
        time.sleep(0.6)

print("[C] client done")
