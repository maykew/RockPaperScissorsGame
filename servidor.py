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

#Funcao que recebe a opcao escolhida e retorna o id correspondente da opcao
def jogadaToInt(opcao):
    if (opcao.lower() == "pedra" or opcao.lower() == "rock"):
        return 1
    elif (opcao.lower() == "papel" or opcao.lower() == "paper"):
        return 2
    elif (opcao.lower() == "tesoura" or opcao.lower() == "scissors"):
        return 3
    else:
        return -1
            
#Funcao que recebe o id correspondente da opcao e retorna a opcao escolhida
def jogadaToString (indice):
    if (indice == 1):
        return "rock"
    elif (indice == 2):
        return "paper"
    elif (indice == 3):
        return "scissors"

#Funcao que recebe a lista de jogadas e envia aos jogadores as jogadas
def jogadasRodada(listJogadas):
    for i in range(len(listJogadas)):
        opcao = jogadaToString(listJogadas[jogadores[i][1]])
        msg="\nThese were the moves:\n"+jogadores[i][0]+": "+opcao
        for j in range(1,len(listJogadas)):
            opcao=jogadaToString(listJogadas[jogadores[(i+j)%len(listJogadas)][1]])
            msg+="\n"+jogadores[(i+j)%len(listJogadas)][0]
            msg+=": "+opcao
        
        enviaMensagem(msg, clientes[jogadores[i][1]][0])




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
        cont+=1     #Incrementando variavel indicador de rodada 
        #jogadas=[]     # Lista com as jogadas da rodada
        jogadas={}

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
                quemParou = i
            mensagens.append(msg)

        #Caso algum jogador interrompa a partida ou digite a opção errada, todos jogadores perdem a conexão
        if parou:
            for i in range(len(jogadores)):
                if i != quemParou:
                    indice = jogadores[i][1]
                    enviaMensagem("1", clientes[indice][0])
            break
        
        else:
            print("\nArmazenando jogadas da rodada")
            #Armazenando jogadas
            for i in range(len(jogadores)):
                opcao = mensagens[i].decode('UTF-8')	# Decodifica a mensagem
                msg = jogadaToInt(opcao)
                if msg < 0:
                    parou = True
                    for j in range(len(jogadores)):
                        if i != j:
                            indice = jogadores[j][1]
                            enviaMensagem("2", clientes[indice][0])
                        else:
                            indice = jogadores[j][1]
                            enviaMensagem("3", clientes[indice][0])
                    break
                jogadas[jogadores[i][1]]=msg
            
            if parou: break

            for i in range(len(jogadores)):
                indice = jogadores[i][1]
                enviaMensagem("0", clientes[indice][0])  

        #print para controle do servidor
        print("\nJogadas da rodada:")
        for i in range(len(jogadores)):
            jogador = jogadores[i]
            print(jogador[0]," - ",jogadas[jogador[1]])
        
        #Enviando jogadas da rodad aos clientes
        jogadasRodada(jogadas)

        #Tudo ok
        for i in range(len(jogadores)):
            recebeMensagem(clientes[jogadores[i][1]][0])

        terminouRodada = False  #Variavel indicando termino da rodada
        empate = True   #Variavel indicando empate na rodada
        i=0

        #Analise das jogadas
        while (i<len(jogadores) and not terminouRodada):
            resultado = 0

            #Verificando resultados
            for j in range(len(jogadores)):
                if i != j:
                    jogador1 = jogadores[i]
                    jogador2 = jogadores[j]
                    resultado += quemGanhou(jogadas[jogador1[1]], jogadas[jogador2[1]])

            #Um jogador venceu todos os outros
            if resultado == len(jogadores)-1:
                print("\nJogador ",jogadores[i][0], " venceu\n")
                msgVencedor(jogadores[i][1])
                for j in range(len(jogadores)):
                    if i != j:
                        msgEliminado(jogadores[j][1])
                empate = False
                terminouRodada = True
                fimDeJogo = True

            #Um jogador foi eliminado (perdeu para todos os outros)
            elif resultado == ((len(jogadores)-1)*(-1)):
                print("\nJogador ",jogadores[i][0], " foi eliminado")
                msgEliminado(jogadores[i][1])
                if len(jogadores) > 2:
                    for j in range(len(jogadores)):
                        if i != j:
                            msgEmpatado(jogadores[j][1])
                print("\nJogador excluido")
                jogadores.pop(i)
                if len(jogadores) == 1:
                    print("\nJogador ", jogadores[0][0] , "venceu\n")
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

    for i in range(len(clientes)):
        finalizaCliente(i)