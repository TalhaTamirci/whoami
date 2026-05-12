/**
 * Ben Kimim? — Client WebSocket + UI Mantığı
 */

// ── Ayarlar ─────────────────────────────────────────
const WS_URL = "wss://whoami-kaa7.onrender.com";

// ── State ───────────────────────────────────────────
let ws = null;
let myPlayerId = null;
let myRoomCode = null;
let isHost = false;
let currentPlayers = []; // oyun ekranındaki oyuncu listesi

// ── DOM Referansları ────────────────────────────────
const $ = (id) => document.getElementById(id);

// Ekranlar
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
const playerList = $("player-list");
const hostControls = $("host-controls");
const btnStart = $("btn-start");
const selectCategory = $("select-category");
const waitingMsg = $("waiting-msg");
const connectionStatus = $("connection-status");

// Oyun
const gameRoomCode = $("game-room-code");
const playersCircle = $("players-circle");
const inputGuess = $("input-guess");
const btnGuess = $("btn-guess");
const guessFeedback = $("guess-feedback");

// Sonuç
const rankingsList = $("rankings-list");
const hostControlsResult = $("host-controls-result");
const btnNewRound = $("btn-new-round");
const selectCategoryResult = $("select-category-result");
const waitingNewRound = $("waiting-new-round");


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
// WEBSOCKET BAĞLANTISI
// ══════════════════════════════════════════════════

function connectWebSocket() {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        console.log("[WS] Bağlandı");
        connectionStatus.textContent = "● Bağlandı";
        connectionStatus.className = "status-connected";

        // Join mesajı gönder
        ws.send(JSON.stringify({
            type: "join",
            playerName: inputName.value.trim(),
            roomCode: inputRoom.value.trim().toUpperCase(),
        }));
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("[WS] ←", data);
        handleMessage(data);
    };

    ws.onclose = () => {
        console.log("[WS] Bağlantı kapandı");
        connectionStatus.textContent = "● Bağlantı kesildi";
        connectionStatus.className = "status-disconnected";
    };

    ws.onerror = (err) => {
        console.error("[WS] Hata:", err);
        connectionStatus.textContent = "● Bağlantı hatası";
        connectionStatus.className = "status-disconnected";
    };
}

function sendMessage(data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
        console.log("[WS] →", data);
    }
}


// ══════════════════════════════════════════════════
// EVENT HANDLER — Sunucudan gelen mesajları işle
// ══════════════════════════════════════════════════

function handleMessage(data) {
    switch (data.type) {
        case "welcome":
            handleWelcome(data);
            break;
        case "lobby_update":
            handleLobbyUpdate(data);
            break;
        case "game_started":
            handleGameStarted(data);
            break;
        case "guess_result":
            handleGuessResult(data);
            break;
        case "player_revealed":
            handlePlayerRevealed(data);
            break;
        case "game_over":
            handleGameOver(data);
            break;
        case "error":
            handleError(data);
            break;
        default:
            console.warn("[WS] Bilinmeyen event:", data.type);
    }
}

function handleWelcome(data) {
    myPlayerId = data.playerId;
    myRoomCode = data.roomCode;
    isHost = data.isHost;

    // Lobby bilgisini göster
    lobbyInfo.classList.remove("hidden");
    displayRoomCode.textContent = myRoomCode;

    // Join formunu gizle
    inputName.disabled = true;
    inputRoom.disabled = true;
    btnJoin.disabled = true;
    btnJoin.textContent = "✓ Katıldın";

    // Host ise başlat butonunu göster
    updateHostUI();
}

