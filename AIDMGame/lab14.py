from __future__ import annotations

import argparse
import http.server
import json
import os
import random
import sqlite3
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, List, Set
import uuid

# Add the parent directory to sys.path to import utils
sys.path.insert(0, os.path.dirname(__file__))

from utils.base import DungeonMaster
from character_parser import parse_character_updates


# Global state for broadcasting player updates to listening clients
listening_clients: Dict[str, Set] = {}  # session_id -> set of response write functions
listening_lock = threading.Lock()


@dataclass
class PlayerCharacter:
    name: str
    character_class: str = "Fighter"
    level: int = 1
    health: int = 100
    max_health: int = 100
    strength: int = 15
    dexterity: int = 12
    constitution: int = 14
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    experience: int = 0
    inventory: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "character_class": self.character_class,
            "level": self.level,
            "health": self.health,
            "max_health": self.max_health,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,
            "experience": self.experience,
            "inventory": self.inventory
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerCharacter':
        return cls(**data)


@dataclass
class Player:
    name: str
    player_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    character: PlayerCharacter = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "player_id": self.player_id,
            "character": self.character.to_dict() if self.character else None
        }


class GameSession:
    def __init__(self, name: str, max_players: int = 4):
        self.session_id = str(uuid.uuid4())
        self.name = name
        self.max_players = max_players
        self.players: List[Player] = []
        self.game_log: List[str] = []
        self.world_state: Dict = {'enemies': {'goblin': {'health': 50, 'max_health': 50}}}
        self.current_turn: int = 0
        self.in_combat: bool = False
        self.combat_state: Dict = {'players': {}, 'enemies': {'goblin': {'health': 50}}}
        self.dm = DungeonMaster()
        self.dm_processing = False  # Lock to prevent concurrent DM calls
        self.dm_lock = threading.Lock()  # Thread lock for DM processing

    def add_player(self, player: Player) -> None:
        if self.is_full():
            raise ValueError(f"Session '{self.name}' is full.")
        if any(existing.name == player.name for existing in self.players):
            raise ValueError(f"Player with name '{player.name}' already joined.")
        self.players.append(player)
        self.combat_state['players'][player.name] = {'health': 100, 'max_health': 100}

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


class CharacterDB:
    def __init__(self, db_path="ai_dm.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        # Create table in main thread
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                player_id TEXT PRIMARY KEY,
                data TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def save_character(self, player_id, character):
        with self.lock:
            conn = self._get_connection()
            try:
                data = json.dumps(character.to_dict())
                conn.execute('INSERT OR REPLACE INTO characters (player_id, data) VALUES (?, ?)', (player_id, data))
                conn.commit()
            finally:
                conn.close()

    def load_character(self, player_id):
        with self.lock:
            conn = self._get_connection()
            try:
                cursor = conn.execute('SELECT data FROM characters WHERE player_id = ?', (player_id,))
                row = cursor.fetchone()
                if row:
                    return PlayerCharacter.from_dict(json.loads(row[0]))
                return None
            finally:
                conn.close()


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}
        self.db = CharacterDB()

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
        player.character = PlayerCharacter(name=player_name)
        loaded = self.db.load_character(player.player_id)
        if loaded:
            player.character = loaded
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

        if path.startswith("/sessions/") and path.endswith("/log"):
            session_id = path.split("/")[2]
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            player_id = query.get('player_id', [None])[0]
            try:
                session = self.manager.get_session(session_id)
                player = None
                if player_id:
                    player = next((p for p in session.players if p.player_id == player_id), None)
                self._send_json(200, {"game_log": session.game_log, "player_character": player.character.to_dict() if player and player.character else None})
            except ValueError:
                self._send_json(404, {"error": "Session not found"})
            return

        if path == "/ui":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Dungeon Master</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        #chat { border: 1px solid #ccc; height: 300px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        input, button { margin: 5px; }
        #loading { display: none; color: blue; margin: 5px; }
        button:disabled, input:disabled { opacity: 0.5; }
    </style>
