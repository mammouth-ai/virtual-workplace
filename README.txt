Virtual Coworking Space (2D Pixel Style)
=========================================

A minimalistic 2D virtual coworking space where two players can connect and chat when they are close on the map.

Features:
- 2D pixel-style grass-covered map
- Two player characters (human heads) with different colors
- Local networking via sockets (localhost)
- Proximity-based chat: see chat messages only when players are close
- Quick chat messages (1-4 keys) and custom chat input (T key)
- Real-time player movement with WASD/arrow keys (depending on player)

Files:
- config.py: Configuration constants
- player.py: Player class with movement and drawing
- network.py: Networking server and client classes
- server.py: Server launcher
- game_client.py: Main game client
- main.py: Single-player test version (not needed for multiplayer)
- requirements.txt: Python dependencies (Pygame)

Setup:
1. Ensure Python 3.12+ is installed
2. Create virtual environment (optional): python -m venv venv
3. Activate venv: source venv/bin/activate (Linux/Mac) or venv\Scripts\activate (Windows)
4. Install dependencies: pip install -r requirements.txt

Running:
1. Start the server first (in one terminal):
   python server.py
   This will listen on localhost:5555 for up to 2 clients.

2. Run the first client (in another terminal):
   python game_client.py
   This will connect as Player 1 (red head). Use WASD to move.

3. Run the second client (in a third terminal):
   python game_client.py
   This will connect as Player 2 (blue head). Use arrow keys to move.

Controls:
- Player 1: WASD to move, 1-4 for quick messages, T to type custom chat
- Player 2: Arrow keys to move, 1-4 for quick messages, T to type custom chat
- When players are within the chat radius (white circle), chat messages become visible
- Custom chat: Press T, type your message, press Enter to send, Esc to cancel

Network:
- The server must be running before clients connect
- Both clients must run on the same machine (localhost)
- If server is not running, clients will fail to connect

Notes:
- This is a minimal implementation for demonstration
- Graphics are simple pixel-style circles and grass pattern
- Chat messages disappear after a few seconds
- Enjoy your virtual coworking space!