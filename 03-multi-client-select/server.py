import socket
import selectors

sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"[+] Client conectat: {addr}")
    conn.setblocking(False)  # Socket non-blocant
    # Înregistrează conexiunea nouă pentru evenimente de citire
    sel.register(conn, selectors.EVENT_READ, data=read_wrapper)

def read_wrapper(conn):
    data = conn.recv(1024)
    if data:
        print(f"Primit: {data.decode().strip()}")
        conn.send(data)  # Trimitere înapoi (Echo)
    else:
        print("[-] Client deconectat")
        sel.unregister(conn)
        conn.close()

# Configurare socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5000))
server.listen()
server.setblocking(False)  # Non-blocant

# Înregistrează socket-ul principal pentru conexiuni noi
sel.register(server, selectors.EVENT_READ, data=accept_wrapper)

print("Serverul cu selectors rulează pe 127.0.0.1:5000...")

try:
    while True:
        # Blocare eficientă până când apare cel puțin un eveniment
        events = sel.select(timeout=None)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)
except KeyboardInterrupt:
    print("\nServer oprit.")
finally:
    sel.close()


