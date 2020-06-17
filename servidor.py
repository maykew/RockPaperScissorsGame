import socket
HOST = ''              # Endereco IP do Servidor e o endereco atual do computador
PORT = 5000            # Porta do Servidor na maquina 


#-------------- Funcoes --------------

#Funcao que abre a conexao com clientes
def conexao():
    for i in range(numJogadores):
        con, cliente = tcp.accept() # Aceita conexao do cliente
        clientes.append((con, cliente)) #Adicionado cliente na lista de clientes
        print ('Concetado por', clientes[i][1])

#Funcao que recebe uma mensagem e uma conexao como paramentro, e encaminha a mensagem para o cliente
def enviaMensagem(msg, destino):
    msg = msg.encode('UTF-8')       # Codifica a mensagem para UTF-8
    destino.send(msg)     #Envia mensagem ao cliente

#Funcao que recebe uma conexao e fica no aguardo para receber uma mensagem
def recebeMensagem(remetente):
    msg = remetente.recv(1024)		# Le uma mensgem vinda do cliente
    msg = msg.decode('UTF-8')	# Decodifica a mensagem
    return msg

#Funcao que envia boas vindas e identifica jogadores
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
        jogadores.append((msg_nome, i)) #Adiciona nome do jogador a lista de jogadores

#Funcao que envia mensagem aos jogadores sobre adversarios da partida
def adversarios():
    #Enviando mensagem aos jogadores da rodada
    for i in range(numJogadores):
        adversarios=[]
        for j in range(1,numJogadores):
            adversarios.append(jogadores[(i+j)%numJogadores][0])
        msg="\n"+jogadores[i][0]+", your opponents are: "+", ".join(adversarios[:len(adversarios)-1])+" and " + adversarios[-1]
        enviaMensagem(msg, clientes[i][0])

#Funcao que recebe duas jogadas e retorna um resultado
def quemGanhou(j1, j2):
    # Se a jogada um venceu
    if j1 == 1 and j2 == 3 or j1 == 2 and j2 == 1 or j1 == 3 and j2 == 2:
        return 1
    # Se a jogada um perdeu
    elif j2 == 1 and j1 == 3 or j2 == 2 and j1 == 1 or j2 == 3 and j1 == 2:
        return -1
    # Se deu empate
    else:
        return 0

#Funcao que recebe o indice da posicao do cliente e encerra a conexao
def finalizaCliente(pos):
    print ('Finalizando conexao do cliente', clientes[pos][1])
    clientes[pos][0].close()		# fecha a conexao com o cliente

#Funcao que recebe o indice da posicao do cliente e informa que ele eh o vencedor
def msgVencedor(pos):
    msg="1"
    enviaMensagem(msg, clientes[pos][0])
    msg="\nYou win!" 
    enviaMensagem(msg, clientes[pos][0])

#Funcao que recebe o indice da posicao do cliente e informa que ele esta eliminado
def msgEliminado(pos):
    msg="1"
    enviaMensagem(msg, clientes[pos][0])
    msg="\nYou lose!" 
    enviaMensagem(msg, clientes[pos][0])

#Funcao que recebe o indice da posicao do cliente e informa que o jogo deu empate
def msgEmpatado(pos):
    msg="0"
    enviaMensagem(msg, clientes[pos][0])
    msg="\nThe game was a draw, let's go to the next round!"
    enviaMensagem(msg, clientes[pos][0])




#-------------- Cria o socket do servidor --------------
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT) # Forma a tupla de host e porta

tcp.bind(orig)		# Solicita ao S.O. acesso exclusivo a porta 5000
tcp.listen(10)		# Entra no modo de escuta

#------- Protocolo --------------

while True:

    #Numero de jogadores
    numJogadores = 3

    #Lista de clientes que armazenda conxecao e o cliente em uma tupla
    clientes = []
    
    #lista de nomes dos jogadores que armazena nome dos jogadores e o indice da conexao
    jogadores = []

    #Realiza a conexao dos clientes
    conexao()

    #Realiza a identificacao dos clientes
    identificacao()
    
    #Envia mensagem aos jogadores da rodada
    adversarios()

    
    cont=0  #Variavel de indicar rodada
    fimDeJogo = False   # Variavel para indicar fim de jogo

    #-------------- Troca de mensagens --------------
    while not fimDeJogo:

        print("\nInicio da rodada")
        cont+=1 #Incrementando variavel indicador de rodada 
        jogadas=[]     # Lista com as jogadas da rodada

        #Enviando mensagem de inicio de rodada
        for i in range(len(jogadores)):
            indice=jogadores[i][1]
            msg="\n---------- Round "+ str(cont) +" ----------\n"
            enviaMensagem(msg, clientes[indice][0])

        print("\nRecebendo jogadas da rodada")
        #Recebendo mensagem de jogadas
        mensagens = []
        parou = False
        for i in range(len(jogadores)):
            indice=jogadores[i][1]
            msg = clientes[indice][0].recv(1024)       
            if not msg:
                parou = True 
                break
            mensagens.append(msg)
        if parou: break

        print("\nArmazenando jogadas da rodada")
        #Armazenando jogadas
        for i in range(len(jogadores)):
            msg = mensagens[i].decode('UTF-8')	# Decodifica a mensagem
            if (msg.lower() == "pedra" or msg.lower() == "rock"): msg=1
            elif (msg.lower() == "papel" or msg.lower() == "paper"): msg=2
            elif (msg.lower() == "tesoura" or msg.lower() == "scissor"): msg=3
            jogadas.append(msg)

        #print para controle do servidor
        print("\nJogadas da rodada:")
        for i in range(len(jogadores)):
            print(jogadores[i][0]," - ",jogadas[i])


        terminouRodada = False  #Variavel indicando termino da rodada
        empate = True   #Variavel indicando empate na rodada
        i=0

        #Analise das jogadas
        while (i<len(jogadores) and not terminouRodada):
            resultado = 0

            #Verificando resultados
            for j in range(len(jogadores)):
                if i != j:
                    resultado += quemGanhou(jogadas[i], jogadas[j])

            #Um jogador venceu todos os outros
            if resultado == len(jogadores)-1:
                print("\n",jogadores[i][0], " venceu")
                msgVencedor(jogadores[i][1])
                for j in range(len(jogadores)):
                    if i != j:
                        msgEliminado(jogadores[j][1])
                empate = False
                terminouRodada = True
                fimDeJogo = True

            #Um jogador foi eliminado (perdeu para todos os outros)
            elif resultado == ((len(jogadores)-1)*(-1)):
                print("\n",jogadores[i][0], " foi eliminado")
                msgEliminado(jogadores[i][1])
                if len(jogadores) > 2:
                    for j in range(len(jogadores)):
                        if i != j:
                            msgEmpatado(jogadores[j][1])
                print("\nJogador excluido")
                jogadores.pop(i)
                if len(jogadores) == 1:
                    print("\nJogador ", jogadores[0][0] , "venceu")
                    msgVencedor(jogadores[0][1])
                    fimDeJogo = True
                empate = False
                terminouRodada = True
            i+=1

        #Ninguem venceu
        if empate:
            print("\nEmpate")
            for j in range(len(jogadores)):
                indice=jogadores[j][1]
                msgEmpatado(indice)


    #---------------- fim do protocolo --------------

    for i in range(numJogadores):
        finalizaCliente(i)