#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

#define READ_END 0
#define WRITE_END 1

void sigint_handler(int signum) {
    printf("KeyboardInterrupt. Exiting...\n");
    exit(0);
}

int is_prime(int n) {
    if (n < 2) {
        return 0;
    }
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            return 0;
        }
    }
    return 1;
}

int main() {
    int fd[2];
    pid_t pid;
    int number, result;

    signal(SIGINT, sigint_handler);

    if (pipe(fd) == -1) {
        fprintf(stderr, "Pipe failed");
        return 1;
    }

    pid = fork();

    if (pid < 0) {
        fprintf(stderr, "Fork failed");
        return 1;
    }

    if (pid == 0) {
        // child process
        close(fd[READ_END]);
        printf("Enter a number: ");
        scanf("%d", &number);
        result = is_prime(number);
        write(fd[WRITE_END], &result, sizeof(result));
        close(fd[WRITE_END]);
        exit(0);
    } else {
        // parent process
        close(fd[WRITE_END]);
        read(fd[READ_END], &result, sizeof(result));
        if (result) {
            printf("The number is a prime number.\n");
        } else {
            printf("The number is not a prime number.\n");
        }
        close(fd[READ_END]);
        pause();
    }

    return 0;
}
