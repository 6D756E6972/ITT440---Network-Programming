import socket

def get_user_input():
    try:
        pressure_bar = float(input("Enter pressure in bar: "))
        return pressure_bar
    except ValueError:
        print("Invalid input. Please enter a valid numerical value.")
        return get_user_input()

def connect_to_server():
    host = "192.168.218.128"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    pressure_bar = get_user_input()

    client_socket.sendall(str(pressure_bar).encode())

    response = client_socket.recv(1024)
    print("Received atmosphere-standard value from server:", response.decode())

    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
