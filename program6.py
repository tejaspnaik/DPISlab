#Dictionary Attack (run this third)
import hashlib

def h(p, s):
    return hashlib.sha256((s + p).encode()).hexdigest()

users = {
    "alice": ("S1", h("apple123", "S1")),
    "bob":   ("X9", h("qwerty",  "X9")),
    "carol": ("ZZ", h("letmein", "ZZ")),
}

print("Stored (salt,hash) samples (truncated):")
for u, (s, hs) in users.items():
    print(" ", u, s, hs[:12] + "...")

dict_words = ["password", "123456", "qwerty", "apple123", "letmein"]

print("\nAttacker tries small dictionary...")
for u, (s, stored) in users.items():
    hit = next((w for w in dict_words if h(w, s) == stored), None)
    if hit:
        print("[ATTACKER] Cracked", u, "->", hit)
    else:
        print("[ATTACKER] NOT cracked", u)




#Server(run this first)
# Server (run first)
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
            
#Client code(run this second)
# Client (run third, after starting proxy)
import socket

HOST, PORT = "127.0.0.1", 9000  # connect to proxy/attacker
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
