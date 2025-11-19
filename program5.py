#Eavesdrop Proxy (C → Attacker → Server)
#run this code after running server and client(run this second)
#!/usr/bin/env python3
#!/usr/bin/env python3
import socket

# Proxy listens on L and forwards to real server S
L = ("127.0.0.1", 9000)   # client → proxy
S = ("127.0.0.1", 9001)   # proxy → server
BUF = 4096

# Listen for client
ls = socket.socket()
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind(L)
ls.listen(1)

print(f"[Proxy] Listening on {L}, forwarding to {S}")

# Accept client
client_sock, client_addr = ls.accept()
print(f"[Proxy] Client connected: {client_addr}")

# Connect to server
server_sock = socket.socket()
server_sock.connect(S)

# Receive from client
data = client_sock.recv(BUF)
if data:
    print("[Proxy] Captured (Client → Server):", data.decode(errors="replace"))

    # Forward to server
    server_sock.sendall(data)

    # Receive server reply
    reply = server_sock.recv(BUF)
    print("[Proxy] Captured (Server → Client):", reply.decode(errors="replace"))

    # Send back to client
    client_sock.sendall(reply)
else:
    print("[Proxy] No data received")

# Cleanup
server_sock.close()
client_sock.close()
ls.close()
print("[Proxy] Done")




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
