/**
 * Koridor (Quoridor) — istemci
 * Sunucu otoriterdir; buradaki kural hesapları yalnızca UI içindir
 * (vurgu, önizleme, erken uyarı).
 */
"use strict";

// ── WS adresi ───────────────────────────────────────
const WS_URL = (() => {
    if (window.WS_URL) return window.WS_URL;
    const host = location.hostname;
    if (host === "oyun.ahmetkadir.com") {
        return "wss://ws.oyun.ahmetkadir.com";
    }
    if (host === "localhost" || host === "127.0.0.1") {
        return "ws://localhost:8765";
    }
    return "wss://whoami-kaa7.onrender.com";
})();

const SIZE = 9;
const AVATARS = ["🦊", "🐼", "🤖", "👻", "🦁", "🐸", "🦄", "😎", "🐙", "🥷", "🐯", "🐺"];

// ── Durum ───────────────────────────────────────────
let ws = null;
let myId = null;
let roomCode = null;
let isHost = false;
let lobbyPlayers = [];       // lobby_update'ten gelen liste
let game = null;             // son game_state
let selectedPawn = false;    // piyon seçili mi (hamle vurguları açık)
let wallMode = false;
let myAvatar = AVATARS[0];

// ── DOM kısayolları ─────────────────────────────────
const $ = (id) => document.getElementById(id);
const screenLobby = $("screen-lobby");
const screenGame = $("screen-game");
const joinPanel = $("join-panel");
const roomPanel = $("room-panel");
const boardEl = $("board");

// ═════════════════════════════════════════════════════
// Kural yardımcıları (sunucudaki koridor.py ile aynı konvansiyon)
//
// DUVAR ÇAPA KONVANSİYONU:
// - "h" çapa (r,c): (r,c) ve (r,c+1) hücrelerinin ALTINI kapatır
//   → (r,c)↔(r+1,c) ve (r,c+1)↔(r+1,c+1) geçişleri engellenir.
// - "v" çapa (r,c): (r,c) ve (r+1,c) hücrelerinin SAĞINI kapatır
//   → (r,c)↔(r,c+1) ve (r+1,c)↔(r+1,c+1) geçişleri engellenir.
// - Çapa aralığı: 0 <= r,c <= 7.
// ═════════════════════════════════════════════════════

const DIRS = [[-1, 0], [1, 0], [0, -1], [0, 1]];
const inside = (r, c) => r >= 0 && r < SIZE && c >= 0 && c < SIZE;

/** İki komşu hücre arasındaki kenarın anahtarı (yönden bağımsız). */
function edgeKey(r1, c1, r2, c2) {
    return (r1 < r2 || (r1 === r2 && c1 < c2))
        ? `${r1},${c1}|${r2},${c2}`
        : `${r2},${c2}|${r1},${c1}`;
}

/** Bir duvarın engellediği iki kenar. */
function wallEdges(o, r, c) {
    if (o === "h") {
        return [edgeKey(r, c, r + 1, c), edgeKey(r, c + 1, r + 1, c + 1)];
    }
    return [edgeKey(r, c, r, c + 1), edgeKey(r + 1, c, r + 1, c + 1)];
}

function blockedEdges(walls, extra) {
    const set = new Set();
    for (const w of walls) wallEdges(w.o, w.r, w.c).forEach((e) => set.add(e));
    if (extra) wallEdges(extra.o, extra.r, extra.c).forEach((e) => set.add(e));
    return set;
}

/** Standart Quoridor hamleleri: 1 adım + rakip üzerinden atlama + çapraz kaçış. */
function legalMoves(pid) {
    if (!game) return [];
    const blocked = blockedEdges(game.walls);
    const me = game.pawns[pid];
    const oppId = Object.keys(game.pawns).find((id) => id !== pid);
    const opp = oppId ? game.pawns[oppId] : null;
    const moves = [];
    for (const [dr, dc] of DIRS) {
        const nr = me[0] + dr, nc = me[1] + dc;
        if (!inside(nr, nc) || blocked.has(edgeKey(me[0], me[1], nr, nc))) continue;
        if (!opp || nr !== opp[0] || nc !== opp[1]) {
            moves.push([nr, nc]);
            continue;
        }
        // Rakip bitişik → düz atlama
        const jr = nr + dr, jc = nc + dc;
        if (inside(jr, jc) && !blocked.has(edgeKey(nr, nc, jr, jc))) {
            moves.push([jr, jc]);
        } else {
            // Arkası kapalı → çapraz hücreler
            for (const [pr, pc] of [[dc, dr], [-dc, -dr]]) {
                const tr = nr + pr, tc = nc + pc;
                if (inside(tr, tc) && !blocked.has(edgeKey(nr, nc, tr, tc))) {
                    moves.push([tr, tc]);
                }
            }
        }
    }
    return moves;
}

