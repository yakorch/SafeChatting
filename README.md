# SafeChatting
Program uses RSA to encrypt/decrypt messages            
The public and secret keys are generated when the client tries to connect to the server, then the client sends public key to the server.       
Server or user encrypt the message using public key of the receiver.       
Every user doesn't share his secret key, which makes chatting safe.          
                   
                     
Required to have all the modules in the same directory:   ![Знімок екрана 2022-04-28 о 11 25 06](https://user-images.githubusercontent.com/92575094/165710531-e2256757-914b-4e5c-9ce4-3bb7aedc7ba6.png)           
                  

To start a server enter 'python server.py'         ![Знімок екрана 2022-04-28 о 11 19 01](https://user-images.githubusercontent.com/92575094/165709495-cfb3fb09-0ce0-4085-8de8-ba359a6c25c8.png)
           
To start client.py write 'python client.py {username}'in the terminal:         ![image](https://user-images.githubusercontent.com/91615532/165799309-25e403c3-9582-4503-8098-99ba9042a542.png)


Here's the example of usage:                    
           

![Знімок екрана 2022-04-28 о 19 20 05](https://user-images.githubusercontent.com/92575094/165799077-802da97d-7d44-458d-a439-209abf6cde0b.png)



        
As seen on the picture, user can enter '|' sign to indicate receivers - can be one person or more                    
If there is no '|' sign, then the message is sent to everyone.           
         

If username is wrong, user can resend a message:       ![Знімок екрана 2022-04-28 о 11 14 11](https://user-images.githubusercontent.com/92575094/165709078-c12fe355-6781-4ac5-b5b1-9447463f361b.png)            


Allowed characters are ascii symbols in range from 32 to 122 inclusively            
      

Message integrity implemented, the message with warning about error in sending the message can be printed.     
