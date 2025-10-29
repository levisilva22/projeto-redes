import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = False
        self.username = ""
    
    def start_client(self):
        """Inicia o cliente de chat"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))

            # Recebe solicitação de nome
            message = self.client_socket.recv(1024).decode('utf-8')
            if message == "NOME":
                self.username = input("Digite seu nome de usuário: ")
                self.client_socket.send(self.username.encode('utf-8'))

            self.running = True

            # Thread para receber mensagens
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            # Loop principal para enviar mensagens
            self.send_messages()

        except Exception as e:
            print(f"[ERRO] Não foi possível conectar ao servidor: {e}")
        finally:
            self.disconnect()
    
    def receive_messages(self):
        """Recebe mensagens do servidor em uma thread separada"""
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    print("[SISTEMA] Conexão com o servidor perdida.")
                    self.running = False
                    break
                else:
                    print(message)
            
            except:
                print("[SISTEMA] Erro ao receber mensagens.")
                self.running = False
                break
    
    def send_messages(self):
        """Envia mensagens para o servidor"""
        print("\nComandos disponíveis:")
        print("/sair - Sair do chat")
        print("/usuarios - Listar usuários online")
        print("Digite sua mensagem e pressione Enter para enviar\n")
        
        while self.running:
            try:
                message = input()
                
                if not self.running:
                    break
                
                if message.upper() == '/SAIR':
                    self.client_socket.send('/SAIR'.encode('utf-8'))
                    break
                elif message.upper() == '/USUARIOS':
                    self.client_socket.send('/USUARIOS'.encode('utf-8'))
                else:
                    self.client_socket.send(message.encode('utf-8'))
            
            except KeyboardInterrupt:
                print("\n[SISTEMA] Saindo...")
                break
            except Exception as e:
                print(f"[ERRO] Erro ao enviar mensagem: {e}")
                break
    
    def disconnect(self):
        """Desconecta do servidor"""
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        print("[SISTEMA] Desconectado.")

if __name__ == "__main__":
    # Permite especificar o IP do servidor
    server_ip = input("Digite o IP do servidor (ou Enter para localhost): ").strip()
    if not server_ip:
        server_ip = 'localhost'
    
    client = ChatClient(host=server_ip)
    client.start_client()