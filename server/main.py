"""Ben Kimim? — WebSocket Sunucusu

Kullanım:
    python main.py
    Sunucu ws://localhost:8765 adresinde başlar.
"""

import asyncio
import json
import websockets

from game import (
    create_or_join_room,
    remove_player,
    get_player_room,
    Room,
    Player,
)

# Aktif bağlantıları takip et: websocket -> player_id
connected_players: dict[websockets.WebSocketServerProtocol, str] = {}


async def handle_join(websocket, data: dict) -> Player | None:
    """Oyuncu katılma isteğini işle."""
    player_name = data.get("playerName", "").strip()
    room_code = data.get("roomCode", "").strip().upper() or None

    if not player_name:
        await websocket.send(json.dumps({
            "type": "error",
            "message": "İsim boş olamaz!"
        }))
        return None

    try:
        player, room, is_new = create_or_join_room(player_name, room_code, websocket)
    except ValueError as e:
        await websocket.send(json.dumps({
            "type": "error",
            "message": str(e)
        }))
        return None

    connected_players[websocket] = player.id

    # Welcome mesajı gönder
    await player.send({
        "type": "welcome",
        "playerId": player.id,
        "roomCode": room.code,
        "isHost": room.host.id == player.id,
    })

    # Lobby güncelle
    await room.send_lobby_update()

    action = "oluşturdu" if is_new else "katıldı"
    print(f"[+] {player.name} ({player.id}) odaya {action}: {room.code}")
    return player


async def handle_start_game(player_id: str):
    """Oyunu başlat (sadece host yapabilir)."""
    room = get_player_room(player_id)
    if not room:
        return

    if room.host.id != player_id:
        await room.players[player_id].send({
            "type": "error",
            "message": "Sadece oda sahibi oyunu başlatabilir!"
        })
        return

    # if len(room.players) < 2:
    #     await room.players[player_id].send({
    #         "type": "error",
    #         "message": "Oyun başlatmak için en az 2 oyuncu gerekli!"
    #     })
    #     return

    # İsimleri ata ve oyunu başlat
    room.assign_names()
    await room.send_game_state()

    print(f"[▶] Oda {room.code} oyunu başlattı ({len(room.players)} oyuncu)")
    for p in room.players.values():
        print(f"    {p.name} → {p.assigned_name}")


async def handle_guess(player_id: str, data: dict):
    """Tahmin isteğini işle."""
    room = get_player_room(player_id)
    if not room:
        return

    player = room.players.get(player_id)
    if not player:
        return

    guess = data.get("guess", "").strip()
    if not guess:
        await player.send({
            "type": "guess_result",
            "correct": False,
            "message": "Boş tahmin gönderilemez!"
        })
        return

    correct, message = room.check_guess(player_id, guess)

    # Tahmin sonucunu oyuncuya bildir
    await player.send({
        "type": "guess_result",
        "correct": correct,
        "message": message,
    })

    if correct:
        # Herkese bu oyuncunun isminin açıldığını bildir
        await room.broadcast({
            "type": "player_revealed",
            "playerId": player.id,
            "playerName": player.name,
            "assignedName": player.assigned_name,
            "rank": player.rank,
        })

        # Oyun bitti mi kontrol et
        if room.is_game_over():
            room.state = Room.FINISHED
            await room.broadcast({
                "type": "game_over",
                "rankings": room.get_rankings(),
            })
            print(f"[✓] Oda {room.code} oyunu bitti!")
        else:
            print(f"[★] {player.name} doğru tahmin etti: {player.assigned_name} (sıra: {player.rank})")


async def handle_new_round(player_id: str):
    """Yeni tur başlat."""
    room = get_player_room(player_id)
    if not room:
        return

    if room.host.id != player_id:
        await room.players[player_id].send({
            "type": "error",
            "message": "Sadece oda sahibi yeni tur başlatabilir!"
        })
        return

    room.assign_names()
    await room.send_game_state()
    print(f"[▶] Oda {room.code} yeni tur başlattı")


async def handle_disconnect(websocket):
    """Bağlantı koptuğunda temizlik yap."""
    player_id = connected_players.pop(websocket, None)
    if not player_id:
        return

    room = get_player_room(player_id)
    remove_player(player_id)

    if room and room.players:
        await room.send_lobby_update()
        print(f"[-] Oyuncu {player_id} ayrıldı, oda {room.code}")
    elif room:
        print(f"[x] Oda {room.code} boşaldı, silindi")


async def handler(websocket):
    """Her WebSocket bağlantısını yönet."""
    player_id = None
    try:
        async for raw_message in websocket:
            try:
                data = json.loads(raw_message)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Geçersiz JSON formatı."
                }))
                continue

            msg_type = data.get("type")

            if msg_type == "join":
                player = await handle_join(websocket, data)
                if player:
                    player_id = player.id

            elif msg_type == "start_game":
                if player_id:
                    await handle_start_game(player_id)

            elif msg_type == "guess":
                if player_id:
                    await handle_guess(player_id, data)

            elif msg_type == "new_round":
                if player_id:
                    await handle_new_round(player_id)

            else:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Bilinmeyen event tipi: {msg_type}"
                }))

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await handle_disconnect(websocket)


async def health_check(path, request_headers):
    """Cloudflare tüneli sağlık kontrolü için HTTP yanıt."""
    if path == "/health":
        return (200, [], b"OK")
    # None dönerse normal WebSocket upgrade devam eder
    return None


async def main():
    """Sunucuyu başlat."""
    import os
    host = ""
    port = int(os.environ.get("PORT", 8765))

    print(f"╔══════════════════════════════════════╗")
    print(f"║      🎭 Ben Kimim? Sunucusu 🎭      ║")
    print(f"║   ws://0.0.0.0:{port}                ║")
    print(f"╚══════════════════════════════════════╝")

    async with websockets.serve(
        handler,
        host,
        port,
        origins=None,
        ping_interval=20,
        ping_timeout=20,
        process_request=health_check,
    ):
        await asyncio.Future()  # sonsuza kadar çalış


if __name__ == "__main__":
    asyncio.run(main())
