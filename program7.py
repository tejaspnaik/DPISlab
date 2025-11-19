#run the files in this manner:Server (9001) → Attacker/Proxy (9000) → Client
# MITM tampering (run this second)
# proxy.py  (short & simple MITM)
import socket, random

L, S = ("127.0.0.1", 9000), ("127.0.0.1", 9001)
BUF = 4096

ls = socket.socket()
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind(L); ls.listen(1)
print("[Attacker-MITM] listening on", L, "forward to", S)

c, addr = ls.accept()
print("[Attacker] client connected", addr)

s = socket.socket()
s.connect(S)

d = c.recv(BUF)
if not d:
    print("[Attacker] no data from client")
else:
    t = d.decode(errors="replace")
    print("[Attacker] captured (C->S):", t)
    t2 = t.replace("42", str(random.randint(10, 99)))
    print("[Attacker] tampered ->", t2)
    s.sendall(t2.encode())
    r = s.recv(BUF)
    print("[Attacker] captured (S->C):", r.decode(errors="replace"))
    c.sendall(r)

s.close(); c.close(); ls.close()
print("[Attacker] done")


# Server (run this first)
import socket

H, P = "127.0.0.1", 9001
with socket.socket() as s:
    s.bind((H, P)); s.listen(1)
    print("[Server] listening on", (H, P))
    c, addr = s.accept()
    with c:
        print("[Server] connection from", addr)
        d = c.recv(4096)
        if not d:
            print("[Server] no data")
        else:
            print("[Server] received:", d.decode(errors="replace"))
            c.sendall(b"Server->Client: ACK")
            print("[Server] sent ACK")


# Client (run this third, after starting proxy)
import socket

HOST, PORT = "127.0.0.1", 9000  # proxy
MSG = "Client->Server: exam answer: 42"

with socket.socket() as s:
    s.connect((HOST, PORT))
    print("[Client] sending:", MSG)
    s.sendall(MSG.encode())
    r = s.recv(4096)
    if r:
        print("[Client] got reply:", r.decode(errors="replace"))
    else:
        print("[Client] no reply")

