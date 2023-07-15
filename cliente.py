import socket
import os
import time
import matplotlib.pyplot as plt


# Configurações do cliente
host = '127.0.0.1'  # Endereço IP do servidor
port = 20001  # Porta do servidor
bufferSize = 1024 * 10 

# Criação do socket UDP
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Numero de sequencia, janela e controle de congestionamento
num_seq = 0
tamJanela = bufferSize
cwnd = 1
sstresh = 16

msg = ''

def recebe_ack():
    ack, _ = UDPClientSocket.recvfrom(bufferSize)
    num_ack = int(ack)
    print('ACK acumulativo recebido: ', num_ack)
    msg = ack.decode()
    

def tamanho_janela():    
    msg_Tamjanela = str(tamJanela).encode()
    UDPClientSocket.sendto(msg_Tamjanela, (host, port))
    print('Tamanho da janela: ' + str(tamJanela))
    
def atualiza_janela(numACK):
    global tamJanela, cwnd, ssthresh
    
    if numACK >= num_seq:           # 
        cwnd += 1           # Aumenta a janela de congestionamento
    else:
        cwnd = max(cwnd // 2, 1)    # Reduz a janela de congestionamento pela metade, slow start
        sstresh = max(cwnd, 1)      # Define o novo limiar de slow start
        
    tamJanela = min(cwnd, ssthresh)    

tamanho_janela()                    # Passa para o remente o tamanho da janela deslizante

# Nome do arquivo a ser enviado
file_name = 'verificacao.txt'

# Verifica o tamanho do arquivo
file_size = os.path.getsize(file_name)
print('Tamanho do arquivo:', file_size)

# Envia o tamanho do arquivo para o servidor
file_size_message = str(file_size).encode()
UDPClientSocket.sendto(file_size_message, (host, port))


    
# Variaveis para medir vazão
tempoInicio = time.time()
bytes_enviados = 0
throughput_values = []

# abre o arquivo que sera enviado
with open(file_name, 'rb') as file:
    
    while True:
        # Lê os dados do arquivo
        message = file.read(bufferSize)
        
        if not message:
            # Fim do arquivo
            break
        
        #num_seq += len(message)       
        
        # Pacote com o numero de sequencia 
        print(num_seq)
        pacote = f"{num_seq}:::{message}".encode()
        
        # Envia a mensagem para o servidor
        UDPClientSocket.sendto(pacote, (host, port)) 
        
        print('Numero de sequencia atual: ', num_seq)
        # Incrementando o numero de sequencia conforme o fluxo de bytes    
        num_seq += len(pacote)-4
        print('Proximo numero de sequencia: ', num_seq)    
        
        # Recebe o ACK acumulativo
        recebe_ack()    
        
        # Exibe a resposta recebida
        print(msg)
        
        # Atualiza o tamanho total de bytes enviados
        bytes_enviados += len(pacote)
        
        # Calcula a vazão atual
        current_time = time.time()
        elapsed_time = current_time - tempoInicio
        throughput = bytes_enviados / elapsed_time
        
        # Adiciona o valor de vazão à lista
        throughput_values.append(throughput)
        
        # Imprime a vazão atual
        print('Vazão atual:', throughput, 'bytes/segundo')
    
# Fecha o socket do cliente
UDPClientSocket.close()

# Plota o gráfico de vazão
tempoInicio = [t - tempoInicio for t in range(len(throughput_values))]
plt.plot(tempoInicio, throughput_values)
plt.xlabel('Tempo (segundos)')
plt.ylabel('Vazão (bytes/segundo)')
plt.title('Vazão da rede')
plt.show()