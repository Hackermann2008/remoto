import socket
import threading
import os
import time # Adicionado para pequenos delays, se necessário

# --- Configurações do Servidor ---
HOST = '0.0.0.0'
# Render define a porta através da variável de ambiente PORT.
# Usamos 4444 como fallback se não estiver em um ambiente Render (rodando localmente).
PORT = int(os.environ.get('PORT', 4444))

# --- Função para lidar com cada cliente conectado ---
def handle_client(client_socket, addr):
    print(f"[*] Conexão aceita de: {addr[0]}:{addr[1]}")
    try:
        while True:
            # --- ATENÇÃO: MODIFICAÇÃO CRÍTICA PARA AMBIENTES DE NUVEM ---
            # A função `input()` foi removida porque ambientes de nuvem (como Render)
            # não possuem um console interativo para digitar comandos.
            #
            # Neste novo modelo, o servidor AGUARDA que o CLIENTE envie um comando ou dado.
            #
            # Se você deseja que o SERVIDOR INICIE comandos (como no seu script original),
            # você precisará implementar um novo mecanismo para ele obter esses comandos
            # de uma fonte não interativa (ex: uma API REST, uma fila de mensagens,
            # ou um cliente operador dedicado que se conecta a este servidor).

            # Recebe dados do cliente (até 4096 bytes)
            data = client_socket.recv(4096)
            if not data: # Se não houver dados, o cliente desconectou
                break

            received_command = data.decode('utf-8', errors='ignore').strip()
            print(f"[{addr[0]}:{addr[1]}] Cliente enviou: {received_command}")

            # Lógica para processar o comando recebido do cliente
            if received_command.lower() == 'exit':
                print(f"[*] Cliente {addr[0]}:{addr[1]} solicitou encerramento.")
                client_socket.send(b"Saindo da sessão...\n")
                break
            elif received_command:
                # Aqui você pode adicionar sua lógica para o que o servidor deve fazer
                # com o comando recebido do cliente.
                # Por exemplo, se o cliente enviou "uptime", o servidor pode executar
                # "uptime" em si mesmo e enviar a saída de volta.
                # Ou, se este é um C2, o cliente enviaria a SAÍDA de um comando que ele executou.

                # Para esta versão, o servidor simplesmente confirma que recebeu o comando.
                response_to_client = f"Servidor recebeu seu comando: '{received_command}'\n"
                client_socket.send(response_to_client.encode())
            else:
                # Se nenhum comando significativo foi enviado (ex: apenas um keep-alive vazio),
                # ou se o cliente está apenas conectado sem enviar nada por um tempo.
                time.sleep(0.1) # Pequeno delay para evitar loop de CPU intenso

    except Exception as e:
        print(f"[*] Erro na comunicação com {addr[0]}:{addr[1]}: {e}")
    finally:
        print(f"[*] Conexão com {addr[0]}:{addr[1]} fechada.")
        client_socket.close()

# --- Função para iniciar o servidor ---
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reuso do endereço, útil para reiniciar o servidor rapidamente
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
```
