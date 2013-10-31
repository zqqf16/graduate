/*****************************************
 *contorl.c
 *multi-thread, signal, socket, env
 *4/6/2011
 *zqqf16@gmail.com
 ****************************************/
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/socket.h>
#include <linux/if_ether.h>
#include <string.h>
#include <signal.h>
#include <errno.h>

#include "env.h"
#include "data_def.h"
#include "get_data.h"
#include "interface.h"

/*
 *zs_ret_t* zs_init(void)
 *init the global variables
 */
zs_ret_t* zs_init(void)
{

		ret = malloc(sizeof(zs_ret_t));
		ret->message = NULL;
		ret->reason = ZS_SUCCESS;
		
		args = malloc(sizeof(get_data_t));
		args->write = head; 
		args->protocol = ETH_P_ALL; /*all protocols*/
			
		if((args->socket = socket(PF_PACKET, SOCK_RAW, htons(args->protocol))) < 0)
		{
				ret->message = "Socket create error";
				ret->reason = ZS_ERR_SOCKET;
		}
		return ret;
}

/*
 *zs_start()
 *create a new thread to get data
 */
zs_ret_t* zs_start(void)
{
		ret->message = NULL;
		ret->reason = ZS_SUCCESS;
		int flag = pthread_create(&thread_get, NULL, (void*)get_data, (void*)args);
		if(flag !=0)
		{
		        ret->message = "Thread create error";
		        ret->reason = ZS_ERR_THREAD;
		}

		return ret;

}
/*stop getting data*/
void zs_stop(void)
{
		pthread_cancel(thread_get);
}

/*clean args and head*/
void zs_clean(void)
{
		if(ret != NULL)
		{
			free(ret);
		}
        if(args != NULL)
        {
            free(args);
        } 
        data_node_t *tmp;
        while(head != NULL)
        {
            tmp = head->next;
            if(head->data != NULL)
            {
                free(head->data);
            }
            free(head);
            head = tmp;
        }
        args = NULL;
        head = NULL;
}
