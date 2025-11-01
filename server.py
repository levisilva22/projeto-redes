import socket
import threading
from datetime import datetime

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # {conn: {"username": "nome", "address": addr}}
        self.running = False
    
    def start_server(self):
        """Inicia o servidor de chat"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        
        self.running = True
        print(f"[SERVIDOR] Ouvindo em {self.host}:{self.port}")
        print("[SERVIDOR] Aguardando conexões...")
        
        try:
            while self.running:
                conn, addr = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            self.shutdown()
    
    def handle_client(self, conn, addr):
        """Gerencia a comunicação com um cliente específico"""
        try:
            # Solicita nome de usuário
            conn.send("NOME".encode('utf-8'))
            username = conn.recv(1024).decode('utf-8').strip()
            
            if not username:
                username = f"Usuario_{addr[1]}"
            
            # Adiciona cliente à lista
            self.clients[conn] = {
                "username": username,
                "address": addr
            }
            
            # Notifica todos sobre novo usuário
            self.broadcast(f"[SISTEMA] {username} entrou no chat!", conn)
            print(f"[CONEXÃO] {username} ({addr}) conectou-se. Total: {len(self.clients)}")
            
            conn.send(f"[SISTEMA] Bem-vindo(a) ao chat, {username}!".encode('utf-8'))
            
            # Loop principal de mensagens
            while self.running:
                message = conn.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                if message.upper() == '/SAIR':
                    break
                elif message.upper() == '/USUARIOS':
                    users = ", ".join([client["username"] for client in self.clients.values()])
                    conn.send(f"[SISTEMA] Usuários online: {users}".encode('utf-8'))
                else:
                    # Encaminha mensagem para todos
                    formatted_msg = f"[{datetime.now().strftime('%H:%M')}] {username}: {message}"
                    self.broadcast(formatted_msg, conn)
                    print(formatted_msg)
        
        except Exception as e:
            print(f"[ERRO] Com cliente {addr}: {e}")
        finally:
            self.remove_client(conn, username)
    
    def broadcast(self, message, sender_conn=None):
        """Envia mensagem para todos os clientes, exceto o remetente"""
        disconnected_clients = []
        
        for client_conn in self.clients.keys():
            if client_conn != sender_conn:
                try:
                    client_conn.send(message.encode('utf-8'))
                except:
                    disconnected_clients.append(client_conn)
        
        # Remove clientes desconectados
        for client in disconnected_clients:
            self.remove_client(client)
    
    def remove_client(self, conn, username=None):
        """Remove cliente da lista e notifica os demais"""
        if conn in self.clients:
            if not username:
                username = self.clients[conn]["username"]
            
            del self.clients[conn]
            try:
                conn.close()
            except:
                pass
            
            leave_msg = f"[SISTEMA] {username} saiu do chat."
            self.broadcast(leave_msg)
            print(leave_msg)
            print(f"[INFO] Total de usuários: {len(self.clients)}")
    
    def shutdown(self):
        """Encerra o servidor graciosamente"""
        print("\n[SERVIDOR] Encerrando...")
        self.running = False
        self.broadcast("[SISTEMA] Servidor está sendo encerrado!")
        
        for conn in list(self.clients.keys()):
            self.remove_client(conn)
        
        if self.server_socket:
            self.server_socket.close()
        print("[SERVIDOR] Encerrado.")

if __name__ == "__main__":
    server = ChatServer()
    server.start_server()