# SafeChatting
Program uses RSA to encrypt/decrypt messages            
The public and secret keys are generated when the client tries to connect to the server, then the client sends public key to the server.       
Server or user encrypt the message using public key of the receiver.       
Every user doesn't share his secret key, which makes chatting safe.          
              
To start a server enter 'python server.py'         ![Знімок екрана 2022-04-28 о 11 19 01](https://user-images.githubusercontent.com/92575094/165709495-cfb3fb09-0ce0-4085-8de8-ba359a6c25c8.png)
           
To start client.py write 'python client.py {username}'in the terminal:         ![Знімок екрана 2022-04-28 о 11 06 22](https://user-images.githubusercontent.com/92575094/165708585-29b60a85-653f-4cfe-9283-a4f568e8abd8.png)

Here's the example of usage:                    
           

![Знімок екрана 2022-04-28 о 11 12 33](https://user-images.githubusercontent.com/92575094/165709108-8c607399-1dd6-48ab-b0c0-4049d71882dc.png)



        
As seen on the picture, user can enter '|' sign to indicate receivers - can be one person or more                    
If there is no '|' sign, then the message is sent to everyone.           
         

If username is wrong, user can resend a message:       ![Знімок екрана 2022-04-28 о 11 14 11](https://user-images.githubusercontent.com/92575094/165709078-c12fe355-6781-4ac5-b5b1-9447463f361b.png)
