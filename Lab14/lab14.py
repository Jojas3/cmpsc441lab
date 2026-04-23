from __future__ import annotations

import argparse
import http.server
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, List, Set
import uuid


# Global state for broadcasting player updates to listening clients
listening_clients: Dict[str, Set] = {}  # session_id -> set of response write functions
listening_lock = threading.Lock()


@dataclass
class Player:
    name: str
    player_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return {"name": self.name, "player_id": self.player_id}


class GameSession:
    def __init__(self, name: str, max_players: int = 4):
        self.session_id = str(uuid.uuid4())
        self.name = name
        self.max_players = max_players
        self.players: List[Player] = []

    def add_player(self, player: Player) -> None:
        if self.is_full():
            raise ValueError(f"Session '{self.name}' is full.")
        if any(existing.name == player.name for existing in self.players):
            raise ValueError(f"Player with name '{player.name}' already joined.")
        self.players.append(player)

    def is_full(self) -> bool:
        return len(self.players) >= self.max_players

    def list_player_names(self) -> List[str]:
        return [player.name for player in self.players]

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "name": self.name,
            "max_players": self.max_players,
            "players": [player.to_dict() for player in self.players],
        }

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.session_id}) - "
            f"{len(self.players)}/{self.max_players} players"
        )


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}

    def create_session(self, name: str, max_players: int = 4) -> GameSession:
        session = GameSession(name=name, max_players=max_players)
        self.sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> GameSession:
        try:
            return self.sessions[session_id]
        except KeyError as error:
            raise ValueError(f"No session with id '{session_id}' exists.") from error

    def find_session_by_name(self, name: str) -> GameSession:
        for session in self.sessions.values():
            if session.name.lower() == name.lower():
                return session
        raise ValueError(f"No session with name '{name}' exists.")

    def list_sessions(self) -> List[GameSession]:
        return list(self.sessions.values())

    def join_session(self, session_id: str, player_name: str) -> Player:
        session = self.get_session(session_id)
        player = Player(name=player_name)
        session.add_player(player)
        return player

    def to_dict(self) -> dict:
        return {session_id: session.to_dict() for session_id, session in self.sessions.items()}


def create_default_manager() -> SessionManager:
    manager = SessionManager()
    manager.create_session(name="Forest of Whispers", max_players=4)
    manager.create_session(name="Crypt of Echoes", max_players=3)
    manager.create_session(name="Strange Carnival", max_players=5)
    return manager


def broadcast_to_session(session_id: str, message: dict, exclude_wfile=None) -> None:
    """Send a message to all listening clients in a session."""
    with listening_lock:
        if session_id not in listening_clients:
            return
        msg_bytes = (json.dumps(message) + "\n").encode("utf-8")
        for wfile in list(listening_clients[session_id]):
            if exclude_wfile is not None and wfile is exclude_wfile:
                continue
            try:
                wfile.write(msg_bytes)
                wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                listening_clients[session_id].discard(wfile)


class SessionAPIHandler(http.server.BaseHTTPRequestHandler):
    manager = create_default_manager()

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        data = self.rfile.read(length)
        return json.loads(data.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/sessions":
            sessions = [session.to_dict() for session in self.manager.list_sessions()]
            self._send_json(200, {"sessions": sessions})
            return

        if path.startswith("/sessions/"):
            session_id = path.split("/", 2)[2]
            try:
                session = self.manager.get_session(session_id)
                self._send_json(200, session.to_dict())
            except ValueError as error:
                self._send_json(404, {"error": str(error)})
            return

        self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/sessions":
            payload = self._read_json()
            name = payload.get("name")
            max_players = payload.get("max_players", 4)
            if not name:
                self._send_json(400, {"error": "Session name is required"})
                return
            session = self.manager.create_session(name=name, max_players=max_players)
            self._send_json(201, session.to_dict())
            return

        if path.startswith("/sessions/") and path.endswith("/join"):
            session_id = path.split("/")[2]
            payload = self._read_json()
            player_name = payload.get("player_name")
            if not player_name:
                self._send_json(400, {"error": "player_name is required"})
                return
            try:
                player = self.manager.join_session(session_id, player_name)
                session = self.manager.get_session(session_id)
                print(f"Player '{player.name}' joined session '{session.name}' ({session.session_id}).")
                print(f"Session now has {len(session.players)}/{session.max_players} players.")
                
                # Send streaming response with welcome message and keep connection open
                self.send_response(200)
                self.send_header("Content-Type", "application/x-ndjson")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                
                # Send welcome message
                welcome = {
                    "type": "welcome",
                    "message": f"Welcome {player.name} to {session.name}!",
                    "player_id": player.player_id,
                    "player_name": player.name,
                    "session_id": session_id,
                    "session_name": session.name,
                }
                self.wfile.write((json.dumps(welcome) + "\n").encode("utf-8"))
                self.wfile.flush()
                
                # Register this client as a listener for updates
                with listening_lock:
                    if session_id not in listening_clients:
                        listening_clients[session_id] = set()
                    listening_clients[session_id].add(self.wfile)
                
                # Send current player list
                players_msg = {
                    "type": "player_list",
                    "players": [p.to_dict() for p in session.players],
                }
                self.wfile.write((json.dumps(players_msg) + "\n").encode("utf-8"))
                self.wfile.flush()
                
                # Broadcast join event to all other listening clients
                broadcast_msg = {
                    "type": "player_joined",
                    "player_name": player.name,
                    "player_id": player.player_id,
                    "total_players": len(session.players),
                }
                broadcast_to_session(session_id, broadcast_msg, exclude_wfile=self.wfile)
                
                # Keep connection open and listen for hangup
                try:
                    while True:
                        time.sleep(1)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                finally:
                    # Unregister client on disconnect
                    with listening_lock:
                        if session_id in listening_clients:
                            listening_clients[session_id].discard(self.wfile)
                    print(f"Player '{player.name}' disconnected from session.")
                    
            except ValueError as error:
                self._send_json(400, {"error": str(error)})
            return

        self._send_json(404, {"error": "Endpoint not found"})


    def log_message(self, format: str, *args) -> None:
        print("[SERVER] " + format % args)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    server_address = (host, port)
    httpd = http.server.ThreadingHTTPServer(server_address, SessionAPIHandler)
    print(f"Starting session server on http://{host}:{port}")
    print("Available sessions:")
    for session in SessionAPIHandler.manager.list_sessions():
        print(f"  - {session}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.server_close()


def remote_list_sessions(host: str = "localhost", port: int = 8000) -> list:
    url = f"http://{host}:{port}/sessions"
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))["sessions"]


