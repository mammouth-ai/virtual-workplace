import socket
import threading
import json
import time

HOST = '127.0.0.1'
PORT = 5555

class NetworkServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(2)
        self.clients = []
        self.players = {}
        self.running = True
        
        self.thread = threading.Thread(target=self.accept_clients)
        self.thread.daemon = True
        self.thread.start()
    
    def accept_clients(self):
        while self.running and len(self.clients) < 2:
            try:
                client, addr = self.server.accept()
                print(f"Client connected: {addr}")
                player_id = len(self.clients) + 1
                self.clients.append((client, addr, player_id))
                
                thread = threading.Thread(target=self.handle_client, args=(client, player_id))
                thread.daemon = True
                thread.start()
                
                self.players[player_id] = {"x": 100 * player_id, "y": 100 * player_id, "chat": ""}
                
            except Exception as e:
                print(f"Error accepting client: {e}")
    
    def handle_client(self, client, player_id):
        try:
            welcome = json.dumps({"player_id": player_id})
            client.send(welcome.encode('utf-8'))
        except Exception as e:
            print(f"Error sending welcome to client {player_id}: {e}")
            client.close()
            self.remove_client(player_id)
            return
        
        while self.running:
            try:
                data = client.recv(1024).decode('utf-8')
                if not data:
                    break
                
                try:
                    received = json.loads(data)
                    self.players[player_id]["x"] = received.get("x", self.players[player_id]["x"])
                    self.players[player_id]["y"] = received.get("y", self.players[player_id]["y"])
                    self.players[player_id]["chat"] = received.get("chat", "")
                    
                    response = {"player_id": player_id, "players": self.players}
                    client.send(json.dumps(response).encode('utf-8'))
                except json.JSONDecodeError:
                    pass
                    
            except Exception as e:
                print(f"Error handling client {player_id}: {e}")
                break
        
        client.close()
        self.remove_client(player_id)
    
    def remove_client(self, player_id):
        self.players.pop(player_id, None)
        self.clients = [c for c in self.clients if c[2] != player_id]
        print(f"Player {player_id} disconnected")
    
    def shutdown(self):
        self.running = False
        for client, _, _ in self.clients:
            client.close()
        self.server.close()

class NetworkClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.player_id = 0
        self.players = {}
    
    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
            self.connected = True
            
            welcome_data = self.sock.recv(1024).decode('utf-8')
            if welcome_data:
                welcome = json.loads(welcome_data)
                self.player_id = welcome.get("player_id", 0)
                print(f"Connected as Player {self.player_id}")
            
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def send_update(self, x, y, chat=""):
        if not self.connected:
            return {}
        
        try:
            data = json.dumps({"x": x, "y": y, "chat": chat})
            self.sock.send(data.encode('utf-8'))
            
            response = self.sock.recv(1024).decode('utf-8')
            if response:
                data = json.loads(response)
                self.players = data.get("players", {})
                return self.players
        except Exception as e:
            print(f"Send error: {e}")
            self.connected = False
        
        return {}