
#ARP-poisoning/sniffing attack

#server.py(run first)
# server_short.py
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

    while True:
        d = c.recv(1024)
        if not d: break
        msg = d.decode().strip()
        print("[S] recv:", msg)

        if msg.startswith("ARP:"):
            _, ip, mac = msg.split(":", 2)
            mac = mac.lower()
            old = set(seen[ip])
            seen[ip].add(mac)
            c.sendall(f"ACK {ip}->{mac}".encode())

            if len(seen[ip]) > 1 and mac not in old:
                print(f"!!! ALERT: IP {ip} seen with MACs {', '.join(sorted(seen[ip]))}")

        elif msg.lower() == "quit":
            c.sendall(b"bye")
            break

        else:
            c.sendall(f"ECHO:{msg}".encode())

print("[S] server stopped")

#client(run second)

# client_min.py
# client_short.py
import socket, time

H, P = "127.0.0.1", 6000
msgs = [
    "ARP:10.0.0.1:aa:aa:aa:01",
    "ARP:10.0.0.2:aa:aa:aa:02",
    "HELLO",
    "ARP:10.0.0.1:aa:aa:aa:01",
    "ARP:10.0.0.1:02:bb:cc:03",
    "quit"
]

with socket.create_connection((H, P)) as c:
    for m in msgs:
        print("[C] send:", m)
        c.sendall(m.encode())
        r = c.recv(1024).decode().strip()
        print("[C] reply:", r)
        time.sleep(0.6)

print("[C] client done")
