/**
 * Ben Kimim? — Client WebSocket + UI Mantığı
 */

// ── Ayarlar ─────────────────────────────────────────
// WS sunucusu:
//   - oyun.ahmetkadir.com → ws.oyun.ahmetkadir.com (subdomain)
//   - localhost dev → ws://localhost:8765
//   - GitHub Pages / fallback → Render
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

const AVATAR_OPTIONS = [
    "🎭", "🦊", "🐶", "🐱", "🐼", "🐯",
    "🐸", "🐵", "🦁", "🐺", "🐧", "🐙",
    "🦄", "🐲", "🤖", "👻", "😎", "🥷",
    "👽", "🧙", "🧛", "🧝", "🤡", "💀",
];

// ── State ───────────────────────────────────────────
let ws = null;
let myPlayerId = null;
let myRoomCode = null;
let isHost = false;
let currentPlayers = [];
let myAvatar = localStorage.getItem("whoami:avatar") || "🎭";
let soundEnabled = localStorage.getItem("whoami:sound") !== "off";

let turnPlayerId = null;
let timerRemaining = 0;
let timerTotal = 0;
let qaLog = [];
let logPanelSeenCount = 0;

// ── DOM Referansları ────────────────────────────────
const $ = (id) => document.getElementById(id);

const screenLobby = $("screen-lobby");
const screenGame = $("screen-game");
const screenResult = $("screen-result");

// Lobby
const inputName = $("input-name");
const inputRoom = $("input-room");
const btnJoin = $("btn-join");
const lobbyInfo = $("lobby-info");
const displayRoomCode = $("display-room-code");
const btnCopyCode = $("btn-copy-code");
const btnCopyLink = $("btn-copy-link");
const playerList = $("player-list");
const hostControls = $("host-controls");
const btnStart = $("btn-start");
const selectCategory = $("select-category");
const selectDifficulty = $("select-difficulty");
const inputTimer = $("input-timer");
const poolSizeGroup = $("pool-size-group");
const inputPoolSize = $("input-pool-size");
const customCategoryGroup = $("custom-category-group");
const inputCustomWords = $("input-custom-words");
const waitingMsg = $("waiting-msg");
const connectionStatus = $("connection-status");
const avatarGrid = $("avatar-grid");

// Oyun
const gameRoomCode = $("game-room-code");
const playersCircle = $("players-circle");
const inputGuess = $("input-guess");
const btnGuess = $("btn-guess");
const guessFeedback = $("guess-feedback");
const turnBar = $("turn-bar");
const turnPlayerName = $("turn-player-name");
const timerPill = $("timer-pill");
const timerValue = $("timer-value");
const btnPass = $("btn-pass");

// Q&A log
const btnLogToggle = $("btn-log-toggle");
const logFabBadge = $("log-fab-badge");
const logPanel = $("log-panel");
const btnLogClose = $("btn-log-close");
const logList = $("log-list");
const logInput = $("log-input");
const btnLogSend = $("btn-log-send");
const logQuickBtns = document.querySelectorAll(".log-quick-btn");

// Sonuç
const rankingsList = $("rankings-list");
const hostControlsResult = $("host-controls-result");
const btnNewRound = $("btn-new-round");
const selectCategoryResult = $("select-category-result");
const waitingNewRound = $("waiting-new-round");

// Eleme Paneli (mevcut)
const elimFab = $("btn-elim-toggle");
const elimFabBadge = $("elim-fab-badge");
const elimPanel = $("elim-panel");
const elimClose = $("btn-elim-close");
const elimCount = $("elim-count");
const elimNotes = $("elim-notes");
const elimSearch = $("elim-search");
const elimReset = $("btn-elim-reset");
const elimList = $("elim-list");
const elimTabs = document.querySelectorAll(".elim-tab");

// Üst kontrol butonları
const btnSoundToggle = $("btn-sound-toggle");
const soundIconOn = $("sound-icon-on");
const soundIconOff = $("sound-icon-off");

// 3-state elim:  state ∈ {"active", "suspect", "eliminated"}
let elimItems = [];
let elimState = {};   // { itemName: "suspect" | "eliminated" }
let elimCategory = null;
let elimFilter = "all";
let elimSearchTerm = "";


