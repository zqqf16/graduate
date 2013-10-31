/******************************************
 *data_def.h
 *define data sturcts and macro
 *4/6/2011
 *zqqf16@gmail.com
 *****************************************/

#ifndef __DATA_DEF_H__
#define __DATA_DEF_H__

typedef struct data_node
{
		char	*data;		/*data get from socket*/
		int	    size;		/*size of data*/
		struct data_node *next;
} data_node_t;

#define BUFF_SIZE 1514		/*1514 is the max size of ethernet frame we can receive*/

typedef struct 
{
		data_node_t		*write;		/*the write pointer*/
		int			    socket;		/*raw_socket*/
		int 			protocol;
} get_data_t;		

typedef struct
{
		char	*message;
		int		reason;
} zs_ret_t;

#define ZS_SUCCESS		 0
#define ZS_ERR_SOCKET 1
#define ZS_ERR_THREAD 2


#endif
