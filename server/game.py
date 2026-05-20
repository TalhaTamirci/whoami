"""Oyun mantığı — Player, Room sınıfları ve oda yönetimi."""
from __future__ import annotations

import string
import random
import asyncio
import json
from names import get_random_names, get_all_names


class Player:
    """Bir oyuncuyu temsil eder."""

    DEFAULT_AVATAR = "🎭"

    def __init__(self, player_id: str, name: str, websocket):
        self.id = player_id
        self.name = name
        self.ws = websocket
        self.avatar: str = self.DEFAULT_AVATAR
        self.assigned_name: str | None = None  # kafasındaki isim
        self.revealed: bool = False  # doğru tahmin ettiyse True
        self.rank: int | None = None  # sıralama (1., 2., 3. ...)

    def to_dict(self) -> dict:
        """Lobby için oyuncu bilgisi."""
        return {"id": self.id, "name": self.name, "avatar": self.avatar}

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
            "avatar": self.avatar,
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
        self.current_category: str = "populer_ikonlar"
        self.current_difficulty: str = "hepsi"
        self.custom_words: list[str] = []
        self.qa_log: list[dict] = []
        self.turn_order: list[str] = []
        self.current_turn_id: str | None = None
        self.timer_total: int = 0
        self.timer_remaining: int = 0
        self._timer_task = None

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

    def assign_names(self, category: str = "unluler", difficulty: str = "hepsi",
                     custom_words: list[str] | None = None, timer_seconds: int = 0):
        """Her oyuncuya rastgele kelime ata."""
        player_list = list(self.players.values())
        names = get_random_names(
            len(player_list), category, difficulty, custom_words
        )
        for player, name in zip(player_list, names):
            player.assigned_name = name
            player.revealed = False
            player.rank = None
        self._next_rank = 1
        self.state = self.PLAYING
        self.current_category = category
        self.current_difficulty = difficulty
        self.custom_words = list(custom_words or [])

        # Sıra ve log sıfırla
        self.qa_log = []
        self.turn_order = [p.id for p in player_list]
        self.current_turn_id = self.turn_order[0] if self.turn_order else None

        # Timer ayarla
        self.timer_total = max(0, int(timer_seconds or 0))
        self.timer_remaining = self.timer_total
        self._cancel_timer()

    def _cancel_timer(self):
        if self._timer_task and not self._timer_task.done():
            self._timer_task.cancel()
        self._timer_task = None

    def advance_turn(self) -> str | None:
        """Sıradaki açılmamış oyuncuya geç. Açık olanları atla."""
        if not self.turn_order:
            return None
        # geçerli pozisyonu bul
        try:
            idx = self.turn_order.index(self.current_turn_id) if self.current_turn_id else -1
        except ValueError:
            idx = -1

        n = len(self.turn_order)
        for step in range(1, n + 1):
            candidate_id = self.turn_order[(idx + step) % n]
            player = self.players.get(candidate_id)
            if player and not player.revealed:
                self.current_turn_id = candidate_id
                self.timer_remaining = self.timer_total
                return candidate_id
        self.current_turn_id = None
        return None

    def add_log_entry(self, entry: dict):
        """Q&A loguna yeni kayıt ekle (son 100 mesajı tut)."""
        self.qa_log.append(entry)
        if len(self.qa_log) > 100:
            self.qa_log = self.qa_log[-100:]

    def get_hint_for(self, player_id: str) -> str | None:
        """Oyuncunun atanmış isminden ipucu üret (ilk harf + uzunluk)."""
        player = self.players.get(player_id)
        if not player or not player.assigned_name or player.revealed:
            return None
        name = player.assigned_name
        first = name[0] if name else "?"
        word_count = len(name.split())
        return f"İlk harf: {first} · {len(name)} karakter · {word_count} kelime"

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
        category_items = get_all_names(
            self.current_category, self.current_difficulty, self.custom_words
        )
        for player in self.players.values():
            players_data = [
                p.to_game_dict(for_player_id=player.id)
                for p in self.players.values()
            ]
            await player.send({
                "type": "game_started",
                "players": players_data,
                "category": self.current_category,
                "difficulty": self.current_difficulty,
                "categoryItems": category_items,
                "turnPlayerId": self.current_turn_id,
                "timerTotal": self.timer_total,
                "timerRemaining": self.timer_remaining,
            })

    async def broadcast_turn(self):
        await self.broadcast({
            "type": "turn_changed",
            "turnPlayerId": self.current_turn_id,
            "timerRemaining": self.timer_remaining,
            "timerTotal": self.timer_total,
        })

    async def run_timer(self):
        """Süre sayacını arka planda çalıştır."""
        try:
            while self.state == self.PLAYING and self.timer_total > 0:
                await asyncio.sleep(1)
                if self.state != self.PLAYING:
                    return
                self.timer_remaining -= 1
                if self.timer_remaining <= 0:
                    # Süre doldu — sırayı kaydır
                    self.advance_turn()
                    await self.broadcast({
                        "type": "timer_expired",
                        "turnPlayerId": self.current_turn_id,
                        "timerRemaining": self.timer_remaining,
                        "timerTotal": self.timer_total,
                    })
                else:
                    await self.broadcast({
                        "type": "timer_tick",
                        "timerRemaining": self.timer_remaining,
                    })
        except asyncio.CancelledError:
            pass

    def start_timer_task(self):
        self._cancel_timer()
        if self.timer_total > 0:
            self._timer_task = asyncio.create_task(self.run_timer())

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
