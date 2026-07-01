"""Arena — çok oyunlu oyun platformu çekirdeği.

Ben Kimim? dışındaki tüm oyunlar bu çekirdek üzerinden çalışır.
main.py, "join" mesajında "game" alanı görürse bağlantıyı buraya devreder.

Yeni oyun eklemek için:
1. server/games/<oyun>.py oluştur
2. BaseGame'den türet, GAME_TYPE tanımla, @register_game ile işaretle
3. client/<oyun>/ klasörüne istemciyi koy (hub'a kart eklemeyi unutma)

Ortak protokol (istemci → sunucu):
    {type: "join", game, playerName, roomCode?, avatar?}
    {type: "start_game", ...oyuna özel seçenekler}   (sadece host, lobide)
    {type: "restart"}                                 (sadece host, oyun bitince)
    {type: "chat", text}
    diğer her type → oyunun on_message'ına gider

Ortak protokol (sunucu → istemci):
    {type: "welcome", playerId, roomCode, game, isHost}
    {type: "lobby_update", players: [{id, name, avatar, isHost}], state,
     minPlayers, maxPlayers, game}
    {type: "chat", playerId, playerName, avatar, text}
    {type: "player_left", playerId, playerName}
    {type: "error", message}
    oyuna özel mesajlar oyun sınıfından broadcast/send ile gider
"""
from __future__ import annotations

import json
import random
import string
import uuid

GAME_REGISTRY: dict[str, type] = {}


def register_game(cls):
    """Oyun sınıfını platforma kaydeder (decorator)."""
    GAME_REGISTRY[cls.GAME_TYPE] = cls
    return cls


class ArenaPlayer:
    """Arena odasındaki bir oyuncu."""

    def __init__(self, player_id: str, name: str, ws, avatar: str = "🙂"):
        self.id = player_id
        self.name = name
        self.ws = ws
        self.avatar = avatar

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "avatar": self.avatar}

    async def send(self, data: dict):
        try:
            await self.ws.send(json.dumps(data))
        except Exception:
            pass  # bağlantı kopmuş olabilir


class ArenaRoom:
    """Bir arena odası: oyuncular + aktif oyun örneği."""

    LOBBY = "lobby"
    PLAYING = "playing"
    FINISHED = "finished"

    def __init__(self, code: str, game_cls: type):
        self.code = code
        self.state = self.LOBBY
        self.players: dict[str, ArenaPlayer] = {}
        self.order: list[str] = []  # katılım sırası (oyunlar tur sırası için kullanabilir)
        self.host_id: str | None = None
        self.game_type: str = game_cls.GAME_TYPE
        self.game: BaseGame = game_cls(self)

    @property
    def host(self) -> ArenaPlayer | None:
        return self.players.get(self.host_id) if self.host_id else None

    def add_player(self, player: ArenaPlayer):
        self.players[player.id] = player
        self.order.append(player.id)
        if self.host_id is None:
            self.host_id = player.id

    def remove_player(self, player_id: str):
        self.players.pop(player_id, None)
        if player_id in self.order:
            self.order.remove(player_id)
        if self.host_id == player_id:
            self.host_id = self.order[0] if self.order else None

    def ordered_players(self) -> list[ArenaPlayer]:
        return [self.players[pid] for pid in self.order if pid in self.players]

    async def broadcast(self, data: dict, exclude: str | None = None):
        raw = json.dumps(data)
        for p in self.players.values():
            if p.id == exclude:
                continue
            try:
                await p.ws.send(raw)
            except Exception:
                pass

    def lobby_payload(self) -> dict:
        return {
            "type": "lobby_update",
            "game": self.game_type,
            "state": self.state,
            "players": [
                {**p.to_dict(), "isHost": p.id == self.host_id}
                for p in self.ordered_players()
            ],
            "minPlayers": self.game.MIN_PLAYERS,
            "maxPlayers": self.game.MAX_PLAYERS,
        }

    async def send_lobby(self):
        await self.broadcast(self.lobby_payload())


class BaseGame:
    """Tüm arena oyunlarının temel sınıfı."""

    GAME_TYPE = "base"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 2

    def __init__(self, room: ArenaRoom):
        self.room = room

    async def on_start(self, options: dict):
        """Host oyunu başlattığında çağrılır. Başlangıç durumunu kur ve yayınla."""

    async def on_message(self, player: ArenaPlayer, data: dict):
        """Ortak protokol dışındaki her mesaj buraya gelir."""

    async def on_leave(self, player: ArenaPlayer):
        """Oyuncu ayrıldığında çağrılır (oyuncu odadan çıkarıldıktan SONRA)."""

    def finish(self):
        """Oyun bittiğinde çağır — oda 'finished' durumuna geçer, host restart atabilir."""
        self.room.state = ArenaRoom.FINISHED


