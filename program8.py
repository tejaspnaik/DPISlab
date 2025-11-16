
ARP-poisoning/sniffing attack

server

import socket
from collections import defaultdict

H, P = "127.0.0.1", 6000
seen = defaultdict(set)

with socket.socket() as s:
    s.bind((H, P)); s.listen(1)
    c, _ = s.accept()
    with c:
        while True:
            d = c.recv(1024)
            if not d: break
            m = d.decode().strip()

            if m.startswith("ARP:"):
                _, ip, mac = m.split(":")
                mac = mac.lower()
                seen[ip].add(mac)

                if len(seen[ip]) > 1:
                    print("ALERT:", ip, "→", list(seen[ip]))

                c.sendall(b"OK")
            else:
                c.sendall(b"ECHO")

client

# client_min.py
import socket, time

H, P = "127.0.0.1", 6000
msgs = [
    "ARP:10.0.0.1:aa:aa:aa:01",
    "ARP:10.0.0.1:bb:bb:bb:02",  # conflict → causes alert on server
    "ARP:10.0.0.2:cc:cc:cc:03",
    "done"
]

with socket.create_connection((H, P)) as c:
    for m in msgs:
        c.sendall(m.encode())
        print("Server:", c.recv(1024).decode())
        time.sleep(0.3)