import socket
HOST = ''              # Endereco IP do Servidor e o endereco atual do computador
PORT = 5000            # Porta do Servidor na maquina 

#-------------- Funcoes --------------
def conexao():
    for i in range(numJogadores):
        con, cliente = tcp.accept() # Aceita conexao do cliente
        clientes.append((con, cliente)) #Adicionado cliente na lista de clientes
        print ('Concetado por', clientes[i][1])

def enviaMensagem(msg, destino):
    msg = msg.encode('UTF-8')       # Codifica a mensagem para UTF-8
    destino.send(msg)     #Envia mensagem ao cliente

def recebeMensagem(remetente):
    msg = remetente.recv(1024)		# Le uma mensgem vinda do cliente
    msg = msg.decode('UTF-8')	# Decodifica a mensagem
    return msg

def identificacao():
    for i in range(numJogadores):
        #Enviando mensagem inicial
        msg_inicial = "\nHi! Welcome to Rock, Paper, Scissors Game\n"
        enviaMensagem(msg_inicial, clientes[i][0])

        #Enviando mensagem para identificação do jogador
        msg_nome = "Type your name: "
        enviaMensagem(msg_nome, clientes[i][0])

        #Recebendo mensagem para identificação do jogador
        msg_nome = recebeMensagem(clientes[i][0])
        jogadores.append(msg_nome) #Adiciona nome do jogador a lista de jogadores
    
def adversarios():
    #Enviando mensagem aos jogadores da rodada
    for i in range(numJogadores):
        adversarios=[]
        for j in range(1,numJogadores):
            adversarios.append(jogadores[(i+j)%numJogadores])
        msg="\n"+jogadores[i]+", your opponents are: "+", ".join(adversarios[:len(adversarios)-1])+" and " + adversarios[-1]
        enviaMensagem(msg, clientes[i][0])




#-------------- Cria o socket do servidor --------------
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT) # Forma a tupla de host e porta

tcp.bind(orig)		# Solicita ao S.O. acesso exclusivo a porta 5000
tcp.listen(10)		# Entra no modo de escuta

#-------------- Protocolo --------------

while True:

    #Numero de jogadores
    numJogadores = 3

    #Lista de clientes
    clientes = []
    
    #lista de nomes dos jogadores
    jogadores=[]

    #Realiza a conexao dos clientes
    conexao()

    #Realiza a identificacao dos clientes
    identificacao()
    
    #Envia mensagem aos jogadores da rodada
    adversarios()

    #------- Troca de mensagens --------------
    while True:

        #Recebendo mensagem de jogadas
        mensagens = []  #Lista de mensagens 
        for i in range(numJogadores):
            msg = recebeMensagem(clientes[i][0])      
            if not msg: break
            mensagens.append(msg)     # Armazena mensagem          
        if not msg: break

        for i in range(numJogadores):
            for j in range(1,numJogadores): 
                enviaMensagem(mensagens[i], clientes[(i+j)%numJogadores][0])   		# Envia a mensagem para o cliente 

    #---------------- fim do protocolo --------------

    for i in range(numJogadores):
        print ('Finalizando conexao do cliente', clientes[i][1])
        clientes[i][0].close()		# fecha a conexao com o cliente