// ══════════════════════════════════════════════════
// EKRAN GEÇİŞİ
// ══════════════════════════════════════════════════

function showScreen(screen) {
    [screenLobby, screenGame, screenResult].forEach((s) => {
        s.classList.remove("active");
    });
    screen.classList.add("active");
}


// ══════════════════════════════════════════════════
// SES EFEKTLERİ (Web Audio synth)
// ══════════════════════════════════════════════════

let audioCtx = null;
function getAudioCtx() {
    if (!audioCtx) {
        try { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
        catch (e) { return null; }
    }
    return audioCtx;
}

function playTone(freq, duration = 0.12, type = "sine", volume = 0.18) {
    if (!soundEnabled) return;
    const ctx = getAudioCtx();
    if (!ctx) return;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(volume, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + duration);
}

const sounds = {
    correct: () => { playTone(660, 0.1); setTimeout(() => playTone(880, 0.15), 90); },
    wrong:   () => playTone(180, 0.2, "square", 0.14),
    join:    () => playTone(520, 0.1, "triangle"),
    turn:    () => playTone(440, 0.08, "sine"),
    tick:    () => playTone(800, 0.04, "square", 0.08),
    gameOver:() => { [523, 659, 784, 1047].forEach((f, i) => setTimeout(() => playTone(f, 0.18), i * 100)); },
    message: () => playTone(720, 0.06, "triangle", 0.12),
};


// ══════════════════════════════════════════════════
// WEBSOCKET BAĞLANTISI
// ══════════════════════════════════════════════════

function connectWebSocket() {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        connectionStatus.textContent = "● Bağlandı";
        connectionStatus.className = "status-connected";

        ws.send(JSON.stringify({
            type: "join",
            playerName: inputName.value.trim(),
            roomCode: inputRoom.value.trim().toUpperCase(),
        }));
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleMessage(data);
    };

    ws.onclose = () => {
        connectionStatus.textContent = "● Bağlantı kesildi";
        connectionStatus.className = "status-disconnected";
    };

    ws.onerror = () => {
        connectionStatus.textContent = "● Bağlantı hatası";
        connectionStatus.className = "status-disconnected";
    };
}

function sendMessage(data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
    }
}


// ══════════════════════════════════════════════════
// EVENT HANDLER — Sunucudan gelen mesajları işle
// ══════════════════════════════════════════════════

function handleMessage(data) {
    switch (data.type) {
        case "welcome":          handleWelcome(data); break;
        case "lobby_update":     handleLobbyUpdate(data); break;
        case "game_started":     handleGameStarted(data); break;
        case "guess_result":     handleGuessResult(data); break;
        case "player_revealed":  handlePlayerRevealed(data); break;
        case "game_over":        handleGameOver(data); break;
        case "turn_changed":     handleTurnChanged(data); break;
        case "timer_tick":       handleTimerTick(data); break;
        case "timer_expired":    handleTimerExpired(data); break;
        case "log_message":      handleLogMessage(data); break;
        case "error":            handleError(data); break;
        default: console.warn("[WS] Bilinmeyen event:", data.type);
    }
}

function handleWelcome(data) {
    myPlayerId = data.playerId;
    myRoomCode = data.roomCode;
    isHost = data.isHost;

    lobbyInfo.classList.remove("hidden");
    displayRoomCode.textContent = myRoomCode;

    inputName.disabled = true;
    inputRoom.disabled = true;
    btnJoin.disabled = true;
    btnJoin.textContent = "✓ Katıldın";

    // Avatar'ı sunucuya da bildir
    sendMessage({ type: "set_avatar", avatar: myAvatar });

    // URL'yi güncelle ki paylaşılan link doğru oda kodunu içersin
    try {
        const url = new URL(window.location.href);
        url.searchParams.set("room", myRoomCode);
        window.history.replaceState({}, "", url.toString());
    } catch (e) {}

    updateHostUI();
    sounds.join();
}

