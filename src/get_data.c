/******************************************
 *get_data.c
 *get data from socket
 *4/6/2011
 *zqqf16@gmail.com
 *****************************************/
 
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "env.h"
#include "data_def.h"
#include "get_data.h"
 
/*****************************************
 *get_data function
 *get data from socket
 *4/6/2011
 ****************************************/
void get_data(void *arg)
{
	   pthread_detach(pthread_self()); /*线程分离*/
	   data_node_t *tmp;
       int     read_size;
       char    buffer[BUFF_SIZE];
	   int     sock = ((get_data_t*)arg)->socket;
	   data_node_t *write = ((get_data_t*)arg)->write;
	   while(1)
	   {
		       read_size = recvfrom(sock, buffer, BUFF_SIZE, 0, NULL, NULL);
			   if(read_size < 1)
					   continue;
//			   pthread_setcancelstate(PTHREAD_CANCEL_DISABLE,NULL);/*线程不可取消*/
			   tmp = malloc(sizeof(data_node_t));
			   tmp->next = NULL;
			   tmp->size = read_size;
			   tmp->data = malloc(read_size);
			   memcpy(tmp->data, buffer, read_size);
			   if(write == NULL)
			   {
					   head = tmp;
					   write = head;
					   printf("Head\n");
			   }
			   else
			   {
					   write->next = tmp;
			   		   write = write->next;
					   printf("Node\n");
			   }
			   printf("%.2X%.2X\n", write->data[12]&0xFF,write->data[13]&0XFF);
//			   pthread_setcancelstate(PTHREAD_CANCEL_ENABLE,NULL);
		}
}
    
