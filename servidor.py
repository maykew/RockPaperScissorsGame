import socket
HOST = ''              # Endereco IP do Servidor e o endereco atual do computador
PORT = 5000            # Porta do Servidor na maquina 

#-------------- Cria o socket do servidor --------------
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT) # Forma a tupla de host e porta

tcp.bind(orig)		# Solicita ao S.O. acesso exclusivo a porta 5000
tcp.listen(10)		# Entra no modo de escuta

#-------------- Protocolo --------------

while True:

    #Lista de clientes
    clientes = []
    
    #lista de nomes dos jogadores
    jogadores=[]

    for i in range(3):
        con, cliente = tcp.accept() # Aceita conexao do cliente
        clientes.append((con, cliente)) #Adicionado cliente na lista de clientes
        print ('Concetado por', clientes[i][1])

        #Enviando mensagem inicial
        msg_inicial = "\nHi! Welcome to Rock, Paper, Scissors Game\n"
        msg_inicial = msg_inicial.encode('UTF-8')       # Codifica a mensagem para UTF-8
        clientes[i][0].send (msg_inicial)     #Envia mensagem inicial ao cliente

        #Enviando mensagem para identificação do jogador
        msg_nome = "Type your name: "
        msg_nome = msg_nome.encode('UTF-8')       # Codifica a mensagem para UTF-8
        clientes[i][0].send (msg_nome)     #Envia mensagem para identificação do jogador

        #Recebendo mensagem para identificação do jogador
        msg_nome = clientes[i][0].recv(1024)		# Le uma mensgem vinda do cliente
        msg_nome = msg_nome.decode('UTF-8')	# Decodifica a mensagem
        jogadores.append(msg_nome) #Adiciona nome do jogador a lista de jogadores

    #Enviando mensagem aos jogadores da rodada
    for i in range(3):
        msg="\n"+jogadores[i]+", your opponents are "+jogadores[(i+1)%3]+" and "+jogadores[(i+2)%3]
        msg = msg.encode('UTF-8')       # Codifica a mensagem para UTF-8
        clientes[i][0].send (msg)     #Envia mensagem ao cliente

    #------- Troca de mensagens --------------
    while True:
        #Recebendo mensagem de jogadas
        mensagens = []  #Lista de mensagens 
        for i in range(3):
            msg = clientes[i][0].recv(1024)		# Recebe mensagem do cliente         
            if not msg: break
            mensagens.append(msg)     # Armazena mensagem          
        if not msg: break

        for i in range(3):
            for j in range(1,3):
                clientes[(i+j)%3][0].send (mensagens[i])	    		# Envia a mensagem para o cliente 

    #---------------- fim do protocolo --------------

    for i in range(3):
        print ('Finalizando conexao do cliente', clientes[i][1])
        clientes[i][0].close()		# fecha a conexao com o cliente


