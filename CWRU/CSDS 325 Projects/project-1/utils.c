/*--------------------------------------------------------------------*/
/* functions to connect clients and server */

#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <time.h>
#include <errno.h>

#define MAXNAMELEN 256
/*--------------------------------------------------------------------*/


/*----------------------------------------------------------------*/
int startserver()
{
  int     sd;        /* socket */

  char *  serverhost[MAXNAMELEN];  /* hostname */
  ushort  serverport;  /* server port */

  /*
  TODO:
  create a TCP socket
  */
  sd = socket(AF_INET, SOCK_STREAM, 0);
  if (sd < 0)
    error("ERROR opening socket");
  struct sockaddr_in serv_addr; // Server address struct
  bzero((char *) &serv_addr, sizeof(serv_addr));
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_addr.s_addr = INADDR_ANY;
  serv_addr.sin_port = htons(0);
  /*
  TODO:
  bind the socket to some random port, chosen by the system
  */
  if (bind(sd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
    error("ERROR on binding");

  /* ready to receive connections */
  listen(sd, 128);

  /*
  TODO:
  obtain the full local host name (serverhost)
  use gethostname() and gethostbyname()
  */
  gethostname(serverhost,sizeof(serverhost));
  if (serverhost == -1) {
    perror("gethostname");
    exit(1);
  } 
  /*
  TODO:
  get the port assigned to this server (serverport)
  use getsockname()
  */
  struct sockaddr_in sin;
  socklen_t len = sizeof(sin);
  if (getsockname(sd, (struct sockaddr *)&sin, &len) == -1)
    perror("getsockname");
  else
    serverport =ntohs(sin.sin_port);
  /* ready to accept requests */
  printf("admin: started server on '%s' at '%hu'\n", serverhost, serverport);
  return(sd);
}
/*----------------------------------------------------------------*/

/*----------------------------------------------------------------*/
/*
establishes connection with the server
*/
int connecttoserver(char *serverhost, ushort serverport)
{
  int     sd;          /* socket */

  ushort  clientport;  /* port assigned to this client */

  /*
  TODO:
  create a TCP socket
  */

  /*
  TODO:
  connect to the server on 'serverhost' at 'serverport'
  use gethostbyname() and connect()
  */

  /*
  TODO:
  get the port assigned to this client
  use getsockname()
  */
  sd = socket(AF_INET, SOCK_STREAM, 0);
  if (sd < 0)
    error("ERROR opening socket");

  // Set up for connect()
  struct hostent *server;
  server = gethostbyname(serverhost);
  if (server == NULL) {
    fprintf(stderr,"ERROR, no such host\n");
    exit(0);
  }
  struct sockaddr_in serv_addr;
  bzero((char *) &serv_addr, sizeof(serv_addr));
  serv_addr.sin_family = AF_INET;
  bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
  serv_addr.sin_port = htons(serverport);
  // Make connection
  if (connect(sd,(struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
    error("ERROR connecting");
  struct sockaddr_in sin;
  socklen_t len = sizeof(sin);
  if (getsockname(sd, (struct sockaddr *)&sin, &len) == -1)
    perror("getsockname");
  else
    clientport =ntohs(sin.sin_port);
  /* succesful. return socket */
  printf("admin: connected to server on '%s' at '%hu' thru '%hu'\n", serverhost, serverport, clientport);
  return(sd);
}
/*----------------------------------------------------------------*/


/*----------------------------------------------------------------*/
int readn(int sd, char *buf, int n)
{
  int     toberead;
  char *  ptr;

  toberead = n;
  ptr = buf;
  while (toberead > 0) {
    int byteread;

    byteread = read(sd, ptr, toberead);
    if (byteread <= 0) {
      if (byteread == -1)
      perror("read");
      return(0);
    }

    toberead -= byteread;
    ptr += byteread;
  }
  return(1);
}

char *recvdata(int sd)
{
  char *msg;
  long  len;

  /* get the message length */
  if (!readn(sd, (char *) &len, sizeof(len))) {
    return(NULL);
  }
  len = ntohl(len);

  /* allocate memory for message */
  msg = NULL;
  if (len > 0) {
    msg = (char *) malloc(len);
  if (!msg) {
    fprintf(stderr, "error : unable to malloc\n");
    return(NULL);
  }

    /* read the message */
  if (!readn(sd, msg, len)) {
    free(msg);
    return(NULL);
  }
}

  return(msg);
}

int senddata(int sd, char *msg)
{
  long len;

  /* write lent */
  len = (msg ? strlen(msg) + 1 : 0);
  len = htonl(len);
  write(sd, (char *) &len, sizeof(len));

  /* write message data */
  len = ntohl(len);
  if (len > 0)
    write(sd, msg, len);
  return(1);
}
/*----------------------------------------------------------------*/
