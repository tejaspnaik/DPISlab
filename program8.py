
#ARP-poisoning/sniffing attack

#server.py(run first)
# server_short.py
# server_ultra.py
import socket
from collections import defaultdict

H,P="127.0.0.1",6000
seen=defaultdict(set)

s=socket.socket();s.setsockopt(1,2,1);s.bind((H,P));s.listen(1)
print(f"[S] listening on {H}:{P} — waiting for client...")
c,addr=s.accept();print("[S] client connected:",addr)

while True:
    d=c.recv(1024)
    if not d:break
    m=d.decode().strip()
    print("[S] recv:",m)

    if m.startswith("ARP:"):
        _,ip,mac=m.split(":",2);mac=mac.lower()
        old=set(seen[ip]);seen[ip].add(mac)
        c.sendall(f"ACK {ip}->{mac}".encode())
        if len(seen[ip])>1 and mac not in old:
            print(f"!!! ALERT: IP {ip} seen with MACs {', '.join(sorted(seen[ip]))}")
    elif m=="quit":
        c.sendall(b"bye");break
    else:
        c.sendall(f"ECHO:{m}".encode())

print("[S] server stopped")

#client(run second)

# client_min.py
# client_short.py
# client_ultra.py
import socket,time

H,P="127.0.0.1",6000
msgs=[
 "ARP:10.0.0.1:aa:aa:aa:01",
 "ARP:10.0.0.2:aa:aa:aa:02",
 "HELLO",
 "ARP:10.0.0.1:aa:aa:aa:01",
 "ARP:10.0.0.1:02:bb:cc:03",
 "quit"
]

c=socket.create_connection((H,P))
for m in msgs:
    print("[C] send:",m)
    c.sendall(m.encode())
    print("[C] reply:",c.recv(1024).decode().strip())
    time.sleep(0.5)
c.close()
print("[C] client done")

