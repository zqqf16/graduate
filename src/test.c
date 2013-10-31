#include "interface.h"
#include <stdio.h>
int main()
{
		zs_ret_t *ret;
		ret=zs_init();
		printf("---%d---\n", ret->reason);
		ret=zs_start();
			printf("---%d---\n", ret->reason);

		sleep(6);
		zs_stop();
		printf("stoped\n");
        zs_clean();
        printf("clean\n");
		return 0;
}
