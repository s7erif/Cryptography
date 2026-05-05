# 🔐 Secure Encrypted Chat (Diffie-Hellman + AES)

## 📌 Overview

A simple peer-to-peer encrypted chat application built using Python.
The app uses Diffie-Hellman key exchange to establish a shared secret, then encrypts messages using AES.

---

## ⚙️ Features

* 🔑 Diffie-Hellman Key Exchange
* 🔐 AES Encryption (CBC Mode)
* 👥 Real-time chat between two clients
* 🔗 Automatic pairing system
* 😂 Fun chat modes (spam, roast, emojis)

---

## 🛠️ Technologies

* Python
* Sockets
* PyCryptodome

---

## ▶️ How to Run

### 1. Start server

```bash
python3 server.py
```

### 2. Start clients

```bash
python3 client.py
python3 client.py
```

---

## ⚠️ Notes

* This project is for educational purposes
* Not secure for production use

---

## 🚀 Future Improvements

* HMAC (message integrity)
* RSA authentication (prevent MITM)
* GUI interface
* Multi-user chat rooms
