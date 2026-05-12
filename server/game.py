"""Oyun mantığı — Player, Room sınıfları ve oda yönetimi."""
from __future__ import annotations

import string
import random
import asyncio
import json
from names import get_random_names


class Player:
    """Bir oyuncuyu temsil eder."""

    def __init__(self, player_id: str, name: str, websocket):
        self.id = player_id
        self.name = name
        self.ws = websocket
        self.assigned_name: str | None = None  # kafasındaki isim
        self.revealed: bool = False  # doğru tahmin ettiyse True
        self.rank: int | None = None  # sıralama (1., 2., 3. ...)

    def to_dict(self) -> dict:
        """Lobby için oyuncu bilgisi."""
        return {"id": self.id, "name": self.name}

    def to_game_dict(self, for_player_id: str) -> dict:
        """Oyun ekranı için oyuncu bilgisi.
        Eğer bilgiyi isteyen oyuncunun kendisiyse => '???'
        Eğer açılmışsa (revealed) => gerçek isim
        Diğerleri her zaman gerçek ismi görür.
        """
        if self.revealed:
            shown_name = self.assigned_name
        elif self.id == for_player_id:
            shown_name = "???"
        else:
            shown_name = self.assigned_name

        return {
            "id": self.id,
            "name": self.name,
            "assignedName": shown_name,
            "revealed": self.revealed,
        }

    async def send(self, data: dict):
        """Oyuncuya JSON mesaj gönder."""
        try:
            await self.ws.send(json.dumps(data))
        except Exception:
            pass  # bağlantı kopmuş olabilir


class Room:
    """Bir oyun odasını temsil eder."""

    # Oda durumları
    LOBBY = "lobby"
    PLAYING = "playing"
    FINISHED = "finished"

    def __init__(self, code: str, host: Player):
        self.code = code
        self.host = host
        self.players: dict[str, Player] = {host.id: host}
        self.state = self.LOBBY
        self._next_rank = 1  # sıradaki açılan oyuncunun sırası

    def add_player(self, player: Player):
        """Odaya oyuncu ekle."""
        self.players[player.id] = player

    def remove_player(self, player_id: str):
        """Odadan oyuncu çıkar."""
        if player_id in self.players:
            del self.players[player_id]
        # host çıktıysa yeni host ata
        if self.host.id == player_id and self.players:
            self.host = next(iter(self.players.values()))

    def assign_names(self):
        """Her oyuncuya rastgele ünlü isim ata."""
        player_list = list(self.players.values())
        names = get_random_names(len(player_list))
        for player, name in zip(player_list, names):
            player.assigned_name = name
            player.revealed = False
            player.rank = None
        self._next_rank = 1
        self.state = self.PLAYING

    def check_guess(self, player_id: str, guess: str) -> tuple[bool, str]:
        """Oyuncunun tahminini kontrol et.
        Returns: (doğru_mu, mesaj)
        """
        player = self.players.get(player_id)
        if not player:
            return False, "Oyuncu bulunamadı."
        if player.revealed:
            return False, "Zaten doğru tahmin ettin!"
        if self.state != self.PLAYING:
            return False, "Oyun aktif değil."

        # büyük/küçük harf duyarsız karşılaştırma
        if guess.strip().lower() == player.assigned_name.strip().lower():
            player.revealed = True
            player.rank = self._next_rank
            self._next_rank += 1
            return True, f"Doğru! Sen {player.assigned_name} idin!"
        else:
            return False, "Yanlış tahmin, tekrar dene!"

    def is_game_over(self) -> bool:
        """Tüm oyuncular ismini açtıysa oyun bitti."""
        return all(p.revealed for p in self.players.values())

    def get_rankings(self) -> list[dict]:
        """Sıralama listesini döndür."""
        ranked = sorted(
            [p for p in self.players.values() if p.revealed],
            key=lambda p: p.rank,
        )
        # henüz tahmin edemeyenleri sona ekle
        unranked = [p for p in self.players.values() if not p.revealed]
        result = []
        for p in ranked:
            result.append({"name": p.name, "rank": p.rank, "assignedName": p.assigned_name})
        for p in unranked:
            result.append({"name": p.name, "rank": None, "assignedName": p.assigned_name})
        return result

    async def broadcast(self, data: dict, exclude: str | None = None):
        """Odadaki herkese mesaj gönder."""
        tasks = []
        for player in self.players.values():
            if player.id != exclude:
                tasks.append(player.send(data))
        await asyncio.gather(*tasks)

    async def send_game_state(self):
        """Her oyuncuya kendi perspektifinden oyun durumunu gönder."""
        for player in self.players.values():
            players_data = [
                p.to_game_dict(for_player_id=player.id)
                for p in self.players.values()
            ]
            await player.send({
                "type": "game_started",
                "players": players_data,
            })

    async def send_lobby_update(self):
        """Lobbydeki oyuncu listesini herkese gönder."""
        players_data = [p.to_dict() for p in self.players.values()]
        await self.broadcast({
            "type": "lobby_update",
            "players": players_data,
            "hostId": self.host.id,
        })


# ── Oda Yöneticisi ──────────────────────────────────────────────

_rooms: dict[str, Room] = {}
_player_room_map: dict[str, str] = {}  # player_id -> room_code
_player_counter = 0


def _generate_room_code() -> str:
    """6 haneli benzersiz oda kodu üret."""
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if code not in _rooms:
            return code


def _generate_player_id() -> str:
    """Benzersiz oyuncu ID'si üret."""
    global _player_counter
    _player_counter += 1
    return f"p{_player_counter}"


def get_room(room_code: str) -> Room | None:
    return _rooms.get(room_code)


def get_player_room(player_id: str) -> Room | None:
    code = _player_room_map.get(player_id)
    return _rooms.get(code) if code else None


def create_or_join_room(player_name: str, room_code: str | None, websocket) -> tuple[Player, Room, bool]:
    """Odaya katıl veya yeni oda oluştur.
    Returns: (player, room, is_new_room)
    """
    player_id = _generate_player_id()
    player = Player(player_id, player_name, websocket)

    if room_code and room_code in _rooms:
        room = _rooms[room_code]
        if room.state != Room.LOBBY:
            raise ValueError("Oyun zaten başlamış, katılamazsın!")
        room.add_player(player)
        _player_room_map[player_id] = room.code
        return player, room, False
    else:
        code = _generate_room_code() if not room_code else room_code
        room = Room(code, player)
        _rooms[code] = room
        _player_room_map[player_id] = code
        return player, room, True


def remove_player(player_id: str):
    """Oyuncuyu odadan ve sistemden çıkar."""
    room = get_player_room(player_id)
    if room:
        room.remove_player(player_id)
        if not room.players:
            del _rooms[room.code]
    if player_id in _player_room_map:
        del _player_room_map[player_id]
