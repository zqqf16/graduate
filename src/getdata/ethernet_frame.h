#ifndef _ETHERNET_FRAME_H_
#define _ETHERNET_FRAME_H_

#define TYPE_IP 	0x0800
#define TYPE_ARP	0x0806
#define TYPE_FLAG 	0x0600		/*when type >= 0x0600, it's protocol type, else it's data size*/

typedef struct
{
		unsigned char dest[6];	/*destination mac*/
		unsigned char src[6];	/*source mac*/
		unsigned char type;		/*see TYPE_FLAG*/
		void *data;				/*point to data struct(arp/ip)*/
} Eth_frame;
