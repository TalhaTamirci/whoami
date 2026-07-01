"""Skor 4 (Connect Four) — 2 oyunculu arena oyunu.

7 sütun x 6 satır dikey tahta. Sırayla taş bırakılır; taş yerçekimiyle
sütunun en altındaki boş hücreye düşer. 4 taşı yatay/dikey/çapraz
hizalayan kazanır; tahta dolarsa berabere.

İstemci → sunucu:
    {type: "drop", col}

Sunucu → istemci:
    {type: "game_state", board (6x7, null|playerId), turn, lastMove: [row, col]|null,
     players: [{id, name, avatar}], series: {playerId: n}}
    {type: "game_over", winnerId|null, winnerName|null,
     winningCells: [[r, c] x 4]|[], reason?, series: {playerId: n}}
"""
from arena import ArenaRoom, BaseGame, register_game

ROWS = 6
COLS = 7

# Kazanma kontrolü için yön vektörleri: yatay, dikey, iki çapraz
_DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


@register_game
class Skor4(BaseGame):
    GAME_TYPE = "skor4"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 2

    def __init__(self, room: ArenaRoom):
        super().__init__(room)
        # board[0] üst satır, board[ROWS-1] alt satır. Hücre: None | playerId
        self.board: list[list[str | None]] = [[None] * COLS for _ in range(ROWS)]
        self.player_ids: list[str] = []
        self.turn_index = 0
        self.last_move: list[int] | None = None
        self.over = False
        # Seri skoru odada tutulur — restart'ta oyun örneği yenilenir, oda kalır.
        if not hasattr(room, "skor4_series"):
            room.skor4_series = {}

    # ── Yardımcılar ──────────────────────────────────────────────

    def _series(self) -> dict:
        series = self.room.skor4_series
        return {pid: series.get(pid, 0) for pid in self.player_ids}

    def _state_payload(self) -> dict:
        return {
            "type": "game_state",
            "board": self.board,
            "turn": self.player_ids[self.turn_index] if not self.over else None,
            "lastMove": self.last_move,
            "players": [
                self.room.players[pid].to_dict()
                for pid in self.player_ids
                if pid in self.room.players
            ],
            "series": self._series(),
        }

    def _find_win(self, row: int, col: int) -> list[list[int]] | None:
        """Son hamleden geçen 4'lü var mı? Varsa hücrelerini döndür."""
        pid = self.board[row][col]
        for dr, dc in _DIRECTIONS:
            cells = [[row, col]]
            for sign in (1, -1):
                r, c = row + dr * sign, col + dc * sign
                while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == pid:
                    cells.append([r, c])
                    r += dr * sign
                    c += dc * sign
            if len(cells) >= 4:
                cells.sort()
                return cells[:4]
        return None

    async def _game_over(self, winner_id: str | None, winning_cells: list, reason: str = ""):
        self.over = True
        winner_name = None
        if winner_id:
            self.room.skor4_series[winner_id] = self.room.skor4_series.get(winner_id, 0) + 1
            player = self.room.players.get(winner_id)
            winner_name = player.name if player else None
        self.finish()
        payload = {
            "type": "game_over",
            "winnerId": winner_id,
            "winnerName": winner_name,
            "winningCells": winning_cells,
            "series": self._series(),
        }
        if reason:
            payload["reason"] = reason
        await self.room.broadcast(payload)

    # ── Arena kancaları ──────────────────────────────────────────

    async def on_start(self, options: dict):
        players = self.room.ordered_players()[: self.MAX_PLAYERS]
        if len(players) < self.MIN_PLAYERS:
            # Restart'ta arena min oyuncu kontrolü yapmaz — burada güvence altına al
            self.over = True
            self.finish()
            await self.room.broadcast(
                {"type": "error", "message": f"En az {self.MIN_PLAYERS} oyuncu gerekli."}
            )
            return
        self.player_ids = [p.id for p in players]
        # Serilerde sadece mevcut oyuncular kalsın
        self.room.skor4_series = {
            pid: n for pid, n in self.room.skor4_series.items() if pid in self.player_ids
        }
        self.turn_index = 0
        await self.room.broadcast(self._state_payload())

    async def on_message(self, player, data: dict):
        if data.get("type") != "drop":
            return
        if self.over or self.room.state != ArenaRoom.PLAYING:
            await player.send({"type": "error", "message": "Oyun şu anda oynanmıyor."})
            return
        if player.id not in self.player_ids:
            await player.send({"type": "error", "message": "Bu oyunda oyuncu değilsin."})
            return
        if player.id != self.player_ids[self.turn_index]:
            await player.send({"type": "error", "message": "Sıra sende değil."})
            return

        col = data.get("col")
        if not isinstance(col, int) or isinstance(col, bool) or not 0 <= col < COLS:
            await player.send({"type": "error", "message": "Geçersiz sütun."})
            return

        # Taş yerçekimiyle en alttaki boş hücreye düşer
        row = -1
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] is None:
                row = r
                break
        if row == -1:
            await player.send({"type": "error", "message": "Bu sütun dolu."})
            return

        self.board[row][col] = player.id
        self.last_move = [row, col]

        winning_cells = self._find_win(row, col)
        board_full = all(cell is not None for cell in self.board[0])

        if winning_cells or board_full:
            self.over = True
            await self.room.broadcast(self._state_payload())
            if winning_cells:
                await self._game_over(player.id, winning_cells)
            else:
                await self._game_over(None, [])  # berabere
            return

        self.turn_index = (self.turn_index + 1) % len(self.player_ids)
        await self.room.broadcast(self._state_payload())

    async def on_leave(self, player):
        if self.over or self.room.state != ArenaRoom.PLAYING:
            return
        if player.id not in self.player_ids:
            return
        # Kalan oyuncu kazanır
        remaining = [pid for pid in self.player_ids if pid in self.room.players]
        winner_id = remaining[0] if remaining else None
        await self._game_over(winner_id, [], reason="opponent_left")