function handleLobbyUpdate(data) {
    playerList.innerHTML = "";
    data.players.forEach((p) => {
        const li = document.createElement("li");

        const av = document.createElement("span");
        av.className = "player-list-avatar";
        av.textContent = p.avatar || "🎭";
        li.appendChild(av);

        const nm = document.createElement("span");
        nm.textContent = p.name;
        li.appendChild(nm);

        if (p.id === data.hostId) {
            const badge = document.createElement("span");
            badge.className = "host-badge";
            badge.textContent = "👑 Host";
            li.appendChild(badge);
        }
        if (p.id === myPlayerId) {
            li.style.fontWeight = "bold";
        }
        playerList.appendChild(li);
    });
}

function handleGameStarted(data) {
    currentPlayers = data.players;
    turnPlayerId = data.turnPlayerId;
    timerRemaining = data.timerRemaining || 0;
    timerTotal = data.timerTotal || 0;
    qaLog = [];
    logPanelSeenCount = 0;

    showScreen(screenGame);
    gameRoomCode.textContent = `Oda: ${myRoomCode}`;
    renderPlayersOnTable(currentPlayers);
    renderTurnBar();
    renderLog();

    inputGuess.value = "";
    guessFeedback.classList.add("hidden");

    updateGuessUIState();

    if (data.categoryItems) {
        const diffKey = (data.difficulty || "hepsi") + (data.poolLimit ? `_n${data.poolLimit}` : "");
        initElimPanel(data.category, diffKey, data.categoryItems);
    }
}

function handleGuessResult(data) {
    guessFeedback.classList.remove("hidden", "correct", "wrong");
    const stats = data.correct ? formatRevealStats(data) : "";
    guessFeedback.textContent = data.message + (stats ? "  " + stats : "");

    if (data.correct) {
        guessFeedback.classList.add("correct");
        sounds.correct();
    } else {
        guessFeedback.classList.add("wrong");
        inputGuess.value = "";
        sounds.wrong();
    }
    updateGuessUIState();
}

function handlePlayerRevealed(data) {
    const player = currentPlayers.find((p) => p.id === data.playerId);
    if (player) {
        player.revealed = true;
        player.assignedName = data.assignedName;
    }
    renderPlayersOnTable(currentPlayers);
    renderElimList();
    updateGuessUIState();
    if (data.playerId !== myPlayerId) sounds.correct();
}

function handleGameOver(data) {
    showScreen(screenResult);
    renderRankings(data.rankings);
    sounds.gameOver();

    if (isHost) {
        hostControlsResult.classList.remove("hidden");
        waitingNewRound.classList.add("hidden");
    } else {
        hostControlsResult.classList.add("hidden");
        waitingNewRound.classList.remove("hidden");
    }
}

function handleTurnChanged(data) {
    turnPlayerId = data.turnPlayerId;
    timerRemaining = data.timerRemaining || 0;
    timerTotal = data.timerTotal || 0;
    renderTurnBar();
    renderPlayersOnTable(currentPlayers);
    renderElimList();
    updateGuessUIState();
    if (turnPlayerId === myPlayerId) sounds.turn();
}

function handleTimerTick(data) {
    timerRemaining = data.timerRemaining;
    updateTimerDisplay();
    if (timerRemaining > 0 && timerRemaining <= 5) sounds.tick();
}

function handleTimerExpired(data) {
    turnPlayerId = data.turnPlayerId;
    timerRemaining = data.timerRemaining || 0;
    timerTotal = data.timerTotal || 0;
    renderTurnBar();
    renderPlayersOnTable(currentPlayers);
    renderElimList();
    updateGuessUIState();
    sounds.wrong();
}

function handleLogMessage(data) {
    qaLog.push(data.entry);
    renderLog();
    sounds.message();
    if (logPanel.classList.contains("hidden")) {
        const unseen = qaLog.length - logPanelSeenCount;
        if (unseen > 0) {
            logFabBadge.textContent = unseen;
            logFabBadge.classList.remove("hidden");
        }
    } else {
        logPanelSeenCount = qaLog.length;
    }
}

function handleError(data) {
    alert("⚠️ " + data.message);
}


