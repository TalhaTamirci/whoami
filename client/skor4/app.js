/**
 * Skor 4 (Connect Four) — Arena istemcisi
 * Vanilla JS, framework yok.
 */

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

const ROWS = 6;
const COLS = 7;

const AVATAR_OPTIONS = ["🦊", "🐼", "🤖", "👻", "🦁", "🐙", "🦄", "😎", "🐯", "🥷", "🐸", "🐲"];

// ── Durum ───────────────────────────────────────────
let ws = null;
let myId = null;
let isHost = false;
let roomCode = "";
let lobbyPlayers = [];        // lobby_update'ten gelen liste
let gamePlayers = [];         // game_state'teki oyuncu sırası (renk eşlemesi)
let board = null;             // 6x7, null | playerId
let turnId = null;
let gameOver = false;
let joining = false;

// ── DOM kısayolları ─────────────────────────────────
const $ = (id) => document.getElementById(id);
const screens = {
    entry: $("screen-entry"),
    lobby: $("screen-lobby"),
    game: $("screen-game"),
};

function showScreen(name) {
    for (const [key, el] of Object.entries(screens)) {
        el.hidden = key !== name;
    }
}

// ── Toast ───────────────────────────────────────────
function toast(message, type = "info") {
    const el = document.createElement("div");
    el.className = `toast toast-${type}`;
    el.textContent = message;
    $("toasts").appendChild(el);
    setTimeout(() => {
        el.classList.add("toast-out");
        setTimeout(() => el.remove(), 350);
    }, 3200);
}

// ── Giriş ekranı kurulumu ───────────────────────────
let selectedAvatar = localStorage.getItem("skor4_avatar") || AVATAR_OPTIONS[0];
if (!AVATAR_OPTIONS.includes(selectedAvatar)) selectedAvatar = AVATAR_OPTIONS[0];

function buildAvatarGrid() {
    const grid = $("avatar-grid");
    grid.innerHTML = "";
    for (const emoji of AVATAR_OPTIONS) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "avatar-btn" + (emoji === selectedAvatar ? " selected" : "");
        btn.textContent = emoji;
        btn.setAttribute("aria-label", `Avatar ${emoji}`);
        btn.addEventListener("click", () => {
            selectedAvatar = emoji;
            localStorage.setItem("skor4_avatar", emoji);
            grid.querySelectorAll(".avatar-btn").forEach((b) => b.classList.remove("selected"));
            btn.classList.add("selected");
        });
        grid.appendChild(btn);
    }
}
buildAvatarGrid();

$("name-input").value = localStorage.getItem("skor4_name") || "";

// URL'den oda kodu oku (?room=KOD)
const urlRoom = new URLSearchParams(location.search).get("room");
if (urlRoom) $("room-input").value = urlRoom.toUpperCase().slice(0, 4);

$("room-input").addEventListener("input", (e) => {
    e.target.value = e.target.value.toUpperCase().replace(/[^A-Z]/g, "").slice(0, 4);
});

$("join-btn").addEventListener("click", join);
$("name-input").addEventListener("keydown", (e) => { if (e.key === "Enter") join(); });
$("room-input").addEventListener("keydown", (e) => { if (e.key === "Enter") join(); });

function setEntryStatus(text) {
    const el = $("entry-status");
    el.hidden = !text;
    el.textContent = text || "";
}

