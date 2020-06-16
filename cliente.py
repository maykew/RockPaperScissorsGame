import socket
HOST = '127.0.0.1'     # Endereco IP do Servidor (loopback)
PORT = 5000            # Porta que o Servidor esta usando (identifica qual a aplicacao que tenta acessar)

#-------------- Funcoes --------------
def enviaMensagem(msg, destino):
    msg = msg.encode('UTF-8')       # Codifica a mensagem para UTF-8
    destino.send(msg)     #Envia mensagem ao cliente

def recebeMensagem(remetente):
    msg = remetente.recv(1024)		# Le uma mensgem vinda do cliente
    msg = msg.decode('UTF-8')	# Decodifica a mensagem
    return msg


#-------------- Cria o socket do cliente --------------
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT) # Forma a tupla de host(ip), porta
tcp.connect(dest)	# Estabelece a conexao

#-------------- Protocolo --------------

#Recebendo mensagem inicial
msg = recebeMensagem(tcp)
print (msg)

#Recebendo mensagem para identificação do jogador
msg = recebeMensagem(tcp)

#Enviando mensagem para identificação do jogador
msg = input(msg)
enviaMensagem(msg, tcp)

#Recebendo mensagem dos jogadores da rodada
msg = recebeMensagem(tcp)
print (msg)

#------- Troca de mensagens --------------
msg = input("\nTo exit use CTRL+X: ")
while msg != '\x18':
    
    enviaMensagem(msg, tcp)

    msg = recebeMensagem(tcp)
    print (dest, msg)

    msg = recebeMensagem(tcp)
    print (dest, msg)

    msg = input("\nTo exit use CTRL+X: ")
#---------------- fim do protocolo --------------

tcp.close()	# fecha a conexao com o servidor