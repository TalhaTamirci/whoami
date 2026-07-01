"""Koridor (Quoridor) — 2 oyunculu arena oyunu.

Tahta 9x9 hücre. Oyuncu 1 (host) (8,4)'ten başlar, hedefi satır 0;
Oyuncu 2 (0,4)'ten başlar, hedefi satır 8. Her oyuncunun 10 duvarı var.

DUVAR ÇAPA KONVANSİYONU (istemciyle birebir aynı olmalı):
- Yatay duvar "h", çapa (r, c): (r,c) ve (r,c+1) hücrelerinin ALTINI kapatır,
  yani (r,c)<->(r+1,c) ve (r,c+1)<->(r+1,c+1) geçişlerini engeller.
- Dikey duvar "v", çapa (r, c): (r,c) ve (r+1,c) hücrelerinin SAĞINI kapatır,
  yani (r,c)<->(r,c+1) ve (r+1,c)<->(r+1,c+1) geçişlerini engeller.
- Geçerli çapa aralığı her iki yön için: 0 <= r <= 7 ve 0 <= c <= 7.

Sunucu otoriterdir: sıra, hamle geçerliliği, duvar çakışması ve
"hiçbir piyonun yolu tamamen kapatılamaz" (BFS) kuralı burada denetlenir.
"""
from __future__ import annotations

from collections import deque

from arena import ArenaPlayer, ArenaRoom, BaseGame, register_game

SIZE = 9
WALLS_PER_PLAYER = 10
DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def _wall_edges(o: str, r: int, c: int) -> set[frozenset]:
    """Bir duvarın engellediği iki hücre-geçişini (kenarı) döndürür."""
    if o == "h":
        # (r,c) ve (r,c+1) hücrelerinin altı
        return {
            frozenset({(r, c), (r + 1, c)}),
            frozenset({(r, c + 1), (r + 1, c + 1)}),
        }
    # (r,c) ve (r+1,c) hücrelerinin sağı
    return {
        frozenset({(r, c), (r, c + 1)}),
        frozenset({(r + 1, c), (r + 1, c + 1)}),
    }


def _inside(r: int, c: int) -> bool:
    return 0 <= r < SIZE and 0 <= c < SIZE


def _is_coord_int(x) -> bool:
    """Gerçek int mi? (bool, int alt sınıfı olduğundan JSON true/false'u ele.)"""
    return isinstance(x, int) and not isinstance(x, bool)


