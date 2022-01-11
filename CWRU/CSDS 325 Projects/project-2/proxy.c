#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <time.h>
#include <errno.h>

#include "utils.h"

extern int     sendrequest(int sd);
extern char *  readresponse(int sd);
extern void    forwardresponse(int sd, char *msg);
extern int     startserver();

main(int argc, char *argv[])
{
  int    servsock;    /* server socket descriptor */

  fd_set livesdset, servsdset;   /* set of live client sockets and set of live http server sockets */
  int livesdmax;  /* define largest file descriptor number used for select */
  struct pair * table = malloc(sizeof(struct pair)); /* table to keep client<->server pairs */

  char *msg;

  /* check usage */
  if (argc != 1) {
    fprintf(stderr, "usage : %s\n", argv[0]);
    exit(1);
  }

  /* get ready to receive requests */
  servsock = startserver();
  if (servsock == -1) {
    exit(1);
  }

  table->next = NULL;

  /* initialize all the fd_sets and largest fd numbers */
  FD_ZERO(&livesdset);  //clear livesdset
  FD_SET(servsock, &livesdset); //put servsock into livesdset
  livesdmax = servsock;

  while (1) {
    int frsock;

    /*  combine livesdset and servsdset
    * use the combined fd_set for select */
    fd_set currset; //define currset
    FD_ZERO(&currset);  //clear currset
    for (frsock = 3; frsock <= livesdmax; frsock++) { // combine livesdset and servsdset
        if (FD_ISSET(frsock, &livesdset) || FD_ISSET(frsock, &servsdset)) {
            FD_SET(frsock, &currset);
        }
    }

    if(select(livesdmax+1,&currset,NULL,NULL,NULL) == -1) {  // select form the combined currset
      fprintf(stderr, "Can't select.\n");// check the error for selection
      continue;
    }

    for (frsock = 3; frsock <= livesdmax; frsock++) { // iterate over file descriptors
      if (frsock == servsock) continue; //skip the sever

      if(FD_ISSET(frsock,&currset)&&FD_ISSET(frsock,&livesdset)) { //if there's a input from existing client
        /* forward the request */
        int newsd = sendrequest(frsock);
        if (!newsd) {
          printf("admin: disconnect from client\n");
          /* clear frsock from fd_set(s) */
          FD_CLR(frsock,&livesdset);
        } else {
          insertpair(table, newsd, frsock);
          /* : insert newsd into fd_set(s) */
          FD_SET(newsd,&servsdset);// put newsd into servsdset
          if (newsd > livesdmax)// refresh the largest number if necessary
              livesdmax = newsd;
        }
      }
      if(FD_ISSET(frsock,&currset)&&FD_ISSET(frsock,&servsdset)) { /* input from the http server? */
        char *msg;
        struct pair *entry=NULL;
        struct pair *delentry;
        msg = readresponse(frsock);
        if (!msg) {
          fprintf(stderr, "error: server died\n");
          exit(1);
        }

        /* forward response to client */
        entry = searchpair(table, frsock);
        if(!entry) {
          fprintf(stderr, "error: could not find matching clent sd\n");
          exit(1);
        }

        forwardresponse(entry->clientsd, msg);
        delentry = deletepair(table, entry->serversd);

        /* clear the client and server sockets used for
        * this http connection from the fd_set(s) */
        free(msg);
        FD_CLR(entry->clientsd, &livesdset);// clear the client socket
        FD_CLR(frsock,&servsdset);//clear the server socket
      }
    }

    /* input from new client*/
    if(FD_ISSET(servsock, &currset)) {
      struct sockaddr_in caddr;
      socklen_t clen = sizeof(caddr);
      int csd = accept(servsock, (struct sockaddr*)&caddr, &clen);

      if (csd != -1) {
        /* put csd into fd_set(s) */
        FD_SET(csd,&livesdset);// put csd into livesdset
        if (csd > livesdmax)// refresh the largest number if necessary
            livesdmax = csd;
      } else {
        perror("accept");
        exit(0);
      }
    }
  }
}
