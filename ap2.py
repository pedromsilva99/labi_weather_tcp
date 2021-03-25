import sys, socket, csv, json
from random import randint

def main():
	tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_s.connect(("193.136.92.147", 8080))
	f_connect(tcp_s)
	json_data = tcp_s.recv(4096)
	dict_data = json_data.decode("utf-8")
	print(dict_data)
	fich = open('Dados.csv','w')
	writer = csv.DictWriter(fich, fieldnames=['WIND','HUMIDITY','TEMPERATURE'], delimiter=",")
	writer.writeheader()
	temps = 0
	cont = 0
	while 1:
		data = tcp_s.recv(4096)
		j_data = data.decode("utf-8")
		try:
			data_s = json.loads(j_data)
			print_csv(data_s, fich, writer)	
			weather_info(data_s, cont, temps)
			if cont == 3:
				cont = 0
				temps = 0
			cont = cont + 1
			temps = temps + data_s['TEMPERATURE']
		except:
			continue
		
		print(j_data)
		
	fich.close()
	tcp_s.close()

def weather_info(data_s, cont, temps):
	if cont == 3:
		media = temps/3
		if media < 20:
			print("A média da temperatura é %f. Leve um casaco!" % (media))
	

def print_csv(data_s, fich, writer):
	writer.writerow({'WIND': data_s["WIND"], 'HUMIDITY': data_s["HUMIDITY"], 'TEMPERATURE': data_s["TEMPERATURE"]})
	fich.flush()

def f_connect(tcp_s):
	con_data = "CONNECT\n"
	b_data = con_data.encode("utf-8")
	tcp_s.send(b_data)
	recv_data = tcp_s.recv(4096)
	data = recv_data.decode("utf-8")
	print(data)
	try:
		dict_token = json.loads(data)
		read_data = ("READ "+str(dict_token["TOKEN"])+"\n")
		r_data = read_data.encode("utf-8")
		tcp_s.send(r_data)
	except:
		main()
main()