function join() {
    if (joining) return;
    const name = $("name-input").value.trim();
    if (!name) {
        toast("Önce adını yaz!", "error");
        $("name-input").focus();
        return;
    }
    localStorage.setItem("skor4_name", name);
    joining = true;
    $("join-btn").disabled = true;
    setEntryStatus("Sunucuya bağlanılıyor...");

    ws = new WebSocket(WS_URL);

    ws.addEventListener("open", () => {
        setEntryStatus("Odaya katılınıyor...");
        ws.send(JSON.stringify({
            type: "join",
            game: "skor4",
            playerName: name,
            roomCode: $("room-input").value.trim().toUpperCase(),
            avatar: selectedAvatar,
        }));
    });

    ws.addEventListener("message", (event) => {
        let data;
        try { data = JSON.parse(event.data); } catch { return; }
        handleMessage(data);
    });

    ws.addEventListener("close", () => {
        joining = false;
        $("join-btn").disabled = false;
        if (myId) toast("Sunucu bağlantısı koptu.", "error");
        myId = null;
        setEntryStatus("Bağlantı kapandı. Tekrar katılabilirsin.");
        showScreen("entry");
    });

    ws.addEventListener("error", () => {
        setEntryStatus("Sunucuya bağlanılamadı.");
    });
}

// ── Mesaj işleme ────────────────────────────────────
function handleMessage(data) {
    switch (data.type) {
        case "welcome":
            myId = data.playerId;
            isHost = data.isHost;
            roomCode = data.roomCode;
            joining = false;
            $("join-btn").disabled = false;
            setEntryStatus("");
            $("room-code-label").textContent = roomCode;
            showScreen("lobby");
            break;

        case "lobby_update":
            lobbyPlayers = data.players || [];
            const me = lobbyPlayers.find((p) => p.id === myId);
            isHost = !!(me && me.isHost);
            renderLobby(data);
            updateRestartButtons();
            if (data.state === "lobby") showScreen("lobby");
            break;

        case "game_state":
            handleGameState(data);
            break;

        case "game_over":
            handleGameOver(data);
            break;

        case "player_left":
            toast(`${data.playerName} odadan ayrıldı.`, "error");
            break;

        case "chat":
            // Bu istemcide sohbet arayüzü yok — sessizce yok say
            break;

        case "error":
            if (!myId) {
                joining = false;
                $("join-btn").disabled = false;
                setEntryStatus("");
            }
            toast(data.message || "Bir hata oluştu.", "error");
            break;
    }
}

// ── Lobi ────────────────────────────────────────────
function renderLobby(data) {
    const list = $("lobby-players");
    list.innerHTML = "";
    for (const p of lobbyPlayers) {
        const li = document.createElement("li");
        li.className = "player-item" + (p.id === myId ? " me" : "");
        li.innerHTML = `
            <span class="player-avatar">${escapeHtml(p.avatar || "🙂")}</span>
            <span class="player-name">${escapeHtml(p.name)}${p.id === myId ? " (sen)" : ""}</span>
            ${p.isHost ? '<span class="host-badge" title="Host">👑</span>' : ""}
        `;
        list.appendChild(li);
    }
    $("player-count").textContent = `(${lobbyPlayers.length}/${data.maxPlayers || 2})`;

    const enough = lobbyPlayers.length >= (data.minPlayers || 2);
    $("start-btn").hidden = !isHost;
    $("start-btn").disabled = !enough;
    $("host-note").hidden = isHost;
    $("need-note").hidden = !(isHost && !enough);
}

$("start-btn").addEventListener("click", () => {
    send({ type: "start_game" });
});

$("copy-code-btn").addEventListener("click", () => copyText(roomCode, "Oda kodu kopyalandı!"));
$("copy-link-btn").addEventListener("click", () => {
    const url = `${location.origin}${location.pathname}?room=${roomCode}`;
    copyText(url, "Davet linki kopyalandı!");
});

function copyText(text, okMessage) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text)
            .then(() => toast(okMessage, "success"))
            .catch(() => fallbackCopy(text, okMessage));
    } else {
        fallbackCopy(text, okMessage);
    }
}

function fallbackCopy(text, okMessage) {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try {
        document.execCommand("copy");
        toast(okMessage, "success");
    } catch {
        toast("Kopyalanamadı: " + text, "error");
    }
    ta.remove();
}

// ── Tahta kurulumu ──────────────────────────────────
const boardEl = $("board");
const cellEls = [];   // cellEls[row][col]

