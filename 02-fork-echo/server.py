import socket
import os
import sys
import signal

HOST = '127.0.0.1'
PORT = 5000

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"🚀 Serverul părinte ascultă pe {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        print(f"[+] Conexiune nouă de la {addr}")

        pid = os.fork()

        if pid == 0:
            # ---> SUNTEM ÎN PROCESUL COPIL <---
            s.close() 
            
            try:
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break # Clientul a închis conexiunea normal
                        
                        text_primit = data.decode('utf-8').strip()
                        print(f"[Copil {os.getpid()}] Primit de la {addr}: {text_primit}")
                        conn.sendall(data)
                        
            except ConnectionResetError:
                # Interceptăm deconectarea bruscă (când clientul dă force close)
                print(f"[!] Clientul {addr} a întrerupt brusc conexiunea (reset by peer).")
            finally:
                # Ne asigurăm că procesul copil se închide curat, indiferent de erori
                print(f"[-] Proces copil {os.getpid()} s-a terminat pentru {addr}")
                sys.exit(0) 
            
        else:
            # ---> SUNTEM ÎN PROCESUL PĂRINTE <---
            conn.close()

