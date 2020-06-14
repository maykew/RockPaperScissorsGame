import socket
HOST = '127.0.0.1'     # Endereco IP do Servidor (loopback)
PORT = 5000            # Porta que o Servidor esta usando (identifica qual a aplicacao que tenta acessar)

#-------------- Cria o socket do cliente --------------
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT) # Forma a tupla de host(ip), porta
tcp.connect(dest)	# Estabelece a conexao

#-------------- Protocolo --------------

#Recebendo mensagem inicial
msg = tcp.recv(1024)		# Recebe mensagem
msg = msg.decode('UTF-8')	# Decodifica a mensagem
print (msg)

#Recebendo mensagem para identificação do jogador
msg = tcp.recv(1024)		# Recebe mensagem 
msg = msg.decode('UTF-8')	# Decodifica a mensagem

#Enviando mensagem para identificação do jogador
msg = input(msg)
msg = msg.encode('UTF-8') 	# Codifica a mensagem para UTF-8
tcp.send (msg) 				# Envio a mensagem para o servidor

#Recebendo mensagem dos jogadores da rodada
msg = tcp.recv(1024)		# Recebe mensagem 
msg = msg.decode('UTF-8')	# Decodifica a mensagem
print (msg)

#Enviando mensagem da opcao escolhida
msg = input("\nWhat's your choice - Rock, Paper or Scissors? (to exit use CTRL+X): ")
while msg != '\x18':
    msg = msg.encode('UTF-8') 	# Codifica a mensagem para UTF-8
    tcp.send (msg) 				# Envio a mensagem para o servidor

    msg = tcp.recv(1024)		# Le uma mensgem vinda do servidor
    msg = msg.decode('UTF-8')	# Decodifica a mensagem
    print (dest, msg)

    msg = tcp.recv(1024)		# Le uma mensgem vinda do servidor
    msg = msg.decode('UTF-8')	# Decodifica a mensagem
    print (dest, msg)

    msg = input()
#---------------- fim do protocolo --------------

tcp.close()	# fecha a conexao com o servidor