function buildBoard() {
    boardEl.innerHTML = "";
    cellEls.length = 0;
    for (let r = 0; r < ROWS; r++) {
        const rowArr = [];
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement("div");
            cell.className = "cell";
            cell.dataset.col = String(c);
            const disc = document.createElement("div");
            disc.className = "disc";
            cell.appendChild(disc);
            boardEl.appendChild(cell);
            rowArr.push(cell);
        }
        cellEls.push(rowArr);
    }
}
buildBoard();

boardEl.addEventListener("click", (e) => {
    const cell = e.target.closest(".cell");
    if (!cell) return;
    tryDrop(parseInt(cell.dataset.col, 10));
});

// Hayalet önizleme (hover)
boardEl.addEventListener("mouseover", (e) => {
    const cell = e.target.closest(".cell");
    if (cell) showGhost(parseInt(cell.dataset.col, 10));
});
boardEl.addEventListener("mouseleave", clearGhost);

let ghostCell = null;

function showGhost(col) {
    clearGhost();
    if (gameOver || !board || turnId !== myId) return;
    const row = lowestEmptyRow(col);
    if (row === -1) return;
    const cell = cellEls[row][col];
    cell.querySelector(".disc").classList.add("ghost", colorClass(myId));
    ghostCell = cell;
}

function clearGhost() {
    if (ghostCell) {
        ghostCell.querySelector(".disc").classList.remove("ghost", "p1", "p2");
        // Dolu hücreyse rengini geri ver
        syncCellFromBoard(ghostCell);
        ghostCell = null;
    }
}

function lowestEmptyRow(col) {
    for (let r = ROWS - 1; r >= 0; r--) {
        if (board[r][col] === null) return r;
    }
    return -1;
}

function tryDrop(col) {
    if (!board || gameOver) return;
    if (turnId !== myId) {
        toast("Sıra sende değil!", "error");
        return;
    }
    if (lowestEmptyRow(col) === -1) {
        toast("Bu sütun dolu.", "error");
        return;
    }
    clearGhost();
    send({ type: "drop", col });
}

function colorClass(playerId) {
    const idx = gamePlayers.findIndex((p) => p.id === playerId);
    return idx === 1 ? "p2" : "p1";
}

function syncCellFromBoard(cell) {
    const col = parseInt(cell.dataset.col, 10);
    const row = cellEls.findIndex((rowArr) => rowArr[col] === cell);
    if (row === -1 || !board) return;
    const owner = board[row][col];
    const disc = cell.querySelector(".disc");
    disc.classList.remove("ghost");
    if (owner) {
        disc.classList.add("filled", colorClass(owner));
    }
}

// ── Oyun durumu ─────────────────────────────────────
function handleGameState(data) {
    board = data.board;
    turnId = data.turn;
    gameOver = false; // yeni state geldiyse oyun akışta (bittiyse game_over ayrıca gelir)
    if (Array.isArray(data.players) && data.players.length) {
        gamePlayers = data.players;
    }

    $("gameover-overlay").hidden = true;
    showScreen("game");
    clearGhost();
    renderScoreboard(data.series || {});
    renderTurn();
    renderBoard(data.lastMove);
}

function renderBoard(lastMove) {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const disc = cellEls[r][c].querySelector(".disc");
            const owner = board[r][c];
            const wasFilled = disc.classList.contains("filled");
            disc.classList.remove("ghost", "win");
            if (owner) {
                disc.classList.remove("p1", "p2");
                disc.classList.add("filled", colorClass(owner));
                // Yeni düşen taşa animasyon
                if (!wasFilled && lastMove && lastMove[0] === r && lastMove[1] === c) {
                    disc.style.setProperty("--drop-cells", String(r + 1));
                    disc.classList.remove("dropping");
                    void disc.offsetWidth; // animasyonu yeniden tetikle
                    disc.classList.add("dropping");
                }
            } else {
                disc.classList.remove("filled", "p1", "p2", "dropping");
                disc.style.removeProperty("--drop-cells");
            }
        }
    }
}

