import sys, socket, csv, json, hashlib, binascii
from random import randint
from Crypto.Cipher import AES
import base64

def main():
	tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_s.connect(("193.136.92.147", 8080))
	#res = input("Quer usar mensagens encriptadas? Y/n ")
	#if res in ['Y', 'y']:
	#	encrypt(tcp_s)
	#else:
		#f_connect(tcp_s)
	f_connect(tcp_s)
	dict_data = tcp_s.recv(4096).decode("utf-8")
	print(dict_data)
	fich = open('Dados.csv','w')
	writer = csv.DictWriter(fich, fieldnames=['WIND','HUMIDITY','TEMPERATURE'], delimiter=",")
	writer.writeheader()
	temps = 0
	cont = 0
	while 1:
		j_data = tcp_s.recv(4096).decode("utf-8")
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

def weather_info(data_s, cont, temps): #função para fazer print no terminal da informação do tempo
	if cont == 3:
		media = temps/3
		if media < 20:
			print("A média da temperatura é %f. Leve um casaco!" % (media))
		else:
			print("A média da temperatura é %f. Está um tempo agradável." % (media))
	

def print_csv(data_s, fich, writer): #função para escrever no documento CSV a informação
	writer.writerow({'WIND': data_s["WIND"], 'HUMIDITY': data_s["HUMIDITY"], 'TEMPERATURE': data_s["TEMPERATURE"]})
	fich.flush()
	

def f_connect(tcp_s): #função para receber e enviar o TOKEN
	con_data = "CONNECT\n"
	tcp_s.send(con_data.encode("utf-8"))
	data = tcp_s.recv(4096).decode("utf-8")
	print(data)
	try:
		dict_token = json.loads(data)
		read_data = ("READ "+str(dict_token["TOKEN"])+"\n")
		tcp_s.send(read_data.encode("utf-8"))
	except:
		main()
		
# Não conseguimos pôr a parte da encriptação devido a um erro na função recv_data

#~ def encrypt(tcp_s):
	#~ p = 2**33
	#~ g = 49985642365
	#~ a = randint(0,9)
	#~ A = pow(g,a,p)
	#~ con_data = "CONNECT "+str(A)+","+str(p)+","+str(g)+"\n"
	#~ tcp_s.send(con_data.encode("utf-8"))
	#~ data = tcp_s.recv(4096).decode("utf-8")
	#~ print(data)
	#~ try:
		#~ raw_B = json.loads(data)
		#~ B = raw_B['B']
		#~ read_data = "READ "+str(raw_B['TOKEN'])+"\n"
	#~ except:
		#~ encrypt(tcp_s)

	#~ X = pow(B,a,p)
	#~ key = hashlib.md5()
	#~ key.update(str(X).encode("utf-8"))
	#~ X = key.hexdigest()
	#~ X = X[0:16]
	#~ cipher = AES.new(X)
	#~ lst_block = len(read_data) % cipher.block_size
	#~ if lst_block != cipher.block_size :
		#~ p = cipher.block_size - len(read_data)
		#~ read_data = read_data + chr(p) * p
	#~ data = cipher.encrypt(read_data)
	#~ data = base64.b64encode(data)+"\n".encode("utf-8")
	#~ tcp_s.send(data)
	#~ data = recv_data(tcp_s, X).decode("utf-8")
	#~ fich = open('Dados.csv','w')
	#~ writer = csv.DictWriter(fich, fieldnames=['WIND','HUMIDITY','TEMPERATURE'], delimiter=",")
	#~ writer.writeheader()
	#~ temps = 0
	#~ cont = 0
	#~ while 1:
		#~ try:
			#~ data = json.loads(recv_data(tcp_s, X).decode("utf-8"))
			#~ print_csv(data, fich, writer)
			#~ weather_info(data, cont, temps)
			#~ if cont == 3:
				#~ cont = 0
				#~ temps = 0
			#~ cont = cont + 1
			#~ temps = temps + data_s['TEMPERATURE']
			#~ print(data)
		#~ except:
			#~ continue
		
	#~ fich.close()
	#~ tcp_s.close()

#~ def recv_data(tcp_s, X):
	#~ cipher = AES.new(X)
	#~ data = tcp_s.recv(4096)
	#~ data = base64.b64decode(data)
	#~ data = cipher.decrypt(data)
	#~ p = data[len(data)-1]
	#~ data = data[0:len(data)-p]
	#~ return data
	
main()


