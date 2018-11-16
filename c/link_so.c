#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int link_find(char *str)
{
   FILE *fp;
   char fl[1024]="ldd ";
   int len,i,n;
   char bufcode[1024];
   char buf[1024];
   int j=0;
   int k=0;

   strcat(fl,str);
   fp=popen(fl,"r");
   len=sizeof(buf);
   fread(buf,1,len,fp);
   
   for(i=0;i<=len;i++)
   {
      if(buf[i]=='/' && j==0)
      {
          j=i;
      }
      if(buf[i]=='\n' && j!=0)
      {
          for(n=0;n<i-j+1;n++)
          {
              bufcode[k++]=buf[j+n];
          }
          j=0;
      }
      if(i==len)
      {
         printf("%s",bufcode);
         free;
         fclose(fp);
      }
   }
   return 0;
}

int main()
{
   char str[1000]={'0'};
   int i=0;

   printf("please input file path\n");
   do
   {
       scanf("%s",str+i);
       i++;
   }
   while((getchar())!='\n');
   printf("\n");
   printf("link so\n");
   printf("%s\n",str);
   
   link_find(str);
   return 0;
}