import socket
import tqdm
import os
import sys
import time

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

if len(sys.argv) < 3:
    print("Usage: python3 <filename.py> <hostip> <port>")
    sys.exit(1)


host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket()

print(f"\nConnecting to {host}:{port}")
time.sleep(1)
s.connect((host,port))
print("\nConnected")

filename = input("Enter a file from this directory: ")
filesize = os.path.getsize(filename) #get file size

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit = "B", unit_scale = True, ncols = 75, unit_divisor = 1024)

with open(filename, "rb") as f:
        while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                        break

                s.sendall(bytes_read) # use sendall to assure transmission in busy network
                progress.update(len(bytes_read)) #update progress bar

progress.close()
print(f"File Sent!")

s.close()
