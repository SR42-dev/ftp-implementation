from socket import *
import os
ip_addr="172.20.10.12";
port_num=4497
port_num_conn=4603

def main():
	
	client=socket(AF_INET,SOCK_STREAM)
	
	connected=0
	while True:
		print("Commands Supported:")
		print("CONN: To Connect to the FTP server")
		print("UPLD: To Upload a file to the server")
		print("DWND: To download a file from the server")
		print("DELT: To delete a file at the server directory")
		print("LIST: To List all the files the server directory")
		print("EXIT: To Close the connection and Exit")
		user_inp=input("\nEnter your choice: ")
		if(user_inp=="UPLD" and connected==1):
			client.send("UPLD".encode("utf-8"))
			inp_file=input("Enter file name:")
			if(os.path.exists("./"+inp_file)==True):
				file=open(inp_file,"r")
				data =file.read()
				respp=client.recv(1024).decode("utf-8")
				client.send(inp_file.encode("utf-8"))
				res=client.recv(1024).decode("utf-8")
				print(f"\n[Server]: {res}")
				client.send(data.encode("utf-8"))
				res=client.recv(1024).decode("utf-8")
				print("[Server]: file upload\n")
				file.close()
			else:
				print("[Server]: Please Enter a Valid FileName..\n")
				respp=client.recv(1024).decode("utf-8")
				client.send("NO_FILE_EXISTS_12345".encode("utf-8"))
				res=client.recv(1024).decode("utf-8")
				client.send("NO_DATA_12345".encode("utf-8"))
				res=client.recv(1024).decode("utf-8")
		elif(user_inp=="DWND" and connected==1):
			client.send("DWND".encode("utf-8"))
			client.recv(1024).decode("utf-8")
			down_file=input("Enter filename to download:")
			client.send(down_file.encode("utf-8"))
			res3=client.recv(1024).decode("utf-8")
			client.send("res3 recieved...".encode("utf-8"))
			file_data2=client.recv(1024).decode("utf-8")
			if(file_data2!="NULL_12345"):
				wr_file=open("./downloaded_files/"+down_file,"w")
				wr_file.write(file_data2)
				wr_file.close()
				print("\n[SERVER]: FILE Downloaded...\n")
			else:
				print("\n[SERVER]: Please Enter a File which exists over the server...\n")
				
		elif(user_inp=="LIST" and connected==1):
			client.send("LIST".encode("utf-8"))
			res2=client.recv(1024).decode("utf-8")
			res_arr=res2.split(" ")
			print("\n")
			for i in res_arr:
				print(i)
			print("\n")
		elif(user_inp=="EXIT" and connected==1):
			client.send("close".encode("utf-8"))
			connected=0
			print("\n[SERVER]: Connection to server closed..\n")
		elif(user_inp=="DELT" and connected==1):
			client.send("DELT".encode("utf-8"))
			temp23=client.recv(1024).decode("utf-8")
			filenm=input("Enter FileName to be Deleted:")
			client.send(filenm.encode("utf-8"))
			resss=client.recv(1024).decode("utf-8")
			if(resss=="DELETED"):
				print("\n[SERVER]: FILE successfully deleted...\n")
			else:
				print("\n[SERVER]: The entered file doesn't exist over the server..\n")
		elif(user_inp=="CONN" and connected==0):
			conn_client=socket(AF_INET,SOCK_STREAM)
			username1=input('Enter username:')
			password1=input('Enter password:')
			conn_client.connect((ip_addr,port_num_conn))
			conn_client.send("WELCOME".encode("utf-8"))
			respon=conn_client.recv(1024).decode("utf-8")
			conn_client.send(username1.encode("utf-8"))
			respon=conn_client.recv(1024).decode("utf-8")
			conn_client.send(password1.encode("utf-8"))
			respon=conn_client.recv(1024).decode("utf-8")
			conn_client.send("Send Authentication Answer...".encode("utf-8"))
			respon=conn_client.recv(1024).decode("utf-8")
			
			if(respon=="YES"):
				print("\n[SERVER]: Authentication Successfull...")
				client.connect((ip_addr,port_num))
				print("[SERVER]: Connection successfull...\n")
				connected=1
			else:
				print("\n[SERVER]: Authentication Failed, Please Enter correct Username & Password..\n")
				conn_client.close()	
		elif(user_inp=="CONN" and connected==1):
			print("\n[HOST]: Connection is already established...\n")
		elif(connected==1):
			print("\n[HOST]: Please Enter a Valid Command...\n")
		else:
			print("\n[HOST]: Please Connect to the Server first in order to access FTP Server...")
	
	
	
	client.close()
	
if __name__=="__main__":
	main()


