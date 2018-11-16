#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <arpa/inet.h>


int main(int argc, char** argv)
{
    int sockfd,new_fd;
    struct sockaddr_in my_addr;
    struct sockaddr_in their_addr;
    int sin_size;
    int lport = 0;
	
	if(argc <= 1)
	{
		printf("please set port number\n");
		exit(-1);
	}
	
	lport = atoi(argv[1]);
	if(lport <= 1024)
	{
		printf("please set port number > 1024 \n");
		exit(-2);
	}
	
    if((sockfd = socket(AF_INET,SOCK_STREAM,0))==-1)
    {
        printf("create socket error");
        perror("socket");
        exit(1);
    }
    
    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(lport);
    my_addr.sin_addr.s_addr = INADDR_ANY;
    //bzero(&(my_addr.sin_zero),8);
    
    if(bind(sockfd,(struct sockaddr *)&my_addr,sizeof(struct sockaddr))==-1)
    {
        perror("bind socket error");
        exit(1);
    }
    
    if(listen(sockfd,10)==-1)
    {
        perror("listen");
        exit(1);
    }
    
    while(1)
    {
        sin_size = sizeof(struct sockaddr);
        
        if((new_fd = accept(sockfd,(struct sockaddr *)&their_addr,&sin_size))==-1)
        {
            perror("accept");
            exit(1);
        }
       
	
		char buff[256];
		char buff2[256];
		memset(buff,0,256);
		
		struct sockaddr_in sa;
		int len = sizeof(sa);
		if(!getpeername(new_fd, (struct sockaddr *)&sa, &len))
		{
			printf( "peer ip  :%s ", inet_ntoa(sa.sin_addr));
			strcpy(buff,inet_ntoa(sa.sin_addr) );
			printf( "peer port:%d ", ntohs(sa.sin_port));
		}
		
		printf("accept connection from %s\n", buff);
		
		if(recv(new_fd,buff2,strlen(buff2),0)==-1)
			perror("recv");  


		if(send(new_fd,buff,strlen(buff),0)==-1)
			perror("send");            
		
        close(new_fd);
    }
    
    close(sockfd);
}