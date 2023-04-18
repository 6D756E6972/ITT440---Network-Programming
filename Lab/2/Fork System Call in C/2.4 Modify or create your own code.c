#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

void child_process() {
    char name[100];
    while(getchar() != '\n');
    // Ask user to enter their name
    printf("Enter your name: ");
    fgets(name, 100, stdin);
    // Display the name entered
    printf("Your name is: %s", name);
    // Exit child process
    exit(0);
}

int main() {
    int i;
    // Create 4 child processes
    for (i = 0; i < 4; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            // Child process
            child_process();
        } else if (pid < 0) {
            // Fork failed
            printf("Fork failed");
            exit(1);
        }
    }

    // Wait for all child processes to finish
    for (i = 0; i < 4; i++) {
        int status;
        wait(&status);
    }

    // Job is done
    printf("\nJob is done\n");

    return 0;
}
