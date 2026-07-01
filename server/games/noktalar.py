"""Noktalar ve Kutular (Dots and Boxes) — arena oyunu.

2-4 oyuncu. N x N kutuluk ızgarada (N+1 x N+1 nokta) sırayla çizgi çekilir.
Bir kutunun 4. kenarını tamamlayan oyuncu kutuyu alır ve bir hamle daha yapar.
Tüm kutular dolunca en çok kutusu olan kazanır (beraberlik mümkün).

İstemci → sunucu:
    {type: "line", kind: "h"|"v", r, c}
        h: (r,c)-(r,c+1) noktaları arası yatay çizgi  (0<=r<=N, 0<=c<N)
        v: (r,c)-(r+1,c) noktaları arası dikey çizgi  (0<=r<N, 0<=c<=N)

Sunucu → istemci:
    {type: "game_state", size, hLines, vLines, boxes, scores, turn, captured?}
    {type: "game_over", winnerIds, scores, reason?}
"""
from arena import ArenaPlayer, ArenaRoom, BaseGame, register_game

VALID_SIZES = (4, 5, 6)
DEFAULT_SIZE = 5


@register_game
class NoktalarGame(BaseGame):
    GAME_TYPE = "noktalar"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 4

    def __init__(self, room: ArenaRoom):
        super().__init__(room)
        self.size: int = DEFAULT_SIZE
        # (r, c) -> player_id (çizgiyi çeken)
        self.h_lines: dict[tuple[int, int], str] = {}
        self.v_lines: dict[tuple[int, int], str] = {}
        # boxes[r][c] -> kutuyu alan player_id | None
        self.boxes: list[list[str | None]] = []
        self.scores: dict[str, int] = {}
        self.turn_order: list[str] = []
        self.turn_idx: int = 0

    # ── Yaşam döngüsü ────────────────────────────────────────────────

    async def on_start(self, options: dict):
        players = self.room.ordered_players()
        if len(players) < self.MIN_PLAYERS:
            # restart sırasında oyuncu sayısı düşmüş olabilir
            self.room.state = ArenaRoom.FINISHED
            await self.room.broadcast({
                "type": "error",
                "message": f"En az {self.MIN_PLAYERS} oyuncu gerekli.",
            })
            return

        size = options.get("size", DEFAULT_SIZE)
        # type kontrolü şart: bool/float (True==1, 4.0==4) 'in' kontrolünü
        # geçebilir ve aşağıda TypeError'a yol açar.
        if type(size) is not int or size not in VALID_SIZES:
            size = DEFAULT_SIZE
        self.size = size
        self.h_lines = {}
        self.v_lines = {}
        self.boxes = [[None] * size for _ in range(size)]
        self.turn_order = [p.id for p in players]
        self.scores = {pid: 0 for pid in self.turn_order}
        self.turn_idx = 0

        await self._broadcast_state()

    async def on_message(self, player: ArenaPlayer, data: dict):
        if data.get("type") != "line":
            await player.send({"type": "error", "message": "Bilinmeyen mesaj."})
            return
        if self.room.state != ArenaRoom.PLAYING:
            await player.send({"type": "error", "message": "Oyun aktif değil."})
            return
        if player.id != self._current_turn():
            await player.send({"type": "error", "message": "Sıra sende değil."})
            return

        kind = data.get("kind")
        r = data.get("r")
        c = data.get("c")
        if (
            kind not in ("h", "v")
            or type(r) is not int
            or type(c) is not int
            or not self._in_range(kind, r, c)
        ):
            await player.send({"type": "error", "message": "Geçersiz hamle."})
            return

        lines = self.h_lines if kind == "h" else self.v_lines
        if (r, c) in lines:
            await player.send({"type": "error", "message": "Bu çizgi zaten çizilmiş."})
            return

        # Hamleyi uygula
        lines[(r, c)] = player.id
        captured = self._capture_boxes(kind, r, c, player.id)

        if captured:
            self.scores[player.id] += len(captured)
            # kutu kapatan oyuncu bir hamle daha yapar → sıra ilerlemez
        else:
            self.turn_idx = (self.turn_idx + 1) % len(self.turn_order)

        if self._all_boxes_filled():
            await self._broadcast_state(captured=captured, over=True)
            await self._finish_game()
        else:
            await self._broadcast_state(captured=captured)

    async def on_leave(self, player: ArenaPlayer):
        if self.room.state != ArenaRoom.PLAYING:
            return
        # Oyun sırasında ayrılan olursa oyun biter: kalanlardan önde olan kazanır
        remaining = {
            pid: self.scores.get(pid, 0)
            for pid in self.turn_order
            if pid in self.room.players
        }
        await self._finish_game(
            candidates=remaining,
            reason=f"{player.name} oyundan ayrıldı.",
        )

    # ── Yardımcılar ──────────────────────────────────────────────────

    def _current_turn(self) -> str | None:
        if not self.turn_order:
            return None
        return self.turn_order[self.turn_idx]

    def _in_range(self, kind: str, r: int, c: int) -> bool:
        n = self.size
        if kind == "h":
            return 0 <= r <= n and 0 <= c < n
        return 0 <= r < n and 0 <= c <= n

    def _box_complete(self, br: int, bc: int) -> bool:
        return (
            (br, bc) in self.h_lines
            and (br + 1, bc) in self.h_lines
            and (br, bc) in self.v_lines
            and (br, bc + 1) in self.v_lines
        )

    def _capture_boxes(self, kind: str, r: int, c: int, pid: str) -> list[list[int]]:
        """Çizilen çizginin kapattığı kutuları sahiplendirir, [r,c] listesi döner."""
        if kind == "h":
            candidates = [(r - 1, c), (r, c)]  # üstteki ve alttaki kutu
        else:
            candidates = [(r, c - 1), (r, c)]  # soldaki ve sağdaki kutu

        captured: list[list[int]] = []
        for br, bc in candidates:
            if 0 <= br < self.size and 0 <= bc < self.size:
                if self.boxes[br][bc] is None and self._box_complete(br, bc):
                    self.boxes[br][bc] = pid
                    captured.append([br, bc])
        return captured

    def _all_boxes_filled(self) -> bool:
        return all(cell is not None for row in self.boxes for cell in row)

    def _state_payload(self, captured: list[list[int]] | None = None) -> dict:
        payload = {
            "type": "game_state",
            "size": self.size,
            "hLines": [
                {"r": r, "c": c, "player": pid}
                for (r, c), pid in self.h_lines.items()
            ],
            "vLines": [
                {"r": r, "c": c, "player": pid}
                for (r, c), pid in self.v_lines.items()
            ],
            "boxes": self.boxes,
            "scores": self.scores,
            "turn": self._current_turn(),
        }
        if captured:
            payload["captured"] = captured
        return payload

    async def _broadcast_state(
        self, captured: list[list[int]] | None = None, over: bool = False
    ):
        payload = self._state_payload(captured)
        if over:
            payload["turn"] = None
        await self.room.broadcast(payload)

    async def _finish_game(
        self, candidates: dict[str, int] | None = None, reason: str | None = None
    ):
        """Oyunu bitirir ve game_over yayınlar. candidates: kazanan adayları."""
        pool = candidates if candidates is not None else self.scores
        winner_ids: list[str] = []
        if pool:
            best = max(pool.values())
            winner_ids = [pid for pid, s in pool.items() if s == best]

        self.finish()
        payload = {
            "type": "game_over",
            "winnerIds": winner_ids,
            "scores": self.scores,
        }
        if reason:
            payload["reason"] = reason
        await self.room.broadcast(payload)
