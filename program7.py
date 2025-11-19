#run the files in this manner:Server (9001) → Attacker/Proxy (9000) → Client
# MITM tampering (run this second)
# proxy.py  (short & simple MITM)
# attacker_mitm.py — MITM that modifies "42" → random number
import socket
import random

L = ("127.0.0.1", 9000)   # client → attacker (listen here)
S = ("127.0.0.1", 9001)   # attacker → server (forward here)
BUF = 4096

# Listen for client
listener = socket.socket()
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(L)
listener.listen(1)

print(f"[MITM] Listening on {L}, forwarding to {S}")

# Accept client
client_sock, client_addr = listener.accept()
print(f"[MITM] Client connected: {client_addr}")

# Connect to server
server_sock = socket.socket()
server_sock.connect(S)

# Receive from client
data = client_sock.recv(BUF)
if not data:
    print("[MITM] No data from client")
else:
    original = data.decode(errors="replace")
    print("[MITM] Captured (Client → Server):", original)

    # Tamper: replace "42" with random 2-digit number
    new_value = str(random.randint(10, 99))
    tampered = original.replace("42", new_value)

    print("[MITM] Tampered message:", tampered)

    # Forward tampered message to server
    server_sock.sendall(tampered.encode())

    # Receive server reply
    reply = server_sock.recv(BUF)
    print("[MITM] Captured (Server → Client):", reply.decode(errors="replace"))

    # Send reply back to client
    client_sock.sendall(reply)

# Cleanup
server_sock.close()
client_sock.close()
listener.close()

print("[MITM] Done")



# Server (run this first)
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


# Client (run this third, after starting proxy)
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

