/******************************************
 *env.h
 *define the environment
 *4/6/2011
 *zqqf16@gmail.com
 ******************************************/

#ifndef __ENV_H__
#define __ENV_H__

#include <pthread.h>
#include "data_def.h"

extern data_node_t *head;			/* the head of data link */

extern pthread_t  thread_get;		/* this thread gets datas from socket */

extern zs_ret_t *ret;				/* return data */

extern get_data_t *args;			/* parmers of get_data() */

#endif