function hasPath(start, goalRow, blocked) {
    const queue = [start];
    const seen = new Set([`${start[0]},${start[1]}`]);
    while (queue.length) {
        const [r, c] = queue.shift();
        if (r === goalRow) return true;
        for (const [dr, dc] of DIRS) {
            const nr = r + dr, nc = c + dc;
            const key = `${nr},${nc}`;
            if (inside(nr, nc) && !seen.has(key) && !blocked.has(edgeKey(r, c, nr, nc))) {
                seen.add(key);
                queue.push([nr, nc]);
            }
        }
    }
    return false;
}

/** Duvar yerel ön-kontrolü. Geçersizse Türkçe neden, geçerliyse null döner. */
function wallProblem(o, r, c) {
    if (!game) return "Oyun durumu yok.";
    if (r < 0 || r > SIZE - 2 || c < 0 || c > SIZE - 2) return "Duvar tahtanın dışına taşıyor.";
    if ((game.wallsLeft[myId] || 0) <= 0) return "Hiç duvarın kalmadı.";
    for (const w of game.walls) {
        if (w.r === r && w.c === c) return "Duvar mevcut bir duvarla çakışıyor.";
        if (o === "h" && w.o === "h" && w.r === r && Math.abs(w.c - c) === 1) return "Duvar mevcut bir duvarla çakışıyor.";
        if (o === "v" && w.o === "v" && w.c === c && Math.abs(w.r - r) === 1) return "Duvar mevcut bir duvarla çakışıyor.";
    }
    const blocked = blockedEdges(game.walls, { o, r, c });
    for (const pid of Object.keys(game.pawns)) {
        if (!hasPath(game.pawns[pid], game.goals[pid], blocked)) {
            return "Bu duvar bir oyuncunun tüm yollarını kapatıyor.";
        }
    }
    return null;
}

// ═════════════════════════════════════════════════════
// Tahta DOM'u (bir kez kurulur)
// Izgara: 17x17 iz — tek sayılı izler hücre, çiftler oluk.
// ═════════════════════════════════════════════════════

const cells = {};   // "r,c" -> element
const gh = {};      // yatay oluk parçası "r,c" (r 0..7, c 0..8): (r,c) ile (r+1,c) arası
const gv = {};      // dikey oluk parçası "r,c" (r 0..8, c 0..7): (r,c) ile (r,c+1) arası
const xn = {};      // kesişim düğümü "r,c" (r,c 0..7)

