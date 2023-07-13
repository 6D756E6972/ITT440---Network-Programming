#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <signal.h>
#include <arpa/inet.h>

#define PORT 8484
#define BUFFER_SIZE 1024
#define MAX_CLIENTS 10

int serverSocket;
int clientSockets[MAX_CLIENTS];
int clientCount = 0;

void signalHandling(int sig) {
    printf("\nServer is shutting down...\n");
    for (int i = 0; i < clientCount; i++) {
        close(clientSockets[i]);
    }
    close(serverSocket);
    exit(EXIT_SUCCESS);
}

void handleClient(int clientSocket, struct sockaddr_in* clientAddress) {
    char clientIP[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &(clientAddress->sin_addr), clientIP, INET_ADDRSTRLEN);
    printf("\nClient %s connected\n", clientIP);

    while (1) {
        char buffer[BUFFER_SIZE];
        memset(buffer, 0, sizeof(buffer));
        ssize_t bytesRead = recv(clientSocket, buffer, sizeof(buffer) - 1, 0);
        if (bytesRead < 0) {
            perror("Receiving data failed");
            return;
        } else if (bytesRead == 0) {
            printf("Client %s disconnected\n", clientIP);
            break;
        }

        time_t currentTime = time(NULL);
        char* dateTimeString = ctime(&currentTime);
        size_t dateTimeStringLength = strlen(dateTimeString);

        // Combine client's text with server's current date and time
        char combinedString[BUFFER_SIZE + dateTimeStringLength];
        snprintf(combinedString, sizeof(combinedString), "%s received at %s", buffer, dateTimeString);

        // Send the combined string back to the client
        if (send(clientSocket, combinedString, strlen(combinedString), 0) < 0) {
            perror("Sending data failed");
            return;
        }

        printf("Processed request from client %s\n", clientIP);
    }

    // Close the client connection
    close(clientSocket);
}

int main() {
    signal(SIGINT, signalHandling);

    // Socket creation
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) {
        perror("Socket creation failed");
        return EXIT_FAILURE;
    }

    struct sockaddr_in serverAddress;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(PORT);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    // Binding socket
    if (bind(serverSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        perror("Binding failed");
        return EXIT_FAILURE;
    }

    // Listening to socket
    if (listen(serverSocket, 1) < 0) {
        perror("Listening failed");
        return EXIT_FAILURE;
    }

    printf("Server listening on port %d...\n", PORT);

    while (1) {
        struct sockaddr_in clientAddress;
        socklen_t clientAddressLength = sizeof(clientAddress);

        // Accepting connection from client
        int clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddress, &clientAddressLength);
        if (clientSocket < 0) {
            perror("Accepting connection failed");
            return EXIT_FAILURE;
        }

        if (clientCount < MAX_CLIENTS) {
            clientSockets[clientCount++] = clientSocket;
        } else {
            printf("Max client limit reached. Rejecting new connection.\n");
            close(clientSocket);
            continue;
        }

        if (fork() == 0) {
            // Child process handles the client request
            handleClient(clientSocket, &clientAddress);
            exit(EXIT_SUCCESS);
        }

        // Parent process continues accepting new connections
        close(clientSocket);
    }

    return EXIT_SUCCESS;
}
