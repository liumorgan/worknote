#include <stdio.h>  
#include <stdlib.h>  
#include <unistd.h>  
#include <string.h>  
#include <sys/types.h>  
#include <sys/socket.h>  
#include <netinet/in.h>  
#include <netdb.h>   

void error(const char *msg)  
{  
	perror(msg); 
	fprintf(stdout,"%s",msg);
	exit(0);  
}  

int main(int argc, char *argv[])  
{  
	int sockfd, portno, n;  
	struct sockaddr_in serv_addr;  
	struct hostent *server;  

	char buffer[256];  
	if (argc < 4) {  
		fprintf(stdout,"usage %s hostname port command\n", argv[0]);  
		exit(0);  
	}  
	portno = atoi(argv[2]);  
	sockfd = socket(AF_INET, SOCK_STREAM, 0);  
	if (sockfd < 0)   
		error("ERROR opening socket");  
	server = gethostbyname(argv[1]);  
	if (server == NULL) {  
		fprintf(stdout,"ERROR, no such host\n");  
		exit(0);  
	}  

	bzero(buffer,256);  
	strncpy(buffer,argv[3],sizeof(buffer));

	bzero((char *) &serv_addr, sizeof(serv_addr));  
	serv_addr.sin_family = AF_INET;  
	bcopy((char *)server->h_addr,   
		(char *)&serv_addr.sin_addr.s_addr,  
		server->h_length);  
	serv_addr.sin_port = htons(portno);  
	if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0)   
		error("ERROR connecting");  

	n = write(sockfd,buffer,strlen(buffer));  

	bzero(buffer,256);  
	n = read(sockfd,buffer,sizeof(buffer));  
	if (n < 0)   
		error("ERROR reading from socket");  
	printf("%s",buffer);  
	close(sockfd);  
	return 0;  
}  
