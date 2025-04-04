import socket


PORT = 5000  # Porta do servidor
HOST = "127.0.0.1"

# Criando o socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Enviando uma mensagem
client.sendall(b"Hello, servidor!")

# Fechando a conexão
client.close()
