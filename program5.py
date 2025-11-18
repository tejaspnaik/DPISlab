#Eavesdrop Proxy (C → Attacker → Server)
#run this code after running server and client(run this third)
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
