# client.py
import socket
import threading
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

HOST = '127.0.0.1'
PORT = 5000

p = 23
g = 5

a = random.randint(1, 10)
A = pow(g, a, p)

shared_key = None
aes_key = None


def derive_key(shared):
    return hashlib.sha256(str(shared).encode()).digest()


def encrypt(msg):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(msg.encode(), AES.block_size))
    return cipher.iv + ciphertext


def decrypt(data):
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()


def receive(sock):
    global shared_key, aes_key

    while True:
        data = sock.recv(4096)

        if not data:
            break


        if data == b"WAIT":
            print("⏳ Waiting for another user...")

        elif data == b"START":
            print("🔗 Partner connected! Starting key exchange...")
            sock.send(str(A).encode())

        else:
            try:

                if shared_key is None:
                    B = int(data.decode())
                    shared_key = pow(B, a, p)
                    aes_key = derive_key(shared_key)

                    print(f"[KEY EXCHANGED] Shared key: {shared_key}")
                    print("💬 You can start chatting now:\n")

                else:
                    msg = decrypt(data)
                    print(f"\n[RECEIVED] {msg}")

            except:
                pass


def send(sock):
    while True:
        msg = input()
        if aes_key:
            sock.send(encrypt(msg))
        else:
            print("⏳ Still waiting for secure connection...")


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    threading.Thread(target=receive, args=(client,), daemon=True).start()
    send(client)


if __name__ == "__main__":
    main()
