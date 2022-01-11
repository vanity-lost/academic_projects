#include <stdio.h>

struct pair
{
  int clientsd;
  int serversd;
  struct pair * next;
};

struct pair *searchpair(struct pair *head, int serversd);
int insertpair(struct pair * head, int serversd, int clientsd);
struct pair *deletepair(struct pair *head, int serversd);