function handleLobbyUpdate(data) {
    playerList.innerHTML = "";
    data.players.forEach((p) => {
        const li = document.createElement("li");
        li.textContent = p.name;
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
    showScreen(screenGame);
    gameRoomCode.textContent = `Oda: ${myRoomCode}`;
    renderPlayersOnTable(currentPlayers);

    // Tahmin alanını sıfırla
    inputGuess.value = "";
    guessFeedback.classList.add("hidden");

    // Eğer zaten açılmışsam tahmin kutusunu devre dışı bırak
    const me = currentPlayers.find((p) => p.id === myPlayerId);
    if (me && me.revealed) {
        inputGuess.disabled = true;
        btnGuess.disabled = true;
    } else {
        inputGuess.disabled = false;
        btnGuess.disabled = false;
        inputGuess.focus();
    }
}

function handleGuessResult(data) {
    guessFeedback.classList.remove("hidden", "correct", "wrong");
    guessFeedback.textContent = data.message;

    if (data.correct) {
        guessFeedback.classList.add("correct");
        inputGuess.disabled = true;
        btnGuess.disabled = true;
    } else {
        guessFeedback.classList.add("wrong");
        inputGuess.value = "";
        inputGuess.focus();
    }
}

function handlePlayerRevealed(data) {
    // currentPlayers'ı güncelle
    const player = currentPlayers.find((p) => p.id === data.playerId);
    if (player) {
        player.revealed = true;
        player.assignedName = data.assignedName;
    }
    renderPlayersOnTable(currentPlayers);
}

function handleGameOver(data) {
    showScreen(screenResult);
    renderRankings(data.rankings);

    if (isHost) {
        hostControlsResult.classList.remove("hidden");
        waitingNewRound.classList.add("hidden");
    } else {
        hostControlsResult.classList.add("hidden");
        waitingNewRound.classList.remove("hidden");
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

/**
 * Oyuncuları masa etrafında daire şeklinde yerleştir.
 */
function renderPlayersOnTable(players) {
    const playersCircle = document.getElementById("players-circle");
    if (!playersCircle) return;
    playersCircle.innerHTML = "";

    const count = players.length;
    const centerX = 250; // game-table-area genişlik/2
    const centerY = 250;
    const radius = 180;

    players.forEach((player, index) => {
        const angle = (2 * Math.PI * index) / count - Math.PI / 2; // üstten başla
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);

        const node = document.createElement("div");
        node.className = "player-node";
        node.style.left = x + "px";
        node.style.top = y + "px";

        const isMe = player.id === myPlayerId;

        // Avatar
        const avatar = document.createElement("div");
        avatar.className = "player-avatar";
        if (player.revealed) avatar.classList.add("revealed");
        
        // placeholder: avatar görseli yerine ilk harf
        avatar.textContent = player.name.charAt(0).toUpperCase();

        // Kafasındaki isim etiketi
        const nameTag = document.createElement("div");
        nameTag.className = "player-assigned-name";
        nameTag.textContent = player.assignedName;

        if (player.assignedName === "???") {
            nameTag.classList.add("mystery");
        } else if (player.revealed) {
            nameTag.classList.add("revealed");
        }

        // Gerçek isim (küçük yazı)
        const realName = document.createElement("div");
        realName.className = "player-real-name";
        realName.textContent = player.name;

        node.appendChild(nameTag);
        node.appendChild(avatar);
        node.appendChild(realName);

        playersCircle.appendChild(node);
    });
}

/**
 * Sonuç ekranında sıralama listesini render et.
 */
function renderRankings(rankings) {
    rankingsList.innerHTML = "";

    rankings.forEach((entry, index) => {
        const item = document.createElement("div");
        item.className = "ranking-item";

        // Sıra numarası
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

        // Detaylar
        const details = document.createElement("div");
        details.className = "ranking-details";
        details.innerHTML = `
            <div class="name">${entry.name}</div>
            <div class="assigned">${entry.assignedName}</div>
        `;

        item.appendChild(pos);
        item.appendChild(details);
        rankingsList.appendChild(item);
    });
}


// ══════════════════════════════════════════════════
// EVENT LISTENERS
// ══════════════════════════════════════════════════

// Odaya katıl
btnJoin.addEventListener("click", () => {
    const name = inputName.value.trim();
    if (!name) {
        alert("Lütfen adını yaz!");
        inputName.focus();
        return;
    }
    connectWebSocket();
});

// Enter ile katıl
inputName.addEventListener("keydown", (e) => {
    if (e.key === "Enter") btnJoin.click();
});
inputRoom.addEventListener("keydown", (e) => {
    if (e.key === "Enter") btnJoin.click();
});

// Oda kodunu kopyala
btnCopyCode.addEventListener("click", () => {
    navigator.clipboard.writeText(myRoomCode).then(() => {
        btnCopyCode.textContent = "✓";
        setTimeout(() => (btnCopyCode.textContent = "📋"), 1500);
    });
});

// Oyunu başlat
btnStart.addEventListener("click", () => {
    const category = selectCategory.value;
    sendMessage({ type: "start_game", category });
});

// Tahmin gönder
btnGuess.addEventListener("click", () => {
    const guess = inputGuess.value.trim();
    if (!guess) return;
    sendMessage({ type: "guess", guess });
});

// Enter ile tahmin
inputGuess.addEventListener("keydown", (e) => {
    if (e.key === "Enter") btnGuess.click();
});

// Yeni tur
btnNewRound.addEventListener("click", () => {
    const category = selectCategoryResult.value;
    sendMessage({ type: "new_round", category });
});
