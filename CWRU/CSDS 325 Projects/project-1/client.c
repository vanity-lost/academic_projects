/*--------------------------------------------------------------------*/
/* conference client */

#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <time.h>
#include <errno.h>

#define MAXMSGLEN  1024

extern char *  recvdata(int sd);
extern int     senddata(int sd, char *msg);

extern int     connecttoserver(char *servhost, ushort servport);
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
int main(int argc, char *argv[])
{
  int  sock;

  /* check usage */
  if (argc != 3) {
    fprintf(stderr, "usage : %s <servhost> <servport>\n", argv[0]);
    exit(1);
  }

  /* connect to the server */
  sock = connecttoserver(argv[1], atoi(argv[2]));
  if (sock == -1)
    exit(1);

  fd_set readfds;
  int STDIN;
  while (1) {
    FD_ZERO(&readfds);
    FD_SET(STDIN, &readfds); //the input
    FD_SET(sock, &readfds); //the socket
    if (select(sock+1, &readfds, NULL, NULL, NULL)==-1){
      perror("select initilization error!");
      exit(4);
    }
    /*
    TODO:
    use select() to watch for user inputs and messages from the server
    */
    if (FD_ISSET(sock, &readfds)) {
      char *msg;
      msg = recvdata(sock);
      if (!msg) {
        /* server died, exit */
        fprintf(stderr, "error: server died\n");
        exit(1);
      }
      /* print the message */
      printf(">>> %s", msg);
      free(msg);
    }

    if (FD_ISSET(STDIN, &readfds)) {
      char      msg[MAXMSGLEN];
      if (!fgets(msg, MAXMSGLEN, stdin))
        exit(0);
      senddata(sock, msg);
    }
  }
}
/*--------------------------------------------------------------------*/
