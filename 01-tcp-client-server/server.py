import socket

HOST = "0.0.0.0"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = server.accept()

    with conn:
        print(f"Client connected: {addr}")

        while True:
            data = conn.recv(4096)

            if not data:
                print("Client disconnected.")
                break

            message = data.decode("utf-8")
            print(f"Client: {message}")

            if message.lower() == "exit":
                break

            response = input("Server: ")
            conn.sendall(response.encode("utf-8"))

            if response.lower() == "exit":
                break

