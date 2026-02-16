from network import NetworkServer
import time

print("Starting virtual coworking space server...")
print("Server will accept up to 2 clients on localhost:5555")
print("Press Ctrl+C to stop")

server = NetworkServer()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down server...")
    server.shutdown()
    print("Server stopped")