// ══════════════════════════════════════════════════
// UI RENDER FONKSİYONLARI
// ══════════════════════════════════════════════════

function updateHostUI() {
    if (isHost) {
        hostControls.classList.remove("hidden");
        waitingMsg.classList.add("hidden");
    } else {
        hostControls.classList.add("hidden");
        waitingMsg.classList.remove("hidden");
    }
}

function renderPlayersOnTable(players) {
    if (!playersCircle) return;
    playersCircle.innerHTML = "";

    const count = players.length;
    const centerX = 250;
    const centerY = 250;
    const radius = 180;

    players.forEach((player, index) => {
        const angle = (2 * Math.PI * index) / count - Math.PI / 2;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);

        const node = document.createElement("div");
        node.className = "player-node";
        if (player.id === turnPlayerId) node.classList.add("is-turn");
        node.style.left = x + "px";
        node.style.top = y + "px";

        const avatar = document.createElement("div");
        avatar.className = "player-avatar";
        if (player.revealed) avatar.classList.add("revealed");
        avatar.textContent = player.avatar || player.name.charAt(0).toUpperCase();

        const nameTag = document.createElement("div");
        nameTag.className = "player-assigned-name";
        nameTag.textContent = player.assignedName;
        if (player.assignedName === "???") nameTag.classList.add("mystery");
        else if (player.revealed) nameTag.classList.add("revealed");

        const realName = document.createElement("div");
        realName.className = "player-real-name";
        realName.textContent = player.name;

        node.appendChild(nameTag);
        node.appendChild(avatar);
        node.appendChild(realName);
        playersCircle.appendChild(node);
    });
}

function renderTurnBar() {
    if (!turnPlayerId) {
        turnBar.classList.add("hidden");
        return;
    }
    turnBar.classList.remove("hidden");
    const player = currentPlayers.find((p) => p.id === turnPlayerId);
    if (player) {
        turnPlayerName.textContent = `${player.avatar || ""} ${player.name}`;
        turnPlayerName.classList.toggle("is-me", player.id === myPlayerId);
    }
    if (timerTotal > 0) {
        timerPill.classList.remove("hidden");
        updateTimerDisplay();
    } else {
        timerPill.classList.add("hidden");
    }
}

function updateTimerDisplay() {
    const m = Math.floor(timerRemaining / 60);
    const s = timerRemaining % 60;
    timerValue.textContent = `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
    timerPill.classList.toggle("warning", timerRemaining <= 5 && timerRemaining > 0);
}

function renderRankings(rankings) {
    rankingsList.innerHTML = "";
    rankings.forEach((entry) => {
        const item = document.createElement("div");
        item.className = "ranking-item";

        const pos = document.createElement("div");
        pos.className = "ranking-position";
        if (entry.rank) {
            pos.textContent = `#${entry.rank}`;
            if (entry.rank === 1) pos.classList.add("gold");
            else if (entry.rank === 2) pos.classList.add("silver");
            else if (entry.rank === 3) pos.classList.add("bronze");
        } else {
            pos.textContent = "—";
        }

        const details = document.createElement("div");
        details.className = "ranking-details";
        const statsHtml = entry.rank
            ? `<div class="ranking-stats">${escapeHtml(formatRevealStats(entry))}</div>`
            : "";
        details.innerHTML = `
            <div class="name">${escapeHtml(entry.name)}</div>
            <div class="assigned">${escapeHtml(entry.assignedName)}</div>
            ${statsHtml}
        `;

        item.appendChild(pos);
        item.appendChild(details);
        rankingsList.appendChild(item);
    });
}