function buildBoard() {
    for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE; c++) {
            const el = document.createElement("button");
            el.type = "button";
            el.className = "cell";
            el.style.gridRow = String(2 * r + 1);
            el.style.gridColumn = String(2 * c + 1);
            el.addEventListener("click", () => onCellClick(r, c));
            cells[`${r},${c}`] = el;
            boardEl.appendChild(el);
        }
    }
    for (let r = 0; r < SIZE - 1; r++) {
        for (let c = 0; c < SIZE; c++) {
            const el = document.createElement("div");
            el.className = "groove gh";
            el.style.gridRow = String(2 * r + 2);
            el.style.gridColumn = String(2 * c + 1);
            // Yatay parçanın önerdiği duvar çapası: (r, min(c,7))
            const anchorC = Math.min(c, SIZE - 2);
            el.addEventListener("mouseenter", () => previewWall("h", r, anchorC));
            el.addEventListener("mouseleave", clearPreview);
            el.addEventListener("click", () => onWallClick("h", r, anchorC));
            gh[`${r},${c}`] = el;
            boardEl.appendChild(el);
        }
    }
    for (let r = 0; r < SIZE; r++) {
        for (let c = 0; c < SIZE - 1; c++) {
            const el = document.createElement("div");
            el.className = "groove gv";
            el.style.gridRow = String(2 * r + 1);
            el.style.gridColumn = String(2 * c + 2);
            const anchorR = Math.min(r, SIZE - 2);
            el.addEventListener("mouseenter", () => previewWall("v", anchorR, c));
            el.addEventListener("mouseleave", clearPreview);
            el.addEventListener("click", () => onWallClick("v", anchorR, c));
            gv[`${r},${c}`] = el;
            boardEl.appendChild(el);
        }
    }
    for (let r = 0; r < SIZE - 1; r++) {
        for (let c = 0; c < SIZE - 1; c++) {
            const el = document.createElement("div");
            el.className = "xnode";
            el.style.gridRow = String(2 * r + 2);
            el.style.gridColumn = String(2 * c + 2);
            xn[`${r},${c}`] = el;
            boardEl.appendChild(el);
        }
    }
}

/** Bir duvarın kapladığı DOM parçaları: 2 oluk parçası + kesişim düğümü. */
function wallParts(o, r, c) {
    if (o === "h") return [gh[`${r},${c}`], gh[`${r},${c + 1}`], xn[`${r},${c}`]];
    return [gv[`${r},${c}`], gv[`${r + 1},${c}`], xn[`${r},${c}`]];
}

// ── Çizim ───────────────────────────────────────────

function oppIdOf() {
    if (!game) return null;
    return Object.keys(game.pawns).find((id) => id !== myId) || null;
}

function playerInfo(pid) {
    return lobbyPlayers.find((p) => p.id === pid) || { name: "?", avatar: "🙂" };
}

function render() {
    if (!game) return;
    const oppId = oppIdOf();
    const myTurn = game.turn === myId;

    // Hücreleri temizle + piyonları yerleştir
    for (const key of Object.keys(cells)) {
        const el = cells[key];
        el.classList.remove("hl", "has-pawn");
        el.innerHTML = "";
    }
    for (const pid of Object.keys(game.pawns)) {
        const [r, c] = game.pawns[pid];
        const cell = cells[`${r},${c}`];
        const pawn = document.createElement("span");
        pawn.className = "pawn " + (pid === myId ? "pawn-me" : "pawn-opp");
        pawn.textContent = playerInfo(pid).avatar;
        cell.classList.add("has-pawn");
        cell.appendChild(pawn);
    }

    // Hamle vurguları
    if (myTurn && selectedPawn && !wallMode) {
        for (const [r, c] of legalMoves(myId)) {
            cells[`${r},${c}`].classList.add("hl");
        }
    }

    // Duvarlar
    for (const key of Object.keys(gh)) gh[key].classList.remove("wall");
    for (const key of Object.keys(gv)) gv[key].classList.remove("wall");
    for (const key of Object.keys(xn)) xn[key].classList.remove("wall");
    for (const w of game.walls) {
        for (const part of wallParts(w.o, w.r, w.c)) {
            if (part) part.classList.add("wall");
        }
    }

    // Hedef kenar vurgusu (kendi hedef satırın kendi renginde parlar)
    boardEl.classList.toggle("goal-top", game.goals[myId] === 0);
    boardEl.classList.toggle("goal-bottom", game.goals[myId] === SIZE - 1);

    // HUD
    fillCard($("card-me"), myId, myTurn);
    fillCard($("card-opp"), oppId, !myTurn && game.turn === oppId);
    const badge = $("turn-badge");
    badge.textContent = myTurn ? "Sıra sende!" : `Sıra: ${playerInfo(game.turn).name}`;
    badge.classList.toggle("mine", myTurn);

    $("goal-hint").textContent = game.goals[myId] === 0
        ? "🎯 Hedefin: EN ÜST satıra (↑) ulaşmak"
        : "🎯 Hedefin: EN ALT satıra (↓) ulaşmak";

    boardEl.classList.toggle("wall-mode", wallMode && myTurn);
    $("wall-mode-btn").classList.toggle("active", wallMode);
    $("mode-hint").textContent = wallMode
        ? "Olukların üzerine gel → önizleme; tıkla → duvar koy."
        : "Piyonuna dokun → yeşil hücreye git.";
}

