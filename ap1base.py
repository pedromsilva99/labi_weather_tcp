import sys, socket, csv, json

def client():
	tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_s.bind( ("0.0.0.0", 0) )
	tcp_s.connect(("193.136.92.147", 8080))
	con_data = "CONNECT\n"
	b_data = con_data.encode("utf-8")
	tcp_s.send(b_data)
	recv_data = tcp_s.recv(4096)
	data = recv_data.decode("utf-8")
	print(data)
	dict_token = json.loads(data)
	read_data = ("READ "+str(dict_token['TOKEN'])+"\n")
	r_data = read_data.encode("utf-8")
	tcp_s.send(r_data)
	json_data = tcp_s.recv(4096)
	j_data = json_data.decode("utf-8")
	print(j_data)
	while tcp_s.recv(4096):
		data = tcp_s.recv(4096)
		j_data = data.decode("utf-8")
		print(j_data)
	tcp_s.close()
client()
	
