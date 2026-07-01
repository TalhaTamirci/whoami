/**
 * Noktalar — Noktalar ve Kutular (Dots and Boxes) istemcisi
 * Vanilla JS, framework yok. Sunucu otoriter; burası sadece görünüm + istek.
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

const GAME_TYPE = "noktalar";

const AVATAR_OPTIONS = ["🦊", "🐼", "🐸", "🦄", "🤖", "👻", "😎", "🐙", "🐯", "🐧", "🥷", "🐲"];

// Oyuncu renk paleti (sıraya göre atanır)
const COLORS = ["#7c5cff", "#00e5a0", "#ffb020", "#ff5c7a"];

// ── DOM kısayolları ─────────────────────────────────
const $ = (sel) => document.querySelector(sel);

const screens = {
    entry: $("#screen-entry"),
    lobby: $("#screen-lobby"),
    game: $("#screen-game"),
};

// ── Durum ───────────────────────────────────────────
let ws = null;
let joined = false;
let playerId = null;
let roomCode = null;
let isHost = false;
let minPlayers = 2;
let players = [];            // lobby_update'ten gelen sıralı liste
let colorMap = {};           // playerId -> renk (oyun başında sabitlenir)
let lastState = null;        // son game_state
let selectedAvatar = localStorage.getItem("noktalar_avatar") || AVATAR_OPTIONS[0];
let lastChosenSize = 5;

// ── Yardımcılar ─────────────────────────────────────
function showScreen(name) {
    Object.entries(screens).forEach(([key, el]) => {
        el.classList.toggle("hidden", key !== name);
    });
}

function toast(message, kind = "error") {
    const wrap = $("#toast-wrap");
    const el = document.createElement("div");
    el.className = `toast ${kind}`;
    el.textContent = message;
    wrap.appendChild(el);
    setTimeout(() => el.classList.add("show"), 10);
    setTimeout(() => {
        el.classList.remove("show");
        setTimeout(() => el.remove(), 300);
    }, 3200);
}

function playerById(id) {
    return players.find((p) => p.id === id) || null;
}

function playerName(id) {
    const p = playerById(id);
    return p ? p.name : "?";
}

function playerAvatar(id) {
    const p = playerById(id);
    return p ? p.avatar : "🙂";
}

function colorOf(id) {
    if (!(id in colorMap)) {
        colorMap[id] = COLORS[Object.keys(colorMap).length % COLORS.length];
    }
    return colorMap[id];
}

function send(data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
    }
}

// ── Giriş ekranı kurulumu ───────────────────────────
function initEntry() {
    const nameInput = $("#name-input");
    nameInput.value = localStorage.getItem("noktalar_name") || "";

    // URL'den oda kodu (?room=KOD)
    const urlRoom = new URLSearchParams(location.search).get("room");
    if (urlRoom) $("#room-input").value = urlRoom.toUpperCase();

    // Avatar seçici
    const grid = $("#avatar-grid");
    AVATAR_OPTIONS.forEach((emoji) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "avatar-btn" + (emoji === selectedAvatar ? " selected" : "");
        btn.textContent = emoji;
        btn.addEventListener("click", () => {
            selectedAvatar = emoji;
            localStorage.setItem("noktalar_avatar", emoji);
            grid.querySelectorAll(".avatar-btn").forEach((b) => b.classList.remove("selected"));
            btn.classList.add("selected");
        });
        grid.appendChild(btn);
    });

    $("#join-btn").addEventListener("click", joinRoom);
    nameInput.addEventListener("keydown", (e) => { if (e.key === "Enter") joinRoom(); });
    $("#room-input").addEventListener("keydown", (e) => { if (e.key === "Enter") joinRoom(); });
}

function joinRoom() {
    const name = $("#name-input").value.trim();
    if (!name) {
        toast("Önce adını yaz!");
        return;
    }
    localStorage.setItem("noktalar_name", name);
    const code = $("#room-input").value.trim().toUpperCase();

    $("#join-btn").disabled = true;
    $("#join-btn").textContent = "Bağlanılıyor...";

    ws = new WebSocket(WS_URL);
    ws.addEventListener("open", () => {
        send({
            type: "join",
            game: GAME_TYPE,
            playerName: name,
            roomCode: code,
            avatar: selectedAvatar,
        });
    });
    ws.addEventListener("message", (ev) => {
        let msg;
        try { msg = JSON.parse(ev.data); } catch { return; }
        handleMessage(msg);
    });
    ws.addEventListener("close", () => {
        resetJoinButton();
        if (joined) {
            toast("Sunucu bağlantısı koptu.");
            joined = false;
            showScreen("entry");
        }
    });
    ws.addEventListener("error", () => {
        resetJoinButton();
        toast("Sunucuya bağlanılamadı.");
    });
}

function resetJoinButton() {
    $("#join-btn").disabled = false;
    $("#join-btn").textContent = "Odaya Katıl";
}

// ── Mesaj işleme ────────────────────────────────────
function handleMessage(msg) {
    switch (msg.type) {
        case "welcome":
            joined = true;
            playerId = msg.playerId;
            roomCode = msg.roomCode;
            isHost = msg.isHost;
            resetJoinButton();
            $("#room-code-label").textContent = roomCode;
            showScreen("lobby");
            break;

        case "lobby_update":
            players = msg.players;
            minPlayers = msg.minPlayers;
            isHost = players.some((p) => p.id === playerId && p.isHost);
            renderLobby();
            if (lastState) renderScoreboard(lastState); // isimler güncellensin
            updateOverlayControls();
            break;

        case "player_left":
            toast(`${msg.playerName} odadan ayrıldı.`, "info");
            break;

        case "game_state":
            handleGameState(msg);
            break;

        case "game_over":
            handleGameOver(msg);
            break;

        case "error":
            if (!joined) resetJoinButton();
            toast(msg.message);
            break;
    }
}

function handleGameState(gs) {
    // Yeni oyun: oyun ekranı kapalı (ilk başlangıç) veya oyun-sonu ekranı açık (restart)
    const overlayOpen = !$("#gameover-overlay").classList.contains("hidden");
    const firstState = screens.game.classList.contains("hidden") || overlayOpen;
    if (firstState) {
        colorMap = {};
        players.forEach((p) => colorOf(p.id)); // renkleri sırayla sabitle
        $("#gameover-overlay").classList.add("hidden");
        showScreen("game");
    }
    lastState = gs;

    renderTurnBar(gs);
    renderScoreboard(gs);
    renderBoard(gs);
    renderMoveNote(gs);
}

function handleGameOver(msg) {
    if (lastState) lastState.turn = null;
    if (lastState) renderTurnBar(lastState);

    const overlay = $("#gameover-overlay");
    overlay.classList.remove("hidden");

    const winners = msg.winnerIds || [];
    const title = $("#over-title");
    if (winners.length > 1) {
        title.textContent = "🤝 Beraberlik!";
    } else if (winners.length === 1) {
        const win = winners[0];
        title.textContent = win === playerId
            ? "🏆 Kazandın!"
            : `🏆 ${playerAvatar(win)} ${playerName(win)} kazandı!`;
    } else {
        title.textContent = "Oyun bitti";
    }
    $("#over-reason").textContent = msg.reason || "";

    // Skor tablosu (yüksekten düşüğe)
    const scoresEl = $("#over-scores");
    scoresEl.innerHTML = "";
    const entries = Object.entries(msg.scores || {}).sort((a, b) => b[1] - a[1]);
    entries.forEach(([pid, score]) => {
        const row = document.createElement("div");
        row.className = "over-score-row" + (winners.includes(pid) ? " winner" : "");
        row.innerHTML = `
            <span class="chip" style="background:${colorOf(pid)}"></span>
            <span class="ps-name">${playerAvatar(pid)} ${escapeHtml(playerName(pid))}</span>
            <span class="ps-score">${score}</span>`;
        scoresEl.appendChild(row);
    });

    updateOverlayControls();
}

function updateOverlayControls() {
    const overlayOpen = !$("#gameover-overlay").classList.contains("hidden");
    if (!overlayOpen) return;
    $("#restart-btn").classList.toggle("hidden", !isHost);
    $("#over-wait").classList.toggle("hidden", isHost);
}

// ── Lobi görünümü ───────────────────────────────────
function renderLobby() {
    const list = $("#player-list");
    list.innerHTML = "";
    players.forEach((p) => {
        const li = document.createElement("li");
        li.className = "player-item" + (p.id === playerId ? " me" : "");
        li.innerHTML = `
            <span class="p-avatar">${p.avatar}</span>
            <span class="p-name">${escapeHtml(p.name)}${p.id === playerId ? " (sen)" : ""}</span>
            ${p.isHost ? '<span class="p-host" title="Oda sahibi">👑</span>' : ""}`;
        list.appendChild(li);
    });
    $("#player-count").textContent = `(${players.length}/4)`;

    $("#host-controls").classList.toggle("hidden", !isHost);
    $("#wait-note").classList.toggle("hidden", isHost);

    const startBtn = $("#start-btn");
    const enough = players.length >= minPlayers;
    startBtn.disabled = !enough;
    $("#min-note").textContent = enough
        ? ""
        : `Başlamak için en az ${minPlayers} oyuncu gerekli.`;
}

// ── Oyun görünümü ───────────────────────────────────
function renderTurnBar(gs) {
    const bar = $("#turn-bar");
    if (!gs.turn) {
        bar.innerHTML = "";
        bar.classList.remove("my-turn");
        return;
    }
    const mine = gs.turn === playerId;
    bar.classList.toggle("my-turn", mine);
    bar.innerHTML = mine
        ? `<span class="turn-dot" style="background:${colorOf(gs.turn)}"></span> Sıra sende — bir çizgi çek!`
        : `<span class="turn-dot" style="background:${colorOf(gs.turn)}"></span> Sıra: ${playerAvatar(gs.turn)} ${escapeHtml(playerName(gs.turn))}`;
}

function renderScoreboard(gs) {
    const board = $("#scoreboard");
    board.innerHTML = "";
    Object.keys(gs.scores).forEach((pid) => {
        const div = document.createElement("div");
        div.className = "score-card" + (gs.turn === pid ? " active" : "");
        div.style.setProperty("--pc", colorOf(pid));
        const left = playerById(pid) === null ? " (ayrıldı)" : "";
        div.innerHTML = `
            <span class="sc-avatar">${playerAvatar(pid)}</span>
            <span class="sc-name">${escapeHtml(playerName(pid))}${left}</span>
            <span class="sc-score">${gs.scores[pid]}</span>`;
        board.appendChild(div);
    });
}

function renderMoveNote(gs) {
    const note = $("#move-note");
    if (gs.captured && gs.captured.length && gs.turn) {
        // Kutu kapatan oyuncu sırayı korur → gs.turn kapatan kişidir
        note.textContent = gs.turn === playerId
            ? `✨ ${gs.captured.length} kutu kapattın — ekstra hamle senin!`
            : `✨ ${playerName(gs.turn)} ${gs.captured.length} kutu kapattı — ekstra hamle onun!`;
        note.classList.add("visible");
    } else {
        note.textContent = "";
        note.classList.remove("visible");
    }
}

// SVG tahta — her game_state'te yeniden çizilir
const SVG_NS = "http://www.w3.org/2000/svg";
const CELL = 72;   // kutu kenarı (viewBox birimi)
const PAD = 30;    // kenar boşluğu
const HIT = 34;    // tıklama alanı kalınlığı

function svgEl(tag, attrs) {
    const el = document.createElementNS(SVG_NS, tag);
    for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
    return el;
}

function renderBoard(gs) {
    const svg = $("#board");
    const n = gs.size;
    const W = PAD * 2 + n * CELL;
    svg.setAttribute("viewBox", `0 0 ${W} ${W}`);
    svg.innerHTML = "";
    svg.classList.toggle("my-turn", gs.turn === playerId);

    const px = (c) => PAD + c * CELL;
    const hSet = new Map(gs.hLines.map((l) => [`${l.r},${l.c}`, l.player]));
    const vSet = new Map(gs.vLines.map((l) => [`${l.r},${l.c}`, l.player]));
    const capturedSet = new Set((gs.captured || []).map(([r, c]) => `${r},${c}`));

    // 1) Kapatılan kutular (en altta)
    for (let r = 0; r < n; r++) {
        for (let c = 0; c < n; c++) {
            const owner = gs.boxes[r][c];
            if (!owner) continue;
            const g = svgEl("g", { class: "box" + (capturedSet.has(`${r},${c}`) ? " just-captured" : "") });
            g.appendChild(svgEl("rect", {
                x: px(c) + 7, y: px(r) + 7,
                width: CELL - 14, height: CELL - 14,
                rx: 10, fill: colorOf(owner), "fill-opacity": 0.22,
                stroke: colorOf(owner), "stroke-opacity": 0.55, "stroke-width": 1.5,
            }));
            const label = svgEl("text", {
                x: px(c) + CELL / 2, y: px(r) + CELL / 2,
                "text-anchor": "middle", "dominant-baseline": "central",
                "font-size": 26,
            });
            label.textContent = playerAvatar(owner);
            g.appendChild(label);
            svg.appendChild(g);
        }
    }

    // 2) Çizilmiş çizgiler
    const drawLine = (x1, y1, x2, y2, owner) => {
        svg.appendChild(svgEl("line", {
            x1, y1, x2, y2,
            class: "drawn-line",
            stroke: colorOf(owner), "stroke-width": 6, "stroke-linecap": "round",
        }));
    };
    hSet.forEach((owner, key) => {
        const [r, c] = key.split(",").map(Number);
        drawLine(px(c) + 6, px(r), px(c + 1) - 6, px(r), owner);
    });
    vSet.forEach((owner, key) => {
        const [r, c] = key.split(",").map(Number);
        drawLine(px(c), px(r) + 6, px(c), px(r + 1) - 6, owner);
    });

    // 3) Boş kenarlar için tıklama alanları
    const addEdge = (kind, r, c, x, y, w, h) => {
        const hit = svgEl("rect", {
            x, y, width: w, height: h, rx: 8,
            class: "edge",
            "data-kind": kind, "data-r": r, "data-c": c,
        });
        hit.addEventListener("click", () => onEdgeClick(kind, r, c));
        svg.appendChild(hit);
    };
    for (let r = 0; r <= n; r++) {         // yatay kenarlar
        for (let c = 0; c < n; c++) {
            if (hSet.has(`${r},${c}`)) continue;
            addEdge("h", r, c, px(c) + 8, px(r) - HIT / 2, CELL - 16, HIT);
        }
    }
    for (let r = 0; r < n; r++) {          // dikey kenarlar
        for (let c = 0; c <= n; c++) {
            if (vSet.has(`${r},${c}`)) continue;
            addEdge("v", r, c, px(c) - HIT / 2, px(r) + 8, HIT, CELL - 16);
        }
    }

    // 4) Noktalar (en üstte)
    for (let r = 0; r <= n; r++) {
        for (let c = 0; c <= n; c++) {
            svg.appendChild(svgEl("circle", {
                cx: px(c), cy: px(r), r: 5.5, class: "dot",
            }));
        }
    }
}

function onEdgeClick(kind, r, c) {
    if (!lastState || lastState.turn !== playerId) {
        toast("Sıra sende değil.");
        return;
    }
    // Sunucu yine de doğrular — burası sadece kullanıcı deneyimi
    send({ type: "line", kind, r, c });
}

// ── Lobi butonları ──────────────────────────────────
$("#copy-link-btn").addEventListener("click", async () => {
    const url = `${location.origin}${location.pathname}?room=${roomCode}`;
    try {
        await navigator.clipboard.writeText(url);
        toast("Davet linki kopyalandı!", "info");
    } catch {
        toast(`Davet linki: ${url}`, "info");
    }
});

$("#start-btn").addEventListener("click", () => {
    lastChosenSize = parseInt($("#size-select").value, 10) || 5;
    send({ type: "start_game", size: lastChosenSize });
});

$("#restart-btn").addEventListener("click", () => {
    send({ type: "restart", size: lastChosenSize });
});

// ── Küçük yardımcı ──────────────────────────────────
function escapeHtml(str) {
    return String(str)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
}

initEntry();