</head>
<body>
    <h1>AI Dungeon Master Game</h1>
    <div id="join-form">
        <h2>Available Sessions</h2>
        <div id="session-list"></div>
        <input type="text" id="player-name" placeholder="Player Name">
        <button onclick="joinSession()">Join Selected Session</button>
    </div>
    <div id="game" style="display:none;">
        <div id="chat"></div>
        <div id="loading">AI is thinking...</div>
        <div id="character-sheet"></div>
        <input type="text" id="action" placeholder="Enter action (e.g., explore forest, attack goblin)">
        <button onclick="submitAction()">Submit Action</button>
    </div>
    <script>
        let sessionId = '';
        let playerId = '';
        let lastLogLength = 0;
        let waitingForDM = false;  // Track if we're waiting for DM response

        async function loadSessions() {
            try {
                const response = await fetch('/sessions');
                const data = await response.json();
                if (response.ok) {
                    const list = document.getElementById('session-list');
                    list.innerHTML = '';
                    data.sessions.forEach(session => {
                        const div = document.createElement('div');
                        div.innerHTML = `
                            <input type="radio" name="session" value="${session.session_id}" id="session-${session.session_id}">
                            <label for="session-${session.session_id}">
                                ${session.name} (${session.session_id}) - ${session.players.length}/${session.max_players} players
                            </label>
                        `;
                        list.appendChild(div);
                    });
                } else {
                    document.getElementById('session-list').textContent = 'Failed to load sessions';
                }
            } catch (error) {
                document.getElementById('session-list').textContent = 'Error loading sessions: ' + error;
            }
        }

        async function joinSession() {
            const selected = document.querySelector('input[name="session"]:checked');
            if (!selected) {
                alert('Please select a session');
                return;
            }
            sessionId = selected.value;
            const playerName = document.getElementById('player-name').value;
            if (!playerName) {
                alert('Please enter player name');
                return;
            }
            try {
                const response = await fetch(`/sessions/${sessionId}/join`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                    body: JSON.stringify({ player_name: playerName })
                });
                const data = await response.json();
                if (response.ok) {
                    playerId = data.player_id;
                    document.getElementById('join-form').style.display = 'none';
                    document.getElementById('game').style.display = 'block';
                    pollLog();
                } else {
                    alert('Join failed: ' + data.error);
                }
            } catch (error) {
                alert('Error: ' + error);
            }
        }

        async function submitAction() {
            const action = document.getElementById('action').value;
            if (!action) return;
            
            // Set waiting state
            waitingForDM = true;
            
            // Disable input and button, show loading
            document.getElementById('action').disabled = true;
            document.querySelector('button[onclick="submitAction()"]').disabled = true;
            document.getElementById('loading').style.display = 'block';
            document.getElementById('loading').textContent = 'Sending action...';
            
            try {
                const response = await fetch(`/sessions/${sessionId}/action`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ player_id: playerId, action: action })
                });
                const data = await response.json();
                if (response.ok) {
                    document.getElementById('action').value = '';
                    if (data.status === 'waiting') {
                        // Another player is being processed
                        document.getElementById('loading').textContent = 'DM is responding to another player...';
                    } else {
                        // Action accepted, waiting for DM
                        document.getElementById('loading').textContent = 'DM is thinking...';
                    }
                    // UI will re-enable automatically when DM response arrives via polling
                } else {
                    alert('Action failed: ' + data.error);
                    waitingForDM = false;
                    document.getElementById('action').disabled = false;
                    document.querySelector('button[onclick="submitAction()"]').disabled = false;
                    document.getElementById('loading').style.display = 'none';
                }
            } catch (error) {
                alert('Error: ' + error);
                waitingForDM = false;
                document.getElementById('action').disabled = false;
                document.querySelector('button[onclick="submitAction()"]').disabled = false;
                document.getElementById('loading').style.display = 'none';
            }
        }

        async function pollLog() {
            try {
                const response = await fetch(`/sessions/${sessionId}/log?player_id=${playerId}`);
                const data = await response.json();
                if (response.ok) {
                    const chat = document.getElementById('chat');
                    const currentLength = data.game_log.length;
                    
                    // Check if new messages arrived
                    if (currentLength > lastLogLength) {
                        const newMessages = data.game_log.slice(lastLogLength);
                        newMessages.forEach(msg => {
                            const p = document.createElement('p');
                            p.textContent = msg;
                            chat.appendChild(p);
                        });
                        lastLogLength = currentLength;
                        chat.scrollTop = chat.scrollHeight;
                        
                        // If we were waiting for DM and got a DM response, re-enable input
                        if (waitingForDM && newMessages.some(msg => msg.startsWith('DM:'))) {
                            waitingForDM = false;
                            document.getElementById('action').disabled = false;
                            document.querySelector('button[onclick="submitAction()"]').disabled = false;
                            document.getElementById('loading').style.display = 'none';
                        }
                    }
                    
                    updateCharacterSheet(data);
                }
            } catch (error) {
                console.error('Poll error:', error);
            }
            setTimeout(pollLog, 500);  // Poll every 0.5 seconds for very responsive UI
        }

        function updateCharacterSheet(data) {
            const sheet = document.getElementById('character-sheet');
            if (data.player_character) {
                const c = data.player_character;
                sheet.innerHTML = `
                    <h3>Character Sheet</h3>
                    <p>Name: ${c.name}</p>
                    <p>Class: ${c.character_class} Level ${c.level}</p>
                    <p>Health: ${c.health}/${c.max_health}</p>
                    <p>STR: ${c.strength} DEX: ${c.dexterity} CON: ${c.constitution}</p>
                    <p>INT: ${c.intelligence} WIS: ${c.wisdom} CHA: ${c.charisma}</p>
                    <p>Experience: ${c.experience}</p>
                    <p>Inventory: ${c.inventory.join(', ')}</p>
                `;
            } else {
                sheet.innerHTML = '';
            }
        }

        // Load sessions on page load
        window.onload = loadSessions;
    </script>
