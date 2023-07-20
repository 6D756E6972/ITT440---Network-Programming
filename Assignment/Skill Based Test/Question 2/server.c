#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define MIN_NUMBER 100
#define MAX_NUMBER 999
#define BUFFER_SIZE 1024

int main()
{
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    socklen_t client_address_length;
    char buffer[BUFFER_SIZE];

    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1)
    {
        perror("Socket creation failed");
        exit(1);
    }

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(8888);

    if (bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0)
    {
        perror("Binding failed");
        exit(1);
    }

    if (listen(server_socket, 5) < 0)
    {
        perror("Listening failed");
        exit(1);
    }

    printf("Server listening on port 8888 ...\n");

    while (1)
    {
        client_address_length = sizeof(client_address);
        client_socket = accept(server_socket, (struct sockaddr *)&client_address, &client_address_length);
        if (client_socket < 0)
        {
            perror("Accepting connection failed");
            exit(1);
        }

        printf("Client connected\n");

        int random_number = (rand() % (MAX_NUMBER - MIN_NUMBER + 1)) + MIN_NUMBER;

        sprintf(buffer, "%d", random_number);

        if (send(client_socket, buffer, strlen(buffer), 0) < 0)
        {
            perror("Sending data failed");
            exit(1);
        }

        printf("Random number sent: %s\n", buffer);
      
        close(client_socket);
        printf("Client disconnected\n");
    }

    close(server_socket);

    return 0;
}