def remote_join_session(host: str, port: int, session_id: str, player_name: str) -> None:
    """Join a session and listen for streaming updates."""
    url = f"http://{host}:{port}/sessions/{session_id}/join"
    payload = json.dumps({"player_name": player_name}).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        response = urllib.request.urlopen(request)
        print("Connected to session. Listening for updates (Ctrl+C to exit)...\n")
        while True:
            line = response.readline().decode("utf-8").strip()
            if not line:
                break
            try:
                msg = json.loads(line)
                msg_type = msg.get("type", "unknown")
                
                if msg_type == "welcome":
                    print(f"✓ {msg.get('message')}")
                    print(f"  Session: {msg.get('session_name')} ({msg.get('session_id')})")
                    
                elif msg_type == "player_list":
                    players = msg.get("players", [])
                    if players:
                        print(f"\nCurrent players ({len(players)}):")
                        for player in players:
                            print(f"  - {player['name']}")
                    
                elif msg_type == "player_joined":
                    print(f"\n→ {msg.get('player_name')} joined! ({msg.get('total_players')} total)")
                    
                else:
                    print(f"[{msg_type}] {msg}")
                    
            except json.JSONDecodeError:
                pass
                
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        raise RuntimeError(f"Failed to join session: {body}") from error


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Dungeon Master Join Session demo")
    subparsers = parser.add_subparsers(dest="command")

    server_parser = subparsers.add_parser("server", help="Start the join-session server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    server_parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")

    list_parser = subparsers.add_parser("list", help="List available remote sessions")
    list_parser.add_argument("--host", default="localhost", help="Server host")
    list_parser.add_argument("--port", type=int, default=8000, help="Server port")

    join_parser = subparsers.add_parser("join", help="Join a remote session")
    join_parser.add_argument("--host", default="localhost", help="Server host")
    join_parser.add_argument("--port", type=int, default=8000, help="Server port")
    join_parser.add_argument("--session-id", required=True, help="Session ID to join")
    join_parser.add_argument("--player-name", required=True, help="Player name")

    args = parser.parse_args()

    if args.command == "server":
        run_server(host=args.host, port=args.port)
        return

    if args.command == "list":
        sessions = remote_list_sessions(host=args.host, port=args.port)
        print("Available remote sessions:")
        for session in sessions:
            print(f"  - {session['name']} ({session['session_id']}) - {len(session['players'])}/{session['max_players']} players")
        return

    if args.command == "join":
        try:
            remote_join_session(host=args.host, port=args.port, session_id=args.session_id, player_name=args.player_name)
        except RuntimeError as error:
            print(error)
        except KeyboardInterrupt:
            print("\n\nDisconnected from session.")
        return

    manager = create_default_manager()
    print("Welcome to the AI Dungeon Master Join Session demo")
    print("Available game sessions:")
    for session in manager.list_sessions():
        print(f"  - {session}")

    player_name = input("Enter your player name: ").strip()
    session_id = input("Enter the session ID you want to join: ").strip()

    try:
        player = manager.join_session(session_id=session_id, player_name=player_name)
        session = manager.get_session(session_id)
        print(f"\n{player.name} joined session '{session.name}' successfully!")
        print("Current players:")
        for name in session.list_player_names():
            print(f"  - {name}")
    except ValueError as error:
        print(f"Failed to join session: {error}")


if __name__ == "__main__":
    main()
