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
bufferSize = 20* 1024  # Buffer de Tamanho T = 20
packetSize = 1024  # Pacotes de Tamanho M = 1024
tamJanela = 0
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
    tamJanela = cwnd
    
    
def recebe_tamJanela():
    global cwnd
    msg_tamJanela, addres = UdpServerSocket.recvfrom(bufferSize)
    cwnd = int(msg_tamJanela)    
    print('Tamanho da janela: ' + str(cwnd))
    

recebe_tamJanela()      # Recebe o tamanho da janela do definido pelo cliente



print('Servidor iniciado.')

while True:
    # Recebe dados do cliente    
    data, address = UdpServerSocket.recvfrom(bufferSize)
    
    # Trata os dados recebidos em numero de sequencia e dado    
    num_seq, dados = data.split(b':', 1)
    num_seq = int(num_seq)
    
    atualiza_janela()
       
    # Verificação do tamanho da janela deslizante
    if bufferSize < 10 * packetSize:
        print('O tamanho da janela deslizante deve ser pelo menos 10 vezes o tamanho do pacote.')
        exit()
    
    # Verifica se o pacote recebido está dentro da janela deslizante
    if prox_numero_seq <= num_seq < prox_numero_seq + bufferSize:
        
        # Adiciona o pacote recebido à lista
        lista.heappush(pacotes_recebidos, (num_seq, dados))
        
        # Verifica se o pacote recebido é o próximo na ordem
        print(pacotes_recebidos[0][0])
        print(prox_numero_seq)
        while pacotes_recebidos and pacotes_recebidos[0][0] == prox_numero_seq:
            # Remove da fila
            _, pacote = lista.heappop(pacotes_recebidos)  
            
            # Verifica se ha espaço no buffer
            print(len(pacotes_recebidos))
            print(tamJanela)
            if len(pacotes_recebidos) < tamJanela:        
                # Processa o pacote
                # função para processar o pacote 
                print ('Pacote recebido: ', pacote.decode())
                        
                # Incrementa numero de sequencia esperado                
                prox_numero_seq += len(pacote)                
                
                # Exibe os dados recebidos   
                print('Mensagem recebida ', data.decode()) 
                
                # Envia uma resposta ao cliente    
                envia_ack(prox_numero_seq, address)
            
            else: 
                # Pacote descartado
                print('Pacote descartado devido estouro do buffer')
    
    
    
