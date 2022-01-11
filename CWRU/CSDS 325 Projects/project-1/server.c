/*--------------------------------------------------------------------*/
/* conference server */

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
#define max_clients 128

extern char *recvdata(int sd);
extern int   senddata(int sd, char *msg);
extern int   startserver();
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/* main function*/
int main(int argc, char *argv[])
{
  int    serversock;    /* server socket*/

  fd_set liveskset;   /* set of live client sockets */
  int    liveskmax;   /* maximum socket */
  int   client_socket[max_clients]; /* save the detail of client socket */
  /* check usage */
  if (argc != 1) {
    fprintf(stderr, "usage : %s\n", argv[0]);
    exit(1);
  }

  /* get ready to receive requests */
  serversock = startserver();
  if (serversock == -1) {
    exit(1);
  }
  for (int i = 0; i < max_clients; i++)   {
    client_socket[i] = 0;
  }

  while (1) {
    int itsock;      /* loop variable */
    /*
    TODO:
    init the live client set
    */
    /* receive and process requests */
    FD_ZERO(&liveskset);
    FD_SET(serversock, &liveskset);
    liveskmax = serversock;
    //we need to set client socket into liveskset
    for (int i=0;i<max_clients;i++){
      itsock = client_socket[i];
      if(itsock>0)
        FD_SET(itsock,&liveskset);
      if(itsock>liveskmax)
        liveskmax = itsock; /* we need a good liveskmax to work in select() */
    }
    /*
    TODO:
    using select() to serve both live and new clients
    */
    if (select(liveskmax+1,&liveskset,NULL,NULL,NULL) == -1){
      perror("select initilization error!");
      exit(4);
    }
    /* process messages from clients */
    for (int j=0; j < liveskmax; j++) {
      itsock=client_socket[j];
      /* skip the listen socket */
      if (itsock == serversock) continue;
      //if the client socket is evoked, receive message
      if (FD_ISSET(itsock,&liveskset)) {
        char *  clienthost;  /* host name of the client */
        ushort  clientport;  /* port number of the client */
        /*
        TODO:
        obtain client's host name and port
        using getpeername() and gethostbyaddr()
        */
        struct sockaddr_in cli_addr;
        int cli_addr_len=sizeof(cli_addr);
        int s=getpeername(itsock, &cli_addr, &cli_addr_len);
        if (s!=0){
          perror("getpeername");
          exit(1);
        }
        clientport=ntohs(cli_addr.sin_port); /* get client port number */
        struct hostent *host=gethostbyaddr((char *) &cli_addr.sin_addr,sizeof(cli_addr.sin_addr),AF_INET);
        if(host==NULL){
          perror("gethostbyaddr");
          exit(1);
        }
        clienthost=host->h_name; /* get client host name */
        /* read the message */
        char *msg = recvdata(itsock);
        if (!msg) {
          /* disconnect from client */
          printf("admin: disconnect from '%s(%hu)'\n", clienthost, clientport);

          /*
          TODO:
          remove this client from 'liveskset'
          */
          FD_CLR(itsock,&liveskset);
          client_socket[j] = 0;
          close(itsock);
        } else {
          /*
          TODO:
          send the message to other clients
          */
          int sock;
          for (int m=0; m < liveskmax; m++){
            sock=client_socket[m];
            if (sock == serversock) continue; /* we don't need to send message to server socket */
            if (sock == itsock) continue; /* we don't need to send message to that client socket */
            if (sock!=0)
              senddata(sock, msg);
          }
          /* print the message */
          printf("%s(%hu): %s", clienthost, clientport, msg);
          free(msg);
        }
      }
    }
    //if serversock is evoked, we need to accept a new connection
    if (FD_ISSET(serversock,&liveskset)) {

      /*
      TODO:
      accept a new connection request
      */
      struct sockaddr_in cli_addr;
      socklen_t clilen = sizeof(cli_addr); // Address struct length
      int new = accept(serversock, (struct sockaddr *) &cli_addr, &clilen);
      if (!(new < 0)) {
        char *  clienthost;  /* host name of the client */
        ushort  clientport;  /* port number of the client */

        /*
        TODO:
        get client's host name and port using gethostbyaddr()
        */

        struct hostent *host=gethostbyaddr((char *) &cli_addr.sin_addr,sizeof(cli_addr.sin_addr),AF_INET);
        if(host==NULL){
          perror("gethostbyaddr");
          exit(1);
        }
        clienthost=host->h_name;
        clientport=ntohs(cli_addr.sin_port);
        /* read the message */
        printf("admin: connect from '%s' at '%hu'\n",clienthost, clientport);

        /*
        TODO:
        add this client to 'liveskset'
        */
        FD_SET(new,&liveskset);
        for (int i = 0; i <=max_clients; i++) {
          //if position is empty, put it
          if( client_socket[i] == 0 ){
            client_socket[i] = new;
            break;
          }
          //if can't find a empty position, error
          if(i==max_clients-1)
            perror("max clients!");
        }
      } else {
        perror("accept");
        exit(0);
      }
    }
  }
}
/*--------------------------------------------------------------------*/