function escapeHtml(s) {
    return String(s || "").replace(/[&<>"']/g, (c) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[c]));
}

function formatDuration(seconds) {
    const s = Math.max(0, Math.floor(Number(seconds) || 0));
    if (s < 60) return `${s}sn`;
    const m = Math.floor(s / 60);
    const r = s % 60;
    return r === 0 ? `${m}dk` : `${m}dk ${r}sn`;
}

function updateGuessUIState() {
    const me = currentPlayers.find((p) => p.id === myPlayerId);
    const iAmRevealed = !!(me && me.revealed);
    const isMyTurn = turnPlayerId === myPlayerId;

    if (iAmRevealed) {
        inputGuess.disabled = true;
        btnGuess.disabled = true;
        inputGuess.placeholder = "Bildin! Diğer oyuncuları izle.";
    } else if (!isMyTurn) {
        inputGuess.disabled = true;
        btnGuess.disabled = true;
        inputGuess.placeholder = "Sıran değil, bekle...";
    } else {
        inputGuess.disabled = false;
        btnGuess.disabled = false;
        inputGuess.placeholder = "Kafandaki ismi tahmin et...";
        if (document.activeElement !== inputGuess) inputGuess.focus();
    }
}

function formatRevealStats(entry) {
    const parts = [];
    if (entry.rank) parts.push(`${entry.rank}. bilen`);
    if (entry.turnCount) parts.push(`${entry.turnCount}. tur`);
    if (entry.elapsedSeconds != null) parts.push(formatDuration(entry.elapsedSeconds));
    return parts.length ? `(${parts.join(" · ")})` : "";
}


// ══════════════════════════════════════════════════
// Q&A LOG PANELİ
// ══════════════════════════════════════════════════

function renderLog() {
    logList.innerHTML = "";
    if (qaLog.length === 0) {
        const empty = document.createElement("div");
        empty.className = "log-empty";
        empty.textContent = "Henüz mesaj yok. Sorularını yazmaya başla!";
        logList.appendChild(empty);
        return;
    }
    qaLog.forEach((entry) => {
        const row = document.createElement("div");
        row.className = "log-entry";
        row.dataset.kind = entry.kind || "question";

        const av = document.createElement("span");
        av.className = "log-entry-avatar";
        av.textContent = entry.avatar || "🎭";

        const body = document.createElement("div");
        body.className = "log-entry-body";

        const author = document.createElement("div");
        author.className = "log-entry-author";
        author.textContent = entry.playerName + (entry.playerId === myPlayerId ? " (sen)" : "");

        const txt = document.createElement("div");
        txt.className = "log-entry-text";
        if (entry.kind === "guess_correct") {
            const stats = formatRevealStats(entry);
            txt.textContent = `✅ Tahmin etti: "${entry.text}" — Doğru!${stats ? "  " + stats : ""}`;
        } else if (entry.kind === "guess_wrong") {
            txt.textContent = `❌ Tahmin etti: "${entry.text}" — Yanlış`;
        } else {
            txt.textContent = entry.text;
        }

        body.appendChild(author);
        body.appendChild(txt);
        row.appendChild(av);
        row.appendChild(body);
        logList.appendChild(row);
    });
    logList.scrollTop = logList.scrollHeight;
}

function sendLogMessage(text, kind = "question") {
    const trimmed = (text || "").trim();
    if (!trimmed) return;
    sendMessage({ type: "post_message", text: trimmed, kind });
    logInput.value = "";
}


// ══════════════════════════════════════════════════
// ELEME PANELİ (3-state)
// ══════════════════════════════════════════════════

function elimStorageKey(suffix) {
    return `whoami:elim:${myRoomCode || "_"}:${elimCategory || "_"}:${suffix}`;
}

function initElimPanel(category, difficulty, items) {
    elimCategory = `${category}:${difficulty}`;
    elimItems = items.slice();

    const saved = localStorage.getItem(elimStorageKey("state"));
    elimState = saved ? JSON.parse(saved) : {};

    const savedNotes = localStorage.getItem(elimStorageKey("notes"));
    elimNotes.value = savedNotes || "";

    elimSearch.value = "";
    elimSearchTerm = "";
    elimFilter = "all";
    elimTabs.forEach((t) => t.classList.toggle("active", t.dataset.tab === "all"));
    renderElimList();
}

function getItemState(item) {
    return elimState[item] || "active";
}

function cycleElim(item) {
    const current = getItemState(item);
    const next = current === "active" ? "suspect" : current === "suspect" ? "eliminated" : "active";
    if (next === "active") delete elimState[item];
    else elimState[item] = next;
    localStorage.setItem(elimStorageKey("state"), JSON.stringify(elimState));
    renderElimList();
}

function renderElimList() {
    elimList.innerHTML = "";
    const term = elimSearchTerm.toLowerCase();
    const filtered = elimItems.filter((item) => {
        const state = getItemState(item);
        if (elimFilter === "active" && state !== "active") return false;
        if (elimFilter === "suspect" && state !== "suspect") return false;
        if (elimFilter === "eliminated" && state !== "eliminated") return false;
        if (term && !item.toLowerCase().includes(term)) return false;
        return true;
    });

    if (filtered.length === 0) {
        const empty = document.createElement("div");
        empty.className = "elim-empty";
        empty.textContent = elimItems.length === 0
            ? "Liste yok. Oyun başladığında doldurulacak."
            : "Eşleşen öğe yok.";
        elimList.appendChild(empty);
    } else {
        filtered.forEach((item) => {
            const row = document.createElement("div");
            const state = getItemState(item);
            row.className = "elim-item";
            if (state === "suspect") row.classList.add("suspect");
            if (state === "eliminated") row.classList.add("eliminated");

            const mark = document.createElement("span");
            mark.className = "elim-item-mark";

            const text = document.createElement("span");
            text.className = "elim-item-text";
            text.textContent = item;

            const me = currentPlayers.find((p) => p.id === myPlayerId);
            const iAmRevealed = !!(me && me.revealed);
            const isMyTurn = turnPlayerId === myPlayerId;
            const canGuess = !iAmRevealed && isMyTurn;

            const guessBtn = document.createElement("button");
            guessBtn.type = "button";
            guessBtn.className = "elim-item-guess";
            guessBtn.textContent = "Tahmin Et";
            guessBtn.disabled = !canGuess;
            guessBtn.title = canGuess
                ? `"${item}" olarak tahmin gönder`
                : iAmRevealed ? "Zaten bildin" : "Sıran değil";
            guessBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                if (!canGuess) return;
                if (!confirm(`"${item}" olarak tahmin gönderilsin mi?`)) return;
                sendMessage({ type: "guess", guess: item });
            });

            row.appendChild(mark);
            row.appendChild(text);
            row.appendChild(guessBtn);
            row.title = "Tıkla → aday / şüpheli / elenmiş";
            row.addEventListener("click", () => cycleElim(item));
            elimList.appendChild(row);
        });
    }

    let suspectCount = 0, elimCount2 = 0;
    Object.values(elimState).forEach((s) => {
        if (s === "suspect") suspectCount++;
        else if (s === "eliminated") elimCount2++;
    });
    const total = elimItems.length;
    const active = total - suspectCount - elimCount2;
    elimCount.textContent = `${active} aday · ${suspectCount} şüpheli · ${elimCount2} elenmiş / ${total}`;

    if (elimCount2 + suspectCount > 0) {
        elimFabBadge.textContent = elimCount2 + suspectCount;
        elimFabBadge.classList.remove("hidden");
    } else {
        elimFabBadge.classList.add("hidden");
    }
}


