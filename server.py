# server.py
import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

waiting_client = None
pairs = {}  # client -> partner


def handle_client(client):
    global pairs

    while True:
        try:
            data = client.recv(4096)
            if not data:
                break

            partner = pairs.get(client)
            if partner:
                partner.send(data)

        except:
            break

    # cleanup
    partner = pairs.get(client)
    if partner:
        try:
            partner.close()
        except:
            pass
        del pairs[partner]

    if client in pairs:
        del pairs[client]

    client.close()


def main():
    global waiting_client

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER RUNNING] {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        print(f"[NEW CONNECTION] {addr}")

        if waiting_client is None:
            waiting_client = client
            client.send(b"WAIT")
            print("🕐 Client waiting for partner...")
        else:

            partner = waiting_client
            waiting_client = None

            pairs[client] = partner
            pairs[partner] = client

            client.send(b"START")
            partner.send(b"START")

            print("🔥 Pair created!")

            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
            threading.Thread(target=handle_client, args=(partner,), daemon=True).start()


if __name__ == "__main__":
    main()
