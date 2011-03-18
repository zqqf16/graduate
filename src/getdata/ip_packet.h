#ifndef _IP_PACKET_H_
#define _IP_PACKET_H_

#include<sys/tpyes.h>

typedef struct
{
		u_int8_t 	version;	/*low 4 bits are useful, highters are 0*/
		/*head_len some times more than 5, to make it sample, I ignore it */
		u_int8_t 	head_len;	/*low 4 bits are useful, highters are 0*/
		u_int8_t 	tos;		
		u_int16_t 	total_len;
		u_int16_t	id;
		u_int8_t	flag;		/*low 3 bits are useful, highters are 0*/
		u_int16_t	offset;		/*low 13 bits are useful, highters are 0*/
		u_int8_t	ttl;		
		u_int8_t 	protocol;	/*not all protocols are supportted, just some well-known*/
		u_int16_t	head_sum;
		u_int8_t 	src[4];
		u_int8_t 	dest[4];
		void			*data;
} ip_packet;

#endif