@register_game
class KoridorGame(BaseGame):
    GAME_TYPE = "koridor"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 2

    def __init__(self, room: ArenaRoom):
        super().__init__(room)
        self.player_ids: list[str] = []
        self.pawns: dict[str, tuple[int, int]] = {}
        self.goals: dict[str, int] = {}
        self.walls: list[dict] = []          # [{"o": "h"|"v", "r": int, "c": int}]
        self.walls_left: dict[str, int] = {}
        self.turn: str | None = None

    # ── Yaşam döngüsü ────────────────────────────────────────────────

    async def on_start(self, options: dict):
        players = self.room.ordered_players()
        if len(players) < 2:
            self.finish()
            await self.room.broadcast(
                {"type": "error", "message": "Yeni oyun için 2 oyuncu gerekli."}
            )
            return
        p1, p2 = players[0].id, players[1].id
        self.player_ids = [p1, p2]
        self.pawns = {p1: (SIZE - 1, 4), p2: (0, 4)}   # p1 alttan, p2 üstten
        self.goals = {p1: 0, p2: SIZE - 1}
        self.walls = []
        self.walls_left = {p1: WALLS_PER_PLAYER, p2: WALLS_PER_PLAYER}
        self.turn = p1  # ilk oyuncu (host) başlar
        await self._broadcast_state()

    async def on_message(self, player: ArenaPlayer, data: dict):
        msg_type = data.get("type")
        if msg_type not in ("move", "wall"):
            return
        if self.room.state != ArenaRoom.PLAYING:
            await player.send({"type": "error", "message": "Oyun şu anda oynanmıyor."})
            return
        if player.id not in self.pawns:
            await player.send({"type": "error", "message": "Bu oyunda oyuncu değilsin."})
            return
        if self.turn != player.id:
            await player.send({"type": "error", "message": "Sıra sende değil."})
            return

        if msg_type == "move":
            await self._handle_move(player, data)
        else:
            await self._handle_wall(player, data)

    async def on_leave(self, player: ArenaPlayer):
        # Oyun sırasında ayrılan kaybeder; kalan oyuncu kazanır.
        if self.room.state != ArenaRoom.PLAYING or player.id not in self.pawns:
            return
        self.finish()
        remaining = [
            pid for pid in self.player_ids
            if pid != player.id and pid in self.room.players
        ]
        if remaining:
            winner = self.room.players[remaining[0]]
            await self.room.broadcast({
                "type": "game_over",
                "winnerId": winner.id,
                "winnerName": winner.name,
                "reason": f"{player.name} oyundan ayrıldı.",
            })

    # ── Hamleler ─────────────────────────────────────────────────────

    async def _handle_move(self, player: ArenaPlayer, data: dict):
        to = data.get("to")
        if (
            not isinstance(to, (list, tuple)) or len(to) != 2
            or not all(_is_coord_int(x) for x in to) or not _inside(to[0], to[1])
        ):
            await player.send({"type": "error", "message": "Geçersiz hedef hücre."})
            return
        target = (to[0], to[1])
        legal = self._legal_moves(player.id)
        if target not in legal:
            await player.send({
                "type": "error",
                "message": "Bu hücreye gidemezsin — arada duvar var ya da hücre erişilemez.",
            })
            return

        self.pawns[player.id] = target

        if target[0] == self.goals[player.id]:
            # Kazandı: son durumu ve sonucu yayınla.
            await self._broadcast_state()
            self.finish()
            await self.room.broadcast({
                "type": "game_over",
                "winnerId": player.id,
                "winnerName": player.name,
                "reason": f"{player.name} hedef satıra ulaştı!",
            })
            return

        self._next_turn()
        await self._broadcast_state()

    async def _handle_wall(self, player: ArenaPlayer, data: dict):
        o = data.get("orientation")
        r, c = data.get("r"), data.get("c")
        if o not in ("h", "v") or not _is_coord_int(r) or not _is_coord_int(c):
            await player.send({"type": "error", "message": "Geçersiz duvar isteği."})
            return
        if not (0 <= r <= SIZE - 2 and 0 <= c <= SIZE - 2):
            await player.send({"type": "error", "message": "Duvar tahtanın dışına taşıyor."})
            return
        if self.walls_left.get(player.id, 0) <= 0:
            await player.send({"type": "error", "message": "Hiç duvarın kalmadı."})
            return
        if self._wall_conflicts(o, r, c):
            await player.send({
                "type": "error",
                "message": "Duvar mevcut bir duvarla çakışıyor veya kesişiyor.",
            })
            return

        # KRİTİK KURAL: duvar hiçbir piyonun hedefe giden TÜM yollarını kapatamaz.
        blocked = self._blocked_edges(extra={"o": o, "r": r, "c": c})
        for pid in self.player_ids:
            if not self._has_path(self.pawns[pid], self.goals[pid], blocked):
                await player.send({
                    "type": "error",
                    "message": "Bu duvar bir oyuncunun hedefe giden tüm yollarını kapatıyor.",
                })
                return

        self.walls.append({"o": o, "r": r, "c": c})
        self.walls_left[player.id] -= 1
        self._next_turn()
        await self._broadcast_state()

    # ── Kural yardımcıları ───────────────────────────────────────────

    def _next_turn(self):
        p1, p2 = self.player_ids
        self.turn = p2 if self.turn == p1 else p1

    def _blocked_edges(self, extra: dict | None = None) -> set[frozenset]:
        edges: set[frozenset] = set()
        for w in self.walls:
            edges |= _wall_edges(w["o"], w["r"], w["c"])
        if extra is not None:
            edges |= _wall_edges(extra["o"], extra["r"], extra["c"])
        return edges

    def _wall_conflicts(self, o: str, r: int, c: int) -> bool:
        """Üst üste binme / kesişme kontrolü.

        - Aynı çapada ikinci duvar yasak (h+v kesişmesi dahil).
        - İki yatay duvar aynı satırda komşu çapalarda çakışır (|dc| <= 1).
        - İki dikey duvar aynı sütunda komşu çapalarda çakışır (|dr| <= 1).
        """
        for w in self.walls:
            if w["r"] == r and w["c"] == c:
                return True
            if o == "h" and w["o"] == "h" and w["r"] == r and abs(w["c"] - c) == 1:
                return True
            if o == "v" and w["o"] == "v" and w["c"] == c and abs(w["r"] - r) == 1:
                return True
        return False

    def _has_path(self, start: tuple[int, int], goal_row: int, blocked: set) -> bool:
        """BFS: start hücresinden goal_row satırına duvarlar arasından yol var mı?
        (Standart kural: piyonlar yol kontrolünde engel sayılmaz.)"""
        queue = deque([start])
        seen = {start}
        while queue:
            r, c = queue.popleft()
            if r == goal_row:
                return True
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if (
                    _inside(nr, nc) and (nr, nc) not in seen
                    and frozenset({(r, c), (nr, nc)}) not in blocked
                ):
                    seen.add((nr, nc))
                    queue.append((nr, nc))
        return False

    def _legal_moves(self, pid: str) -> set[tuple[int, int]]:
        """Standart Quoridor piyon hamleleri: 1 adım ortogonal; rakibin
        üzerinden düz atlama; atlanacak yer kapalıysa çapraz kaçış."""
        blocked = self._blocked_edges()
        me = self.pawns[pid]
        opp_id = self.player_ids[1] if pid == self.player_ids[0] else self.player_ids[0]
        opp = self.pawns.get(opp_id)
        moves: set[tuple[int, int]] = set()

        for dr, dc in DIRS:
            nr, nc = me[0] + dr, me[1] + dc
            if not _inside(nr, nc) or frozenset({me, (nr, nc)}) in blocked:
                continue
            if (nr, nc) != opp:
                moves.add((nr, nc))
                continue
            # Rakip bitişik: önce düz atlamayı dene.
            jr, jc = nr + dr, nc + dc
            if _inside(jr, jc) and frozenset({(nr, nc), (jr, jc)}) not in blocked:
                moves.add((jr, jc))
            else:
                # Arkası duvar/tahta dışı → rakibin yanındaki çapraz hücreler.
                for pr, pc in ((dc, dr), (-dc, -dr)):
                    tr, tc = nr + pr, nc + pc
                    if _inside(tr, tc) and frozenset({(nr, nc), (tr, tc)}) not in blocked:
                        moves.add((tr, tc))
        return moves

    # ── Durum yayını ─────────────────────────────────────────────────

    async def _broadcast_state(self):
        await self.room.broadcast({
            "type": "game_state",
            "pawns": {pid: list(pos) for pid, pos in self.pawns.items()},
            "walls": [dict(w) for w in self.walls],
            "wallsLeft": dict(self.walls_left),
            "turn": self.turn,
            "goals": dict(self.goals),
        })
