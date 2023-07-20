import socket
import threading
import random

quotes = [
    "If, at first, you do not succeed, call it version 1.0. ― Khayri R.R. Woulfe",
    "Code is like humor. When you have to explain it, it’s bad. – Cory House",
    "It’s not a bug; it’s an undocumented feature. ― Anonymous",
    "Java is to JavaScript what car is to Carpet. – Chris Heilmann",
    "There is always one more bug to fix.  – Ellen Ullman",
    "Confusion is part of programming. ― Felienne Hermans",
    "Copy-and-Paste was programmed by programmers for programmers actually. - Anonymous",
    "Apapun terjadi, tetaplah bernafas.. - Munerrr",
]

def get_random_quote():
    return random.choice(quotes)

def handle_client(client_socket):
    quote = get_random_quote()
    client_socket.send(quote.encode())
    client_socket.close()

def start_server():
    host = "0.0.0.0"
    port = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("QOTD Server listening on {}:{}".format(host, port))

    while True:
        client_socket, client_addr = server_socket.accept()
        print("Connected by:", client_addr)

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
