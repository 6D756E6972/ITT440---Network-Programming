import socket

def connect_to_server():
    host = "izani.synology.me"
    port = 8443

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        student_id = "2021619382"

        client_socket.sendall(student_id.encode())

        response = client_socket.recv(1024)
        print(response.decode())

        client_socket.close()

    except ConnectionRefusedError:
        print("Connection to the server was refused. Please make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    connect_to_server()