function fillCard(card, pid, active) {
    if (!pid) return;
    const info = playerInfo(pid);
    card.querySelector(".pc-avatar").textContent = info.avatar;
    card.querySelector(".pc-name").textContent = info.name + (pid === myId ? " (sen)" : "");
    const left = game ? (game.wallsLeft[pid] ?? 0) : 0;
    card.querySelector(".pc-walls").textContent = `🧱 ${left}`;
    card.classList.toggle("active", !!active);
}

// ── Etkileşim ───────────────────────────────────────

function onCellClick(r, c) {
    if (!game || game.turn !== myId || wallMode) return;
    const [mr, mc] = game.pawns[myId];
    if (r === mr && c === mc) {
        selectedPawn = !selectedPawn;   // piyona tıkla → vurguları aç/kapa
        render();
        return;
    }
    if (!selectedPawn) return;
    const ok = legalMoves(myId).some(([lr, lc]) => lr === r && lc === c);
    if (!ok) return;
    send({ type: "move", to: [r, c] });
    selectedPawn = false;
}

function onWallClick(o, r, c) {
    if (!game || !wallMode || game.turn !== myId) return;
    const problem = wallProblem(o, r, c);
    if (problem) {
        toast(problem);
        return;
    }
    clearPreview();
    send({ type: "wall", orientation: o, r, c });
}

let previewParts = [];
function previewWall(o, r, c) {
    clearPreview();
    if (!game || !wallMode || game.turn !== myId) return;
    const bad = wallProblem(o, r, c) !== null;
    previewParts = wallParts(o, r, c).filter(Boolean);
    for (const part of previewParts) part.classList.add(bad ? "preview-bad" : "preview");
}
function clearPreview() {
    for (const part of previewParts) part.classList.remove("preview", "preview-bad");
    previewParts = [];
}

$("wall-mode-btn").addEventListener("click", () => {
    wallMode = !wallMode;
    selectedPawn = false;
    clearPreview();
    render();
});

// ═════════════════════════════════════════════════════
// WebSocket
// ═════════════════════════════════════════════════════

function send(data) {
    if (ws && ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(data));
}

function connectAndJoin(name, code) {
    $("conn-status").textContent = "Bağlanılıyor…";
    ws = new WebSocket(WS_URL);
    ws.addEventListener("open", () => {
        $("conn-status").textContent = "";
        send({ type: "join", game: "koridor", playerName: name, roomCode: code, avatar: myAvatar });
    });
    ws.addEventListener("message", (ev) => {
        let data;
        try { data = JSON.parse(ev.data); } catch { return; }
        handleMessage(data);
    });
    ws.addEventListener("close", () => {
        toast("Bağlantı koptu.");
        showJoin();
    });
    ws.addEventListener("error", () => {
        $("conn-status").textContent = "Sunucuya bağlanılamadı.";
    });
}

function handleMessage(data) {
    switch (data.type) {
        case "welcome":
            myId = data.playerId;
            roomCode = data.roomCode;
            isHost = data.isHost;
            $("room-code").textContent = roomCode;
            joinPanel.classList.add("hidden");
            roomPanel.classList.remove("hidden");
            break;

        case "lobby_update":
            lobbyPlayers = data.players || [];
            isHost = lobbyPlayers.some((p) => p.id === myId && p.isHost);
            renderLobby(data);
            if (game) render();  // isim/avatar güncellenmiş olabilir
            break;

        case "game_state":
            game = data;
            selectedPawn = false;
            $("overlay").classList.add("hidden");
            screenLobby.classList.add("hidden");
            screenGame.classList.remove("hidden");
            render();
            break;

        case "game_over":
            showGameOver(data);
            break;

        case "player_left":
            toast(`${data.playerName} odadan ayrıldı.`);
            break;

        case "chat":
            break;  // bu oyunda sohbet arayüzü yok

        case "error":
            toast(data.message || "Bir hata oluştu.");
            break;
    }
}

// ── Lobi arayüzü ────────────────────────────────────

