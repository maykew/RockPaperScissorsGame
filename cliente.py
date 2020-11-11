import socket
HOST = '127.0.0.1'     # Endereco IP do Servidor (loopback)
PORT = 5000            # Porta que o Servidor esta usando (identifica qual a aplicacao que tenta acessar)

#-------------- Funcoes --------------

#Funcao que recebe uma mensagem e uma conexao como paramentro, e encaminha a mensagem para o cliente
def enviaMensagem(msg, destino):
    msg = msg.encode('UTF-8')       # Codifica a mensagem para UTF-8
    destino.send(msg)     #Envia mensagem ao cliente

#Funcao que recebe uma conexao e fica no aguardo para receber uma mensagem
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

#Enviando mensagem para identificação do jogador
msg = input()
enviaMensagem(msg, tcp)

#Recebendo mensagem dos jogadores da rodada
msg = recebeMensagem(tcp)
print (msg)

#Tudo ok
enviaMensagem("Tudo ok", tcp)

#Recebendo mensagem de inicio de rodada
msg = recebeMensagem(tcp)
print (msg)

#------- Troca de mensagens (jogadas) --------------
msg = input("\nWhat's your choice - Rock, Paper or Scissors? (to exit use CTRL+X): ")
while msg != '\x18':
    
    enviaMensagem(msg, tcp)
    
    #Recebendo resposta da jogada enviada
    msg = recebeMensagem(tcp)
    erro = int(msg)
    if erro == 1: 
        print ("\nThe game was interrupted :(")
        msg='\x18'
        break
    elif erro == 2:
        print ("\nSomeone typed wrong, please try again")
        msg='\x18'
        break
    elif erro == 3:
        print ("\nIncorrect option, please try again")
        msg='\x18'
        break
	
	#Tudo ok
    enviaMensagem("Tudo ok", tcp)
	
    #Recebendo mensagem das jogadas
    msg = recebeMensagem(tcp)
    print (msg)

    #Tudo ok
    enviaMensagem("Tudo ok", tcp)

    #Recebendo mensagem do resultado
    msgs = recebeMensagem(tcp)
    msgs = msgs.split(",")
    
    msg = msgs[1]
    fimDeJogo = int(msgs[0])
    
    if fimDeJogo: break

    #Mensagem de continuacao
    print (msg)
    
    #Tudo ok
    enviaMensagem("Tudo ok", tcp)

    #Recebendo mensagem de inicio de rodada
    msg = recebeMensagem(tcp)
    print (msg)

    msg = input("\nWhat's your choice - Rock, Paper or Scissors? (to exit use CTRL+X): ")
#---------------- fim do protocolo --------------

if msg != '\x18':
    print (msg)

tcp.close()	# fecha a conexao com o servidor