function renderScoreboard(series) {
    for (let i = 0; i < 2; i++) {
        const p = gamePlayers[i];
        $(`score-avatar-${i}`).textContent = p ? p.avatar : "🙂";
        $(`score-name-${i}`).textContent = p ? p.name + (p.id === myId ? " (sen)" : "") : "—";
        $(`score-wins-${i}`).textContent = p ? String(series[p.id] || 0) : "0";
        $(`score-card-${i}`).classList.toggle("active", !!p && p.id === turnId && !gameOver);
    }
}

function renderTurn() {
    const disc = $("turn-disc");
    disc.className = "mini-disc";
    if (gameOver || !turnId) {
        $("turn-text").textContent = "Oyun bitti";
        return;
    }
    disc.classList.add(colorClass(turnId));
    if (turnId === myId) {
        $("turn-text").textContent = "Sıra sende — bir sütuna dokun!";
        $("turn-banner").classList.add("my-turn");
    } else {
        const p = gamePlayers.find((pl) => pl.id === turnId);
        $("turn-text").textContent = `Sıra: ${p ? p.name : "rakip"}`;
        $("turn-banner").classList.remove("my-turn");
    }
}

// ── Oyun sonu ───────────────────────────────────────
function handleGameOver(data) {
    gameOver = true;
    turnId = null;
    clearGhost();

    // Kazanan 4'lüyü parlat
    for (const [r, c] of data.winningCells || []) {
        cellEls[r][c].querySelector(".disc").classList.add("win");
    }

    renderScoreboard(data.series || {});
    $("turn-banner").classList.remove("my-turn");
    $("turn-text").textContent = "Oyun bitti";
    $("turn-disc").className = "mini-disc";

    const title = $("gameover-title");
    const sub = $("gameover-sub");
    const emoji = $("gameover-emoji");

    if (!data.winnerId) {
        emoji.textContent = "🤝";
        title.textContent = "Berabere!";
        sub.textContent = "Tahta doldu, kazanan yok.";
    } else if (data.winnerId === myId) {
        emoji.textContent = "🏆";
        title.textContent = "Kazandın!";
        sub.textContent = data.reason === "opponent_left"
            ? "Rakibin oyundan ayrıldı."
            : "4'lüyü tamamladın, tebrikler!";
    } else {
        emoji.textContent = "😔";
        title.textContent = `${data.winnerName || "Rakip"} kazandı`;
        sub.textContent = data.reason === "opponent_left"
            ? "Rakip ayrıldığı için oyun bitti."
            : "Bir dahaki sefere!";
    }

    // Seri skoru
    const seriesEl = $("gameover-series");
    seriesEl.innerHTML = "";
    gamePlayers.forEach((p, i) => {
        const div = document.createElement("div");
        div.className = "series-chip " + (i === 1 ? "p2" : "p1");
        div.innerHTML = `<span>${escapeHtml(p.avatar)} ${escapeHtml(p.name)}</span><strong>${(data.series || {})[p.id] || 0}</strong>`;
        seriesEl.appendChild(div);
    });

    updateRestartButtons();

    // Taş animasyonu + parlamayı görebilmek için kısa gecikme
    setTimeout(() => { $("gameover-overlay").hidden = false; }, 900);
}

function updateRestartButtons() {
    const canRestart = isHost && lobbyPlayers.length >= 2;
    $("restart-btn").hidden = !isHost;
    $("restart-btn").disabled = !canRestart;
    if (isHost && !canRestart) {
        $("restart-note").hidden = false;
        $("restart-note").textContent = "Rakip ayrıldı — yeni oyun için yeni oda kur.";
    } else {
        $("restart-note").hidden = isHost;
        $("restart-note").textContent = "Host'un yeni oyun başlatması bekleniyor...";
    }
}

$("restart-btn").addEventListener("click", () => {
    send({ type: "restart" });
});

// ── Yardımcılar ─────────────────────────────────────
function send(obj) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(obj));
    }
}

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}