# ── Oda / oturum yönetimi ───────────────────────────────────────────

rooms: dict[str, ArenaRoom] = {}
_sessions: dict = {}  # websocket -> (room_code, player_id)


def is_arena_ws(ws) -> bool:
    return ws in _sessions


def _new_room_code() -> str:
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=4))
        if code not in rooms:
            return code


async def _error(ws, message: str):
    try:
        await ws.send(json.dumps({"type": "error", "message": message}))
    except Exception:
        pass


async def handle_join(ws, data: dict):
    game_type = (data.get("game") or "").strip()
    game_cls = GAME_REGISTRY.get(game_type)
    if game_cls is None:
        await _error(ws, f"Bilinmeyen oyun: {game_type}")
        return

    name = (data.get("playerName") or "").strip()[:20]
    if not name:
        await _error(ws, "İsim boş olamaz.")
        return

    avatar = (data.get("avatar") or "🙂").strip()[:8]
    room_code = (data.get("roomCode") or "").strip().upper()

    if room_code:
        room = rooms.get(room_code)
        if room is None:
            await _error(ws, f"Oda bulunamadı: {room_code}")
            return
        if room.game_type != game_type:
            await _error(ws, "Bu oda başka bir oyun için açılmış.")
            return
        if room.state != ArenaRoom.LOBBY:
            await _error(ws, "Oyun çoktan başladı — yeni tur için bekleyin.")
            return
        if len(room.players) >= room.game.MAX_PLAYERS:
            await _error(ws, "Oda dolu.")
            return
    else:
        room = ArenaRoom(_new_room_code(), game_cls)
        rooms[room.code] = room

    player = ArenaPlayer(uuid.uuid4().hex[:8], name, ws, avatar)
    room.add_player(player)
    _sessions[ws] = (room.code, player.id)

    await player.send({
        "type": "welcome",
        "playerId": player.id,
        "roomCode": room.code,
        "game": room.game_type,
        "isHost": room.host_id == player.id,
    })
    await room.send_lobby()
    print(f"[arena:{room.game_type}] {player.name} → oda {room.code} ({len(room.players)} oyuncu)")


async def handle_message(ws, data: dict):
    session = _sessions.get(ws)
    if not session:
        return
    room_code, player_id = session
    room = rooms.get(room_code)
    if room is None:
        return
    player = room.players.get(player_id)
    if player is None:
        return

    msg_type = data.get("type")

    if msg_type == "start_game":
        if player.id != room.host_id:
            await _error(ws, "Sadece host oyunu başlatabilir.")
            return
        if room.state == ArenaRoom.PLAYING:
            return
        if len(room.players) < room.game.MIN_PLAYERS:
            await _error(ws, f"En az {room.game.MIN_PLAYERS} oyuncu gerekli.")
            return
        room.state = ArenaRoom.PLAYING
        await room.game.on_start(data)
        print(f"[arena:{room.game_type}] oda {room.code} başladı ({len(room.players)} oyuncu)")

    elif msg_type == "restart":
        if player.id != room.host_id:
            await _error(ws, "Sadece host yeni oyun başlatabilir.")
            return
        if room.state != ArenaRoom.FINISHED:
            return
        room.game = GAME_REGISTRY[room.game_type](room)
        room.state = ArenaRoom.PLAYING
        await room.game.on_start(data)
        print(f"[arena:{room.game_type}] oda {room.code} yeni oyun")

    elif msg_type == "chat":
        text = (data.get("text") or "").strip()[:200]
        if text:
            await room.broadcast({
                "type": "chat",
                "playerId": player.id,
                "playerName": player.name,
                "avatar": player.avatar,
                "text": text,
            })

    else:
        await room.game.on_message(player, data)


async def handle_disconnect(ws):
    session = _sessions.pop(ws, None)
    if not session:
        return
    room_code, player_id = session
    room = rooms.get(room_code)
    if room is None:
        return
    player = room.players.get(player_id)
    room.remove_player(player_id)

    if not room.players:
        del rooms[room_code]
        print(f"[arena:{room.game_type}] oda {room_code} boşaldı, silindi")
        return

    if player:
        await room.broadcast({
            "type": "player_left",
            "playerId": player.id,
            "playerName": player.name,
        })
    await room.send_lobby()
    if player:
        await room.game.on_leave(player)
