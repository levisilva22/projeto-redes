# 💬 Chat em Python - Projeto de Redes

Um sistema de chat simples implementado em Python usando sockets TCP, permitindo comunicação em tempo real entre múltiplos clientes através de uma rede local.

## 📋 Funcionalidades

- ✅ **Múltiplos usuários** simultâneos
- ✅ **Mensagens em tempo real** com timestamp
- ✅ **Comandos especiais** (`/usuarios`, `/sair`)
- ✅ **Notificações** de entrada/saída de usuários
- ✅ **Comunicação entre computadores** diferentes na mesma rede

## 🚀 Como Executar

### Pré-requisitos

- Python 3.6 ou superior
- Computadores na mesma rede local (WiFi/Ethernet)

### 1. **Executar o Servidor**

No computador que será o servidor:

```bash
# Clone ou baixe os arquivos do projeto
cd projeto-redes

# Execute o servidor
python3 server.py
```

O servidor iniciará e mostrará:
```
[SERVIDOR] Ouvindo em 0.0.0.0:5555
[SERVIDOR] Aguardando conexões...
```

### 2. **Descobrir o IP do Servidor**

No computador servidor, execute:

```bash
# Descobrir o IP da máquina
ifconfig
# ou
ip addr show
```

Procure pela interface de rede ativa (geralmente `wlp0s20f3` para WiFi ou `eth0` para cabo). 
O IP será algo como: `192.168.1.100` ou `172.172.22.210`

### 3. **Conectar Clientes**

No(s) computador(es) cliente(s):

```bash
# Execute o cliente
python3 client.py
```

Quando solicitado, digite:
- **IP do servidor:** o IP descoberto no passo anterior (ex: `172.172.22.210`)
- **Nome de usuário:** seu nome no chat

## 🌐 Configuração de Rede

### Firewall (Ubuntu/Linux)

Se estiver usando firewall, libere a porta 5555:

```bash
# Ativar firewall e liberar porta
sudo ufw enable
sudo ufw allow 5555

# Verificar status
sudo ufw status
```



## 📝 Comandos do Chat

Uma vez conectado, você pode usar:

- **Mensagem normal:** Digite e pressione Enter
- **`/usuarios`:** Lista todos os usuários online
- **`/sair`:** Sair do chat
- **`Ctrl+C`:** Forçar saída



## 🔧 Arquivos Principais

### `connection.py` - Servidor
- Gerencia múltiplas conexões simultâneas
- Retransmite mensagens entre clientes
- Controla entrada/saída de usuários
- Porta padrão: **5555**

### `client.py` - Cliente
- Interface de usuário para o chat
- Conexão com servidor remoto
- Threads separadas para envio/recepção

## 🐛 Solução de Problemas

### Erro: "Conexão recusada"
- ✅ Servidor está executando?
- ✅ IP correto?
- ✅ Mesma rede?
- ✅ Firewall liberado?


## 👥 Autores

Desenvolvido por **Levi Farias**, **Lucas Beelen** e **Matheus Almeida** como projeto de aprendizado de redes e sockets em Python.

---

🚀 **Divirta-se chatando!**