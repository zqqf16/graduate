#ifndef _IP_PACKET_H_
#define _IP_PACKET_H_

typedef struct
{
		unsigned char 	version;	/*low 4 bits are useful, highters are 0*/
		/*head_len some times more than 5, to make it sample, I ignore it */
		unsigned char 	head_len;	/*low 4 bits are useful, highters are 0*/
		unsigned char 	tos;		
		unsigned short 	total_len;
		unsigned short	id;
		unsigned char	flag;		/*low 3 bits are useful, highters are 0*/
		unsigned short	offset;		/*low 13 bits are useful, highters are 0*/
		unsigned char	ttl;		
		unsigned char 	protocol;	/*not all protocols are supportted, just some well-known*/
		unsigned short	head_sum;
		unsigned char 	src[4];
		unsigned char 	dest[4];
		void			*data;
} ip_packet;

#endif
