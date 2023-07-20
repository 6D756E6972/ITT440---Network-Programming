#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

int main()
{
    int client_socket;
    struct sockaddr_in server_address;
    char buffer[BUFFER_SIZE];

    client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == -1)
    {
        perror("Socket creation failed");
        exit(1);
    }
  
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(8888);
    if (inet_pton(AF_INET, "192.168.218.128", &server_address.sin_addr) <= 0)
    {
        perror("Invalid address or address not supported");
        exit(1);
    }

    if (connect(client_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0)
    {
        perror("Connection failed");
        exit(1);
    }

    int bytes_received = recv(client_socket, buffer, BUFFER_SIZE - 1, 0);
    if (bytes_received < 0)
    {
        perror("Receiving data failed");
        exit(1);
    }

    buffer[bytes_received] = '\0';

    printf("Received random number: %s\n", buffer);

    close(client_socket);

    return 0;
}
