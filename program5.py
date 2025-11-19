#Eavesdrop Proxy (C → Attacker → Server)
#run this code after running server and client(run this second)
#!/usr/bin/env python3
#!/usr/bin/env python3
import socket

L, S = ("127.0.0.1", 9000), ("127.0.0.1", 9001)
BUF = 4096

ls = socket.socket()
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind(L); ls.listen(1)
print("[Attacker-EAVESDROP] listening on", L, "forward to", S)

c, addr = ls.accept()
print("[Attacker] client connected", addr)

s = socket.socket(); s.connect(S)

d = c.recv(BUF)
if d:
    txt = d.decode(errors="replace")
    print("[Attacker] captured (C->S):", txt)
    s.sendall(d)
    r = s.recv(BUF)
    print("[Attacker] captured (S->C):", r.decode(errors="replace"))
    c.sendall(r)
else:
    print("[Attacker] no data")

s.close(); c.close(); ls.close()
print("[Attacker] done")



#Server(run this first)
# Server (run first)
# SERVER
import socket

HOST, PORT = "127.0.0.1", 9001

s = socket.socket()
s.bind((HOST, PORT))
s.listen()

print(f"[Server] Listening on {HOST}:{PORT}")
conn, addr = s.accept()

print(f"[Server] Connected by {addr}")
data = conn.recv(4096)

if data:
    print("[Server] Received:", data.decode())
    conn.sendall(b"ACK")
else:
    print("[Server] No data")

conn.close()
s.close()

            
#Client code(run this second)
# Client (run third, after starting proxy)
# CLIENT
import socket

HOST, PORT = "127.0.0.1", 9000
MSG = "Client->Server: exam answer: 42"

s = socket.socket()
s.connect((HOST, PORT))

print("[Client] Sending:", MSG)
s.sendall(MSG.encode())

reply = s.recv(4096)
print("[Client] Reply:", reply.decode() if reply else "No reply")

s.close()