// ══════════════════════════════════════════════════
// AVATAR PICKER (lobby)
// ══════════════════════════════════════════════════

function renderAvatarGrid() {
    avatarGrid.innerHTML = "";
    AVATAR_OPTIONS.forEach((emoji) => {
        const cell = document.createElement("button");
        cell.type = "button";
        cell.className = "avatar-cell" + (emoji === myAvatar ? " selected" : "");
        cell.textContent = emoji;
        cell.title = "Avatar olarak seç";
        cell.addEventListener("click", () => {
            myAvatar = emoji;
            localStorage.setItem("whoami:avatar", emoji);
            renderAvatarGrid();
            if (ws && ws.readyState === WebSocket.OPEN) {
                sendMessage({ type: "set_avatar", avatar: emoji });
            }
        });
        avatarGrid.appendChild(cell);
    });
}


// ══════════════════════════════════════════════════
// URL ile oda doldurma
// ══════════════════════════════════════════════════

function prefillFromUrl() {
    try {
        const url = new URL(window.location.href);
        const room = url.searchParams.get("room");
        if (room) inputRoom.value = room.toUpperCase();
    } catch (e) {}
}


// ══════════════════════════════════════════════════
// EVENT LISTENERS
// ══════════════════════════════════════════════════

btnJoin.addEventListener("click", () => {
    const name = inputName.value.trim();
    if (!name) {
        alert("Lütfen adını yaz!");
        inputName.focus();
        return;
    }
    connectWebSocket();
});

