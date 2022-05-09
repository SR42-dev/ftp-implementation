from socket import *
import os
ip_addr=gethostbyname(gethostname())
port_num=4497
port_num_conn=4603
USERNAME_REQ="admin"
PASSWORD_REQ="admin"

def connected_func():
	server=socket(AF_INET,SOCK_STREAM);
	server.bind((ip_addr,port_num))
	server.listen()
	print('[HOST]: Waiting for client to connect...')
	while True:
		con,client=server.accept()
		print('[HOST]: New client connection received...')
		while True:
			command_type=con.recv(1024).decode("utf-8")
			if(command_type=="UPLD"):
				con.send("inside UPLD".encode("utf-8"))
				filename=con.recv(1024).decode("utf-8")
				print(f"[HOST]: {filename} has been recieved to be uploaded.\n")
				
				if(filename!="NO_FILE_EXISTS_12345"):
					write_file=open("server_data/"+filename,"w")
					con.send("Filename recieved".encode("utf-8"))
			
					file_data=con.recv(1024).decode("utf-8")
			
					write_file.write(file_data)
					print("[HOST]: file data received...".encode("utf-8"))
					con.send("file data received...".encode("utf-8"))
					write_file.close()
				else:
					con.send("Filename recieved".encode("utf-8"))
					file_data=con.recv(1024).decode("utf-8")
					con.send("file data received...".encode("utf-8"))
					
			elif(command_type=="close"):
				con.close()
				print("[HOST]: connection to client closed...\n")
				return
				
			elif(command_type=="LIST"):
				con.send(' '.join(os.listdir('./server_data/')).encode('utf-8'))
			elif(command_type=="DELT"):
				con.send("DELT recieved".encode("utf-8"))
				filenm=con.recv(1024).decode("utf-8")
				if(os.path.exists("./server_data/"+filenm)==True):
					os.remove("./server_data/"+filenm)
					con.send("DELETED".encode("utf-8"))
					print("\n[HOST]: File DELETED....\n")
				else:
					con.send("NOT_FOUND".encode("utf-8"))
					print("\n[HOST]: File NOT FOUND....\n")
			elif(command_type=="DWND"):
				print("inside DWND server")
				con.send("DWND recieved".encode("utf-8"))
				filename2=con.recv(1024).decode("utf-8")
				print(f"[HOST]: {filename2} has been requested to download")
				if(os.path.exists("./server_data/"+filename2)==True):
					read_file=open("server_data/"+filename2,"r")
					con.send("Request to download recieved".encode("utf-8"))
					res3=con.recv(1024).decode("utf-8")
					data2=read_file.read()
					con.send(data2.encode("utf-8"))
					print("[HOST]: data sent\n")
					read_file.close()
				else:
					con.send("Request to download recieved".encode("utf-8"))
					res3=con.recv(1024).decode("utf-8")
					con.send("NULL_12345".encode("utf-8"))
					print("[HOST]: No File Found\n")
				







def main():
	print('[HOST]: Server is Running on TCP socket...')
	
	conn_server=socket(AF_INET,SOCK_STREAM)
	conn_server.bind((ip_addr,port_num_conn))
	conn_server.listen()
	
	while True:
		print('[HOST]: Waiting for client to authenticate...')
		con_cli,client_con=conn_server.accept()
		print("[HOST]: Authentication Request Recieved...")
		client_msg=con_cli.recv(1024).decode("utf-8")
		con_cli.send("Authentication recieved...".encode("utf-8"))
		username2=con_cli.recv(1024).decode("utf-8")
		con_cli.send("Username recieved".encode("utf-8"))
		password2=con_cli.recv(1024).decode("utf-8")
		con_cli.send("Password recieved...".encode("utf-8"))
		req1=con_cli.recv(1024).decode("utf-8")
		if(username2==USERNAME_REQ and password2==PASSWORD_REQ):
			print("[HOST]: Correct username && password...\n")
			con_cli.send("YES".encode("utf-8"))
			connected_func()
		else:
			print("[HOST]: Wrong username && password...\n")
			con_cli.send("NO".encode("utf-8"))
			con_cli.close()
	conn_server.close()
	print("[HOST]: Connnection socket closed...\n")
	
	
	
if __name__=="__main__":
	main()