</body>
</html>
            """
            self.wfile.write(html.encode())
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
            except ValueError as error:
                self._send_json(400, {"error": str(error)})
                return
            print(f"Player '{player.name}' joined session '{session.name}' ({session.session_id}).")
            print(f"Session now has {len(session.players)}/{session.max_players} players.")
            
            if self.headers.get("Accept") == "application/json":
                # Non-streaming join for UI
                self._send_json(200, {"player_id": player.player_id})
                return
            
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
            
            # If first player, send initial DM message
            if len(session.players) == 1:
                session.dm.game_log = session.game_log
                dm_response = session.dm.dm_turn_hook()
                session.game_log.append(f"DM: {dm_response}")
                initial_msg = {
                    "type": "initial_dm",
                    "dm_response": dm_response
                }
                self.wfile.write((json.dumps(initial_msg) + "\n").encode("utf-8"))
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

        if path.startswith("/sessions/") and path.endswith("/action"):
            session_id = path.split("/")[2]
            payload = self._read_json()
            player_id = payload.get("player_id")
            action = payload.get("action")
            if not player_id or not action:
                self._send_json(400, {"error": "player_id and action required"})
                return
            try:
                session = self.manager.get_session(session_id)
            except ValueError as error:
                self._send_json(400, {"error": str(error)})
                return
            player = next((p for p in session.players if p.player_id == player_id), None)
            if not player:
                self._send_json(400, {"error": "Player not in session"})
                return
            
            # Check if DM is already processing
            if session.dm_processing:
                self._send_json(200, {"status": "waiting", "message": "DM is processing another action, please wait"})
                return
            
            # Acquire lock for DM processing
            with session.dm_lock:
                session.dm_processing = True
                
                # Broadcast that DM is thinking to ALL players
                thinking_msg = {
                    "type": "dm_thinking",
                    "player_name": player.name,
                    "action": action
                }
                broadcast_to_session(session_id, thinking_msg)
                
                try:
                    # Parse and update character based on action
                    character_modified = parse_character_updates(action, player.character)
                    
                    # Process action
                    session.game_log.append(f"{player.name}: {action}")
                    dm_response = ""
                    update_type = "narrative_update"
                    if action.lower().startswith("attack"):
                        # Combat action
                        target = action.split()[1] if len(action.split()) > 1 else "goblin"
                        if target in session.combat_state['enemies']:
                            damage = random.randint(5, 15)
                            session.combat_state['enemies'][target]['health'] -= damage
                            dm_response = f"You attack the {target} for {damage} damage."
                            if session.combat_state['enemies'][target]['health'] <= 0:
                                dm_response += f" The {target} is defeated!"
                                session.in_combat = False
                            update_type = "combat_update"
                        else:
                            dm_response = f"No enemy named {target} found."
                            update_type = "combat_update"
                    else:
                        # Narrative action - THIS IS WHERE DM THINKS
                        session.dm.game_log = session.game_log
                        dm_response = session.dm.dm_turn_hook()
                    session.game_log.append(f"DM: {dm_response}")
                    
                    # Always save character after action
                    for p in session.players:
                        if p.player_id == player_id:
                            p.character.health = session.combat_state['players'][p.name]['health']
                            self.manager.db.save_character(p.player_id, p.character)
                            print(f"[DB] Saved character for {p.name}: Class={p.character.character_class}, Health={p.character.health}")
                            break
                    
                    # Broadcast update to ALL players
                    update_msg = {
                        "type": update_type,
                        "action": action,
                        "player_name": player.name,
                        "dm_response": dm_response,
                        "combat_state": session.combat_state if update_type == "combat_update" else None
                    }
                    broadcast_to_session(session_id, update_msg)
                    
                finally:
                    # Release lock
                    session.dm_processing = False
            
            self._send_json(200, {"status": "action processed"})

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
                    
                elif msg_type == "narrative_update":
                    print(f"\n{msg.get('player_name')}: {msg.get('action')}")
                    print(f"DM: {msg.get('dm_response')}")
                    
                elif msg_type == "combat_update":
                    print(f"\n{msg.get('player_name')}: {msg.get('action')}")
                    print(f"DM: {msg.get('dm_response')}")
                    combat_state = msg.get('combat_state')
                    if combat_state:
                        print("Combat State:")
                        for p, stats in combat_state.get('players', {}).items():
                            print(f"  {p}: {stats['health']}/100 HP")
                        for e, stats in combat_state.get('enemies', {}).items():
                            print(f"  {e}: {stats['health']} HP")
                    
                elif msg_type == "initial_dm":
                    print(f"DM: {msg.get('dm_response')}")
                    
                else:
                    print(f"[{msg_type}] {msg}")
                    
            except json.JSONDecodeError:
                pass
                
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        raise RuntimeError(f"Failed to join session: {body}") from error


def remote_submit_action(host: str, port: int, session_id: str, player_id: str, action: str) -> None:
    """Submit an action to a session."""
    url = f"http://{host}:{port}/sessions/{session_id}/action"
    payload = json.dumps({"player_id": player_id, "action": action}).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"Action submitted: {result}")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        print(f"Failed to submit action: {body}")


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

    action_parser = subparsers.add_parser("action", help="Submit an action to a session")
    action_parser.add_argument("--host", default="localhost", help="Server host")
    action_parser.add_argument("--port", type=int, default=8000, help="Server port")
    action_parser.add_argument("--session-id", required=True, help="Session ID")
    action_parser.add_argument("--player-id", required=True, help="Player ID")
    action_parser.add_argument("--action", required=True, help="Action text")

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

    if args.command == "action":
        remote_submit_action(host=args.host, port=args.port, session_id=args.session_id, player_id=args.player_id, action=args.action)
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