inputName.addEventListener("keydown", (e) => { if (e.key === "Enter") btnJoin.click(); });
inputRoom.addEventListener("keydown", (e) => { if (e.key === "Enter") btnJoin.click(); });

btnCopyCode.addEventListener("click", () => {
    navigator.clipboard.writeText(myRoomCode).then(() => {
        btnCopyCode.textContent = "✓";
        setTimeout(() => (btnCopyCode.textContent = "📋"), 1500);
    });
});

btnCopyLink.addEventListener("click", () => {
    try {
        const url = new URL(window.location.href);
        url.searchParams.set("room", myRoomCode);
        navigator.clipboard.writeText(url.toString()).then(() => {
            btnCopyLink.textContent = "✓";
            setTimeout(() => (btnCopyLink.textContent = "🔗"), 1500);
        });
    } catch (e) {
        alert("Link kopyalanamadı.");
    }
});

// Özel kategori seçilince textarea'yı göster
selectCategory.addEventListener("change", () => {
    if (selectCategory.value === "ozel") {
        customCategoryGroup.classList.remove("hidden");
    } else {
        customCategoryGroup.classList.add("hidden");
    }
});

// Özel zorluk (toplam sayı) seçilince sayı input'unu göster
function updatePoolSizeVisibility() {
    if (selectDifficulty.value === "ozel_sayi") {
        poolSizeGroup.classList.remove("hidden");
    } else {
        poolSizeGroup.classList.add("hidden");
    }
}
selectDifficulty.addEventListener("change", updatePoolSizeVisibility);

function buildGameConfig(category) {
    const difficulty = selectDifficulty.value;
    const timerSeconds = parseInt(inputTimer.value || "0", 10) || 0;
    const poolLimit = difficulty === "ozel_sayi"
        ? Math.max(0, parseInt(inputPoolSize.value || "0", 10) || 0)
        : 0;
    let customWords = [];
    if (category === "ozel") {
        customWords = inputCustomWords.value
            .split(/\r?\n/)
            .map((s) => s.trim())
            .filter((s) => s.length > 0);
        if (customWords.length < currentPlayers.length && customWords.length < 2) {
            alert(`Özel kategori için en az 2 kelime girmelisin (şu an ${customWords.length}).`);
            return null;
        }
    }
    if (difficulty === "ozel_sayi") {
        if (poolLimit < currentPlayers.length) {
            alert(`Toplam seçenek sayısı oyuncu sayısından (${currentPlayers.length}) az olamaz.`);
            return null;
        }
        if (poolLimit < 2) {
            alert("Toplam seçenek sayısı en az 2 olmalı.");
            return null;
        }
    }
    return { category, difficulty, timerSeconds, customWords, poolLimit };
}

btnStart.addEventListener("click", () => {
    const cfg = buildGameConfig(selectCategory.value);
    if (!cfg) return;
    sendMessage({
        type: "start_game",
        category: cfg.category,
        difficulty: cfg.difficulty,
        customWords: cfg.customWords,
        timerSeconds: cfg.timerSeconds,
        poolLimit: cfg.poolLimit,
    });
});

btnGuess.addEventListener("click", () => {
    const guess = inputGuess.value.trim();
    if (!guess) return;
    sendMessage({ type: "guess", guess });
});
inputGuess.addEventListener("keydown", (e) => { if (e.key === "Enter") btnGuess.click(); });

btnNewRound.addEventListener("click", () => {
    const cfg = buildGameConfig(selectCategoryResult.value);
    if (!cfg) return;
    sendMessage({
        type: "new_round",
        category: cfg.category,
        difficulty: cfg.difficulty,
        customWords: cfg.customWords,
        timerSeconds: cfg.timerSeconds,
        poolLimit: cfg.poolLimit,
    });
});