function renderLobby(data) {
    const list = $("player-list");
    list.innerHTML = "";
    for (const p of lobbyPlayers) {
        const li = document.createElement("li");
        li.innerHTML = `<span class="pl-avatar"></span><span class="pl-name"></span>${p.isHost ? '<span class="pl-crown">👑</span>' : ""}`;
        li.querySelector(".pl-avatar").textContent = p.avatar;
        li.querySelector(".pl-name").textContent = p.name + (p.id === myId ? " (sen)" : "");
        list.appendChild(li);
    }

    const startBtn = $("start-btn");
    const waitNote = $("wait-note");
    if (data.state === "lobby") {
        startBtn.classList.toggle("hidden", !isHost);
        waitNote.classList.toggle("hidden", isHost);
        startBtn.disabled = lobbyPlayers.length < (data.minPlayers || 2);
        startBtn.textContent = startBtn.disabled
            ? `Oyuncu bekleniyor (${lobbyPlayers.length}/${data.minPlayers || 2})`
            : "Oyunu Başlat";
    }
    // Oyun bittiyse restart butonunu host durumuna göre tazele
    $("restart-btn").classList.toggle("hidden", !isHost);
    $("over-wait").classList.toggle("hidden", isHost);
}

function showJoin() {
    screenGame.classList.add("hidden");
    $("overlay").classList.add("hidden");
    screenLobby.classList.remove("hidden");
    roomPanel.classList.add("hidden");
    joinPanel.classList.remove("hidden");
    game = null;
}

function showGameOver(data) {
    const win = data.winnerId === myId;
    $("over-emoji").textContent = win ? "🏆" : "😔";
    $("over-title").textContent = win ? "Kazandın!" : `${data.winnerName} kazandı`;
    $("over-reason").textContent = data.reason || "";
    $("restart-btn").classList.toggle("hidden", !isHost);
    $("over-wait").classList.toggle("hidden", isHost);
    $("overlay").classList.remove("hidden");
}

$("start-btn").addEventListener("click", () => send({ type: "start_game" }));
$("restart-btn").addEventListener("click", () => send({ type: "restart" }));

$("copy-link-btn").addEventListener("click", async () => {
    const link = `${location.origin}${location.pathname}?room=${roomCode}`;
    try {
        await navigator.clipboard.writeText(link);
        toast("Davet linki kopyalandı!");
    } catch {
        prompt("Linki kopyala:", link);
    }
});

$("join-btn").addEventListener("click", () => {
    const name = $("name-input").value.trim();
    if (!name) {
        toast("Önce adını yaz.");
        return;
    }
    localStorage.setItem("koridor_name", name);
    localStorage.setItem("koridor_avatar", myAvatar);
    connectAndJoin(name, $("room-input").value.trim().toUpperCase());
});
$("name-input").addEventListener("keydown", (e) => { if (e.key === "Enter") $("join-btn").click(); });
$("room-input").addEventListener("keydown", (e) => { if (e.key === "Enter") $("join-btn").click(); });

// ── Toast ───────────────────────────────────────────

let toastTimer = null;
function toast(msg) {
    const el = $("toast");
    el.textContent = msg;
    el.classList.remove("hidden");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.add("hidden"), 3000);
}

// ── Başlangıç ───────────────────────────────────────

function initAvatarGrid() {
    const grid = $("avatar-grid");
    const saved = localStorage.getItem("koridor_avatar");
    if (saved && AVATARS.includes(saved)) myAvatar = saved;
    for (const a of AVATARS) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "avatar-btn" + (a === myAvatar ? " selected" : "");
        btn.textContent = a;
        btn.addEventListener("click", () => {
            myAvatar = a;
            grid.querySelectorAll(".avatar-btn").forEach((b) => b.classList.remove("selected"));
            btn.classList.add("selected");
        });
        grid.appendChild(btn);
    }
}

function init() {
    buildBoard();
    initAvatarGrid();
    const savedName = localStorage.getItem("koridor_name");
    if (savedName) $("name-input").value = savedName;
    const urlRoom = new URLSearchParams(location.search).get("room");
    if (urlRoom) $("room-input").value = urlRoom.toUpperCase();
}

init();
