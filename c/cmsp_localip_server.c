#include <sys/socket.h>
#include <sys/epoll.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>    

#define MAXLINE		100
#define OPEN_MAX	100
#define LISTENQ		20
#define SERV_PORT	5555
#define INFTIM		1000

int g_daemon = 0;

typedef struct u_data
{
	int fd;
	char* buffer;
}u_data_t;

short g_exit = 0;

int cprintf(char *fmt, ...)
{
	if (!g_daemon)
	{
		va_list argptr;
		int cnt;
		va_start(argptr, fmt);
		cnt = vprintf(fmt, argptr);
		va_end(argptr);
		return(cnt);
	}
}

void setnonblocking(int sock)
{
	int opts;
	opts = fcntl(sock, F_GETFL);

	if(opts < 0) {
		perror("fcntl(sock, GETFL)");
		exit(1);
	}

	opts = opts | O_NONBLOCK;

	if(fcntl(sock, F_SETFL, opts) < 0) {
		perror("fcntl(sock, SETFL, opts)");
		exit(1);
	}
}

void closefd(int epfd,struct epoll_event* ev)
{
	u_data_t* uptr = (u_data_t*)(ev->data.ptr);
	cprintf("closefd %d\n",uptr->fd);

	epoll_ctl(epfd,EPOLL_CTL_DEL,uptr->fd,NULL);  
	close(uptr->fd);
	free(ev->data.ptr);
}


void print_hex(char *buffer, size_t buffer_size, size_t line_width)
{
	size_t j = 0;
	for (j = 0; j < buffer_size; ++ j) 
	{
		char tmp = buffer[j] ;
		printf ("%01x", tmp >> 4 & 0xF);
		printf ("%01x", buffer[j]  & 0xF );
		if ((j + 1) % 2 == 0)
		{
			printf(" ");
		}
		if ((j+1)%line_width == 0) 
		{
			printf("\n");
		}
	}
	printf("\n");
}

int main(int argc, char *argv[])
{
	int i, maxi, listenfd, connfd, sockfd, epfd, nfds;
		
	socklen_t clilen;
	int lport = SERV_PORT;
	
	struct epoll_event ev, events[20];
	int flags;
	int n = 0;
	int ret = 0;

	char ch;  
	while((ch = getopt(argc, argv, "p:d")) != EOF)  
	{  
		switch(ch)  
		{  
		case 'p':  
			{
				lport =  atoi(optarg);
			}
			break;
		case 'd':
			{
				g_daemon = 1;				
			}
			break;
		case '?':
			printf("Unknown option: %c\n",(char)optopt);
			exit(0);
			break;
		default:  
			break;  
		}  
	}  

	if (g_daemon)
	{
		daemon(1,1);
	}

	epfd = epoll_create(256);

	struct sockaddr_in clientaddr;
	struct sockaddr_in serveraddr;

	listenfd = socket(AF_INET, SOCK_STREAM, 0);

	setnonblocking(listenfd);

	ev.data.fd = listenfd;
	ev.events = EPOLLIN | EPOLLET;

	epoll_ctl(epfd, EPOLL_CTL_ADD, listenfd, &ev);

	bzero(&serveraddr, sizeof(serveraddr));
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_port = htons(lport);
	serveraddr.sin_addr.s_addr = INADDR_ANY;

	int reUseOn=0;  
	if(setsockopt(listenfd,SOL_SOCKET,SO_REUSEADDR,&reUseOn,sizeof(int))==-1)  
	{  
		return 3;  
	}  
	
	ret = bind(listenfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr));
	if(ret < 0)
	{
		perror("bind error");
		exit(ret);
	}

	listen(listenfd, LISTENQ);

	maxi = 0;

	while(!g_exit)
	{
		nfds = epoll_wait(epfd, events, 20, 1000);

		for(i = 0; i < nfds && !g_exit; ++i) 
		{
			if(events[i].data.fd == listenfd) 
			{				
				connfd = accept(listenfd, (struct sockaddr *)&clientaddr, &clilen);
				cprintf("accept connection, fd is %d\n", connfd);
				if(connfd < 0) 
				{
					perror("connfd < 0");
					continue;
				}

				setnonblocking(connfd);

				char *str = inet_ntoa(clientaddr.sin_addr);
				cprintf("connect from %s\n", str);
				
				u_data_t* uptr = (u_data_t*)malloc(sizeof(u_data_t));
				uptr->fd = connfd;
				uptr->buffer = (char*)malloc(100);
				ev.data.ptr = uptr;
				ev.events = EPOLLIN  | EPOLLERR | EPOLLHUP;
				epoll_ctl(epfd, EPOLL_CTL_ADD, connfd, &ev);
			}
			else if(events[i].events & EPOLLIN) 
			{
				cprintf("epoll in\n");

				char line[MAXLINE];
				int resp = 0;
				u_data_t* uptr = (u_data_t*)(events[i].data.ptr);
				if((sockfd = uptr->fd) < 0) continue;
				
				n = read(sockfd, line, MAXLINE);
				cprintf("received data: %d \n", n );
				if(n < 0) 
				{
					perror("readline error\n");
					closefd(epfd,events + i);		
					continue;
				} 
				else if(n == 0) 
				{
					closefd(epfd,events + i);
					continue;
				}
				
				cprintf("received data: %s\n", line);
				//print_hex(line,n,16);

				char buff[256];
				memset(buff,0,256);

				if (strncmp(line,"get",3) == 0)
				{
					struct sockaddr_in sa;
					int len = sizeof(sa);
					if(!getpeername(connfd, (struct sockaddr *)&sa, &len))
					{
						cprintf( "peer ip  :%s \n", inet_ntoa(sa.sin_addr));
						strcpy(buff,inet_ntoa(sa.sin_addr) );
						cprintf( "peer port:%d \n", ntohs(sa.sin_port));
					}
					strncpy(uptr->buffer,buff,16);

					resp = 1;
				}
				else if (strncmp(line,"exit",4) == 0)
				{
					g_exit = 1;					
				}
				if (resp)
				{
					ev.data.ptr = uptr;
					ev.events = EPOLLOUT ;
					epoll_ctl(epfd, EPOLL_CTL_MOD, sockfd, &ev);
					cprintf("set mod to out\n");
				}
			}	
			
			else if(events[i].events & EPOLLERR || (events[i].events & EPOLLHUP) )  
			{  
				closefd(epfd,events + i);
				continue;  
				cprintf("epoll error or hup\n");
			}  
			
			else if(events[i].events & EPOLLOUT) 
			{
				cprintf("epoll out\n");
				u_data_t* uptr = (u_data_t*)(events[i].data.ptr);
				if(!uptr)
					continue;
				if((sockfd = uptr->fd) < 0) continue;
				char* data = (char*)(uptr->buffer);
				write(sockfd, data, strlen(data));

				cprintf("written data: %s\n", data);

				ev.data.ptr = uptr;
				ev.events = EPOLLIN  | EPOLLERR | EPOLLHUP;
				epoll_ctl(epfd, EPOLL_CTL_MOD, sockfd, &ev);
				cprintf("set mod to in\n");
			}
		}
	}

	 close(listenfd);  
	 close(epfd);
}