#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <time.h>
#include <pthread.h>    //strlen
#include <assert.h>

#define SERVER_PORT 1256
#define QUEUE_SIZE 5
#define SERVER_SIZE 3

/*
- brak aktywnego czekania
- brak zmiennych lokalnych przekazywanyhc jako wskazniki do funkcji socketowych
( albo zmienna globalna albo mallaoc -> free ) 

*/
struct socket_msq{
    int socket;
    char message[2000];
};


int n=256;
int client_socket = -1;
int sockets[SERVER_SIZE];
int sockets_avability_mask[SERVER_SIZE];  // 0 - covered , 1 - open
//struct socket_msq sockets;
pthread_mutex_t example_mutex = PTHREAD_MUTEX_INITIALIZER;




void init(){
		int i = 0;
		for(i = 0; i < SERVER_SIZE; i++){
			sockets_avability_mask[i] = 1;
		}
}

int get_socket_index(){
		int i = 0;
		int open_socket_index = -1;
		//printf("start looking for open socekt \n");	
			for(i = 0; i < SERVER_SIZE; i++){
				if(sockets_avability_mask[i] == 1){
					open_socket_index = i;
					break;
				}	
			}
		printf("found open socket index %d \n", open_socket_index);		
		return open_socket_index;			
}

// commands 

void sendServerCallback(int mySocket){
	printf("want to sended callback to socket with id %d \n",mySocket );

	send(mySocket, "Connected\n",11, 0);
}

void sendServerConnectionStatus(){
	int i = 0;
	printf(" \n printing all socket status \n");
	for(i = 0; i < SERVER_SIZE; i++){
		printf("index %d   socket_value %d   avability %d \n",i,sockets[i],sockets_avability_mask[i]);
	}
	printf("\nwant to send server status to client  with id %d \n", client_socket);
	if(client_socket != -1){
		char msg[64] = "status-";
		
		char id[2] ;
		id[1] = 0;
				for(i = 0; i < SERVER_SIZE; i++){
					if(sockets_avability_mask[i] == 0 && sockets[i] != client_socket){
						id[0] = sockets[i] +'0';
						strcat(msg,id);
						strcat(msg,"-");
					}	
				}
		strcat(msg,"\n");
		printf("server status %s \n", msg);
		send(client_socket, msg,64, 0);
	}else{
		printf("error no client found \n");	
	}
}


void log_out(int socket_id){
	int i = 0;
	printf("want to logout agent with id  %d \n",socket_id);
			for(i = 0; i < SERVER_SIZE; i++){
				if(sockets[i] ==  socket_id){
					sockets_avability_mask[i] = 1;
					send(socket_id, "kill\n",8, 0);
					break;
				}	
			}

}

void execute_command(char** messages,int socket_id){
	printf("want to execute command \n" );
	if(!strcmp(messages[0],"client")){
		printf("recognized client \n");
		if(!strcmp(messages[1],"kill")){
			printf("want to shut down\n" );
			int id_to_kill = atoi(messages[2]);
			log_out(id_to_kill);
			sendServerConnectionStatus();
		}else if(!strcmp(messages[1],"registrate")){
			printf("want to registrate client with id %d \n",socket_id );
			client_socket  = socket_id;
		}else{
			printf("command %s is not recognized for client \n",messages[1] );
		}
	}else if(!strcmp(messages[0],"agent")){
		printf("agent" );	
	}else{
		printf("command is not recognized \n" );
	} 

}

char** str_split(char* a_str, const char a_delim)
{
    char** result    = 0;
    size_t count     = 0;
    char* tmp        = a_str;
    char* last_comma = 0;
    char delim[2];
    delim[0] = a_delim;
    delim[1] = 0;

    while (*tmp)
    {
        if (a_delim == *tmp)
        {
            count++;
            last_comma = tmp;
        }
        tmp++;
    }

    count += last_comma < (a_str + strlen(a_str) - 1);

    count++;

    result = malloc(sizeof(char*) * count);

    if (result)
    {
        size_t idx  = 0;
        char* token = strtok(a_str, delim);

        while (token)
        {
            assert(idx < count);
            *(result + idx++) = strdup(token);
            token = strtok(0, delim);
        }
        assert(idx == count - 1);
        *(result + idx) = 0;
    }

    return result;
}


void* odbieranie (void* structure){
	struct socket_msq *message_wraper = (struct socket_msq*)structure;
	char buffer[2000];
    char** messages;

		int read_size  = 0;
	   while(1)
	    {
		bzero(buffer,2000);
		if( (read_size = read(message_wraper->socket , buffer , 2000)) > 0){
			printf("recived raw msg from socket with id %d msg is %s \n", message_wraper->socket, buffer);
			messages = str_split(buffer,'-');
			pthread_mutex_lock(&example_mutex);	
			execute_command(messages,message_wraper->socket);
			pthread_mutex_unlock(&example_mutex);
		}
	    }
			
	int r=1;
	printf("koniec\n");
	pthread_exit(&r);


}



int main(int argc, char* argv[])
{
   int nSocket;
   int nBind, nListen;
   int nFoo = 1;
   int open_socket_index = -1;
   socklen_t nTmp;
   struct sockaddr_in stAddr, stClientAddr;
 
	pthread_t handle[SERVER_SIZE];

	printf("inicjalizuje...");
	init();
   /* address structure */
   memset(&stAddr, 0, sizeof(struct sockaddr));
   stAddr.sin_family = AF_INET;
   stAddr.sin_addr.s_addr = htonl(INADDR_ANY);
   stAddr.sin_port = htons(SERVER_PORT);

   /* create a socket */
   nSocket = socket(AF_INET, SOCK_STREAM, 0);	
   if (nSocket < 0)
   {
       fprintf(stderr, "%s: Can't create a socket.\n", argv[0]);
       exit(1);
   }
   setsockopt(nSocket, SOL_SOCKET, SO_REUSEADDR, (char*)&nFoo, sizeof(nFoo));

   /* bind a name to a socket */
   nBind = bind(nSocket, (struct sockaddr*)&stAddr, sizeof(struct sockaddr));
   if (nBind < 0)
   {
       fprintf(stderr, "%s: Can't bind a name to a socket.\n", argv[0]);
       exit(1);
   }
   /* specify queue size */
   nListen = listen(nSocket, QUEUE_SIZE);
   if (nListen < 0)
   {
       fprintf(stderr, "%s: Can't set queue size.\n", argv[0]);
   }
	
   while(1)
   {
	printf("start while loop \n" );
   		open_socket_index = get_socket_index() ;
       /* block for connection request */
	 	if(open_socket_index != -1){
		    nTmp = sizeof(struct sockaddr);
		    sockets[open_socket_index] = accept(nSocket, (struct sockaddr*)&stClientAddr, &nTmp);
		    if (sockets[open_socket_index] > 0)
		       {		         
			int mySocket = sockets[open_socket_index];
			printf("new client with id: %d\n", mySocket);
			printf("%s: [connection from %s]\n",
			argv[0], inet_ntoa((struct in_addr)stClientAddr.sin_addr));
			sockets_avability_mask[open_socket_index] = 0;
			pthread_create(&handle[open_socket_index], NULL, odbieranie, &mySocket);
			sendServerCallback(mySocket);
			sendServerConnectionStatus();
			}else{
			 fprintf(stderr, "%s: Can't create a connection's socket.\n", argv[0]);
			}
	       }
	}
       

   close(nSocket);
   return(0);
}