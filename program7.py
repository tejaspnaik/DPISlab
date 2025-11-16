#MITM tampering (run this third)
import socket, random

L, S = ("127.0.0.1", 9000), ("127.0.0.1", 9001)

with socket.socket() as ls:
    ls.bind(L); ls.listen(1)
    c, _ = ls.accept()
    with c, socket.socket() as s:
        s.connect(S)

        d = c.recv(4096)
        t = d.decode(errors="replace")
        t2 = t.replace("42", str(random.randint(10,99)))
        s.sendall(t2.encode())

        r = s.recv(4096)


#Server(run this first)
import socket

H, P = "127.0.0.1", 9001
with socket.socket() as s:
    s.bind((H, P)); s.listen(1)
    c, _ = s.accept()
    with c:
        d = c.recv(4096)
        print("Server got:", d.decode(errors="replace"))
        c.sendall(b"Server->Client: ACK")

#Client code(run this second)
import socket

HOST, PORT = "127.0.0.1", 9000  # connect to proxy/attacker
MSG = "Client->Server: exam answer: 42"

with socket.socket() as s:
    s.connect((HOST, PORT))
    s.sendall(MSG.encode())
    r = s.recv(4096)
    print("Client got:", r.decode(errors="replace"))
