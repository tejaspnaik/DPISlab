#How to run
#Generate the certificate & key using this command :openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
#it might not work in your pc because ssl is not installed download it from here:https://slproweb.com/products/Win32OpenSSL.html
#install it and add to path then check ssl version using openssl version
#after u run this command:openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes it will ask for info put '.' as answer for everything 
#it will generate 2 .pem files
#in same directory as the 2 files create server.py and client.py given below
#run server.py first then client .py thats it

#server.py
import socket, ssl

HOST = "127.0.0.1"
PORT = 4443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("cert.pem", "key.pem")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)
    print(f"Server listening on {HOST}:{PORT} with TLS...")

    conn, addr = sock.accept()
    with context.wrap_socket(conn, server_side=True) as tls:
        print(f"Secure connection from {addr}")
        data = tls.recv(1024)
        print("Received (after decryption):", data.decode())
        reply = b"secure reply: " + data
        tls.sendall(reply)



#client.py

import socket, ssl

HOST = "127.0.0.1"
PORT = 4443

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # minimalist lab mode

with socket.create_connection((HOST, PORT)) as raw:
    with context.wrap_socket(raw, server_hostname=HOST) as tls:
        print("TLS connection established!")
        message = "Hello Secure World!"
        print(f'Sending: "{message}"')
        tls.sendall(message.encode())

        reply = tls.recv(1024).decode()
        print("Received from server:", reply)






