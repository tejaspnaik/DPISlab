Eavesdrop Proxy (C → Attacker → Server)

import socket

L, S = ("127.0.0.1", 9000), ("127.0.0.1", 9001)

with socket.socket() as ls:
    ls.bind(L)
    ls.listen(1)
    c, _ = ls.accept()

    with c, socket.socket() as s:
        s.connect(S)

        d = c.recv(4096)
        print("[EAVESDROP C->S]", d.decode(errors="replace"))
        s.sendall(d)

        r = s.recv(4096)
        print("[EAVESDROP S->C]", r.decode(errors="replace"))
        c.sendall(r)


Server
import socket

H, P = "127.0.0.1", 9001
with socket.socket() as s:
    s.bind((H, P)); s.listen(1)
    c, _ = s.accept()
    with c:
        d = c.recv(4096)
        print("Server got:", d.decode(errors="replace"))
        c.sendall(b"Server->Client: ACK")

Client code
import socket

HOST, PORT = "127.0.0.1", 9000  # connect to proxy/attacker
MSG = "Client->Server: exam answer: 42"

with socket.socket() as s:
    s.connect((HOST, PORT))
    s.sendall(MSG.encode())
    r = s.recv(4096)
    print("Client got:", r.decode(errors="replace"))

