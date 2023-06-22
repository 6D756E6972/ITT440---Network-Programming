import socket
import math

SERVER = "IP ADDRESS"
PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER, PORT))

while True:
        print("\n--- Calculator Menu ---")
        print("1. Logarithmic (log)")
        print("2. Square Root")
        print("3. Exponential (exp)")
        print("0. Exit")

        option = input("Enter an option: ")
        if option == "0":
                break

        num = input("Enter a number: ")
        exp = f"{option}:{num}"
        client.sendall(exp.encode())

        # Here we received output from the server socket
        answer = client.recv(1024)
        print("Answer is ",answer.decode())

client.close()
