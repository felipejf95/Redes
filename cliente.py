import socket

# Configurações do cliente
host = '127.0.0.1'  # Endereço IP do servidor
port = 20001  # Porta do servidor
bufferSize = 1024 * 10 

# Criação do socket UDP
UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Numero de sequencia
num_seq = 0

msg = ''

def recebe_ack():
    ack, _ = UDPClientSocket.recvfrom(bufferSize)
    num_ack = int(ack)
    print('ACK acumulativo recebido: ', num_ack)
    msg = ack.decode()
    

while True:
    # Solicita que o usuário digite uma mensagem
    message = input('Digite uma mensagem para enviar ao servidor (ou digite "sair" para encerrar): ')
    
    if message == 'sair':
        break
    
    # Pacote com o numero de sequencia 
    pacote = f"{num_seq}:{message}".encode()
    
    # Envia a mensagem para o servidor
    UDPClientSocket.sendto(pacote, (host, port)) 
    
    print(num_seq)
    # Incrementando o numero de sequencia conforme o fluxo de bytes    
    num_seq += len(message)
    print(num_seq)
    
    
    # Recebe o ACK acumulativo
    recebe_ack()         
    
    # Exibe a resposta recebida
    print(msg)
    
     
        

# Fecha o socket do cliente
UDPClientSocket.close()