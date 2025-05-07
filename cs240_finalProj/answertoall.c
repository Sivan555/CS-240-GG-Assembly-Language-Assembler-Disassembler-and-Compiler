#include <stdio.h>

void main(){

   int val = 0;
   int ans = 42;   
   printf("What is the Answer to life?");
   scanf("%d", &val);
   if( val == ans){
      printf("Right!\n");
   }else{
      printf("Wrong!\n");
   }

}