// Pas
btnPass.addEventListener("click", () => {
    sendMessage({ type: "next_turn" });
});

// Boşluk = Pas (oyun ekranı açıkken, input/textarea'da değilse)
document.addEventListener("keydown", (e) => {
    if (e.key !== " " && e.code !== "Space") return;
    if (!screenGame.classList.contains("active")) return;
    const t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    e.preventDefault();
    sendMessage({ type: "next_turn" });
});

// Q&A log
btnLogToggle.addEventListener("click", () => {
    const wasHidden = logPanel.classList.contains("hidden");
    logPanel.classList.toggle("hidden");
    if (wasHidden) {
        logPanelSeenCount = qaLog.length;
        logFabBadge.classList.add("hidden");
        logList.scrollTop = logList.scrollHeight;
        setTimeout(() => logInput.focus(), 100);
    }
});
btnLogClose.addEventListener("click", () => logPanel.classList.add("hidden"));
btnLogSend.addEventListener("click", () => sendLogMessage(logInput.value, "question"));
logInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendLogMessage(logInput.value, "question");
});
logQuickBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        const kind = btn.dataset.kind;
        const labels = { yes: "Evet", no: "Hayır", maybe: "Belki" };
        sendLogMessage(labels[kind] || "?", kind);
    });
});

// Eleme paneli kontrolleri
elimFab.addEventListener("click", () => elimPanel.classList.toggle("hidden"));
elimClose.addEventListener("click", () => elimPanel.classList.add("hidden"));
elimSearch.addEventListener("input", (e) => {
    elimSearchTerm = e.target.value;
    renderElimList();
});
elimTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
        elimTabs.forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        elimFilter = tab.dataset.tab;
        renderElimList();
    });
});
elimReset.addEventListener("click", () => {
    const total = Object.keys(elimState).length;
    if (total === 0) return;
    if (!confirm(`${total} işaretlenmiş öğeyi sıfırlamak istiyor musun?`)) return;
    elimState = {};
    localStorage.removeItem(elimStorageKey("state"));
    renderElimList();
});
elimNotes.addEventListener("input", () => {
    localStorage.setItem(elimStorageKey("notes"), elimNotes.value);
});


// ══════════════════════════════════════════════════
// SES TOGGLE
// ══════════════════════════════════════════════════
function updateSoundIcon() {
    if (soundEnabled) {
        soundIconOn.classList.remove("hidden");
        soundIconOff.classList.add("hidden");
    } else {
        soundIconOn.classList.add("hidden");
        soundIconOff.classList.remove("hidden");
    }
}
btnSoundToggle.addEventListener("click", () => {
    soundEnabled = !soundEnabled;
    localStorage.setItem("whoami:sound", soundEnabled ? "on" : "off");
    updateSoundIcon();
    if (soundEnabled) sounds.message();
});


// ══════════════════════════════════════════════════
// THEME TOGGLE
// ══════════════════════════════════════════════════
document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");
    const sunIcon = document.getElementById("sun-icon");
    const moonIcon = document.getElementById("moon-icon");
    const body = document.body;

    function applyTheme(theme) {
        if (theme === "dark") {
            body.classList.add("dark-mode");
            sunIcon.classList.remove("hidden");
            moonIcon.classList.add("hidden");
        } else {
            body.classList.remove("dark-mode");
            sunIcon.classList.add("hidden");
            moonIcon.classList.remove("hidden");
        }
    }
    const savedTheme = localStorage.getItem("theme") || "light";
    applyTheme(savedTheme);
    themeToggle.addEventListener("click", () => {
        const isDark = body.classList.contains("dark-mode");
        const newTheme = isDark ? "light" : "dark";
        applyTheme(newTheme);
        localStorage.setItem("theme", newTheme);
    });

    // İlk yüklemede UI hazırlıkları
    renderAvatarGrid();
    prefillFromUrl();
    updateSoundIcon();
    updatePoolSizeVisibility();

    // PWA service worker registrasyonu
    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register("sw.js").catch(() => {});
    }
});
