import socket
import heapq as lista

# Configurações do servidor
host = '127.0.0.1'  # Endereço IP do servidor
port = 20001  # Porta do servidor

# Criação do socket UDP
UdpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UdpServerSocket.bind((host, port))

# Lista de pacotes recebidos e numero de sequencia esperado

pacotes_recebidos = [] 
prox_numero_seq = 0
bufferSize = (20 * 1024)  # Buffer de Tamanho T = 20
packetSize = 1024  # Pacotes de Tamanho M = 1024
tamJanela = 10 * packetSize
cwnd = 1

# Função para processar um pacote recebido
# def processa_pacote()

# Função responsável pelo envio de ACK
def envia_ack(num_ack, addr):
    msg_ack = str(num_ack).encode()
    UdpServerSocket.sendto(msg_ack, addr)
    print('Proximo nº de seq. esperado: '+ str(prox_numero_seq))
    

def atualiza_janela():
    global tamJanela
    tamJanela = min(cwnd, len(pacotes_recebidos))
    
    
def recebe_tamJanela():
    global cwnd
    msg_tamJanela, addres = UdpServerSocket.recvfrom(bufferSize)
    cwnd = int(msg_tamJanela)    
    print('Tamanho da janela: ' + str(cwnd))
    

recebe_tamJanela()      # Recebe o tamanho da janela do definido pelo cliente

tamPacote = True # Flag para controlar primeira mensagem: tamanho do pacote

print('Servidor iniciado.')

while True:
    # Recebe dados do cliente    
    data, address = UdpServerSocket.recvfrom(bufferSize)
    
    if tamPacote:
        tamanho = int(data)
        print('Tamanho do pacote: ', tamanho )
        tamPacote = False
        continue
    
    # Trata os dados recebidos em numero de sequencia e dado    
    split_data = data.split(b':::')
    if len(split_data) == 2:
        num_seq, dados = split_data
        num_seq = int(num_seq)
    else:
        print('Formato inválido da mensagem recebida.')
        continue
    
       
    # Verificação do tamanho da janela deslizante
    if bufferSize < 10 * packetSize:
        print('O tamanho da janela deslizante deve ser pelo menos 10 vezes o tamanho do pacote.')
        exit()
    
    # Verifica se o pacote recebido está dentro da janela deslizante
    print('Numero de sequencia esperado', prox_numero_seq)
    print('Numero de sequencia recebido', num_seq)
    print('tamanho da janela: ', tamJanela)
    print(prox_numero_seq + bufferSize)
    if prox_numero_seq <= num_seq < (prox_numero_seq + bufferSize):
        
        # Adiciona o pacote recebido à lista
        lista.heappush(pacotes_recebidos, (num_seq, dados))
        atualiza_janela()
        
        # Verifica se o pacote recebido é o próximo na ordem
        if (num_seq - prox_numero_seq) <= 25:
            prox_numero_seq = num_seq
        while pacotes_recebidos and pacotes_recebidos[0][0] == prox_numero_seq:
            # Remove da fila
            _, pacote = lista.heappop(pacotes_recebidos)  
            
            # Verifica se ha espaço no buffer
            if len(pacotes_recebidos) < tamJanela:                        
                # Incrementa numero de sequencia esperado                
                prox_numero_seq += len(pacote)                
                
                # Exibe os dados recebidos   
                #print('Mensagem recebida ', data.decode()) 
                
                # Envia uma resposta ao cliente    
                envia_ack(prox_numero_seq, address)
            
            else: 
                # Pacote descartado
                print('Pacote descartado devido estouro do buffer')
    
    
    
