import socket

def convert_to_atmosphere(pressure_bar):
    return pressure_bar * 0.986923

def start_server():
    host = "0.0.0.0"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server listening on {}:{}".format(host, port))

    while True:
        conn, addr = server_socket.accept()
        print("Connected by:", addr)

        data = conn.recv(1024)
        if not data:
            break

        try:
            pressure_bar = float(data.decode())
            atmosphere_standard = convert_to_atmosphere(pressure_bar)
            conn.sendall(str(atmosphere_standard).encode())
        except ValueError:
            conn.sendall(b"Invalid input. Please enter a valid numerical value.")

        conn.close()

if __name__ == "__main__":
    start_server()
