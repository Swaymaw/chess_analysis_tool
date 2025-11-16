<template>
    <div style="width: 90%">
        <div class="player-info">
            <span class="player-name">{{ topPlayerName }}</span>
            <span :class="topPlayerClockClass">{{ topPlayerClock }}</span>
        </div>
        <TheChessboard
            :fen="currentFen"
            :board-config="boardConfig"
            class="my-board"
            style="width: 90%"
            @board-created="(api) => (boardAPI = api)"
        />
        <div class="player-info">
            <span class="player-name">{{ bottomPlayerName }}</span>
            <span :class="bottomPlayerClockClass">{{ bottomPlayerClock }}</span>
        </div>

        <div class="game-controls">
            <h2>Game Controls</h2>
            <div class="button-group">
                <button
                    @click="prevMove"
                    :disabled="moveIndex <= -1"
                    class="btn btn-primary me-2"
                >
                    <i class="fa-solid fa-arrow-left"></i> Previous
                </button>
                <button
                    @click="nextMove"
                    :disabled="moveIndex >= gameHistory.length - 1"
                    class="btn btn-primary me-2"
                >
                    Next <i class="fa-solid fa-arrow-right"></i>
                </button>
                <button @click="flipBoard" class="btn btn-secondary">
                    <i class="fa-solid fa-repeat"></i> Flip Board
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, computed } from "vue";
import { TheChessboard } from "vue3-chessboard";
import "vue3-chessboard/style.css";
import { Chess } from "chess.js";

const props = defineProps({
    pgn: { type: String, required: true },
});

const emit = defineEmits(["move-change"]);

const game = new Chess();
const boardAPI = ref();
const currentFen = ref("");
const gameHistory = ref([]);
const moveIndex = ref(-1);
const orientation = ref("white");
const whiteName = ref("White");
const blackName = ref("Black");
const moveTimes = ref([]);
const whiteTime = ref(null);
const blackTime = ref(null);

const boardConfig = {
    viewOnly: true,
    coordinates: true,
};

const topPlayerName = computed(() => {
    return orientation.value === "white" ? blackName.value : whiteName.value;
});

const bottomPlayerName = computed(() => {
    return orientation.value === "white" ? whiteName.value : blackName.value;
});

const topPlayerClock = computed(() => {
    if (orientation.value === "white") {
        return blackTime.value || "--:--";
    }
    return whiteTime.value || "--:--";
});

const bottomPlayerClock = computed(() => {
    if (orientation.value === "white") {
        return whiteTime.value || "--:--";
    }
    return blackTime.value || "--:--";
});

const topPlayerClockClass = computed(() => {
    return orientation.value === "white"
        ? "player-clock clock-black"
        : "player-clock clock-white";
});

const bottomPlayerClockClass = computed(() => {
    return orientation.value === "white"
        ? "player-clock clock-white"
        : "player-clock clock-black";
});

const parseClockTime = (comment) => {
    if (!comment) return null;
    const match = comment.match(/\[%clk\s+(\d+):(\d+):(\d+(?:\.\d+)?)\]/);
    if (match) {
        return `${match[1]}:${match[2]}:${Math.floor(parseFloat(match[3]))}`;
    }
    return null;
};

const handleKey = (e) => {
    if (e.key === "ArrowLeft") prevMove();
    if (e.key === "ArrowRight") nextMove();
};

onMounted(() => {
    window.addEventListener("keydown", handleKey);
});
onUnmounted(() => {
    window.removeEventListener("keydown", handleKey);
});

watch(
    () => props.pgn,
    (newPgn) => {
        if (!newPgn) return;
        game.loadPgn(newPgn, { strict: false });

        const headers = game.getHeaders();
        whiteName.value = headers.White || "White";
        blackName.value = headers.Black || "Black";

        gameHistory.value = game.history({ verbose: true });

        moveTimes.value = [];
        const pgnMoves =
            newPgn.match(
                /\d+\.\s*[^\s]+\s*\{[^}]*\}|\d+\.\.\.\s*[^\s]+\s*\{[^}]*\}/g,
            ) || [];

        gameHistory.value.forEach((move, idx) => {
            const moveNum = Math.floor(idx / 2) + 1;
            const isWhite = idx % 2 === 0;
            const moveNotation = isWhite
                ? `${moveNum}. ${move.san}`
                : `${moveNum}... ${move.san}`;

            const pgnMove = pgnMoves.find((m) => m.includes(move.san));
            const time = pgnMove ? parseClockTime(pgnMove) : null;
            moveTimes.value.push(time);
        });
        game.reset();
        moveIndex.value = -1;
        currentFen.value = game.fen();
        orientation.value = "white";
        whiteTime.value = moveTimes.value[0] || null;
        blackTime.value = moveTimes.value[1] || null;
        boardAPI.value?.setPosition(currentFen.value);
    },
    { immediate: true },
);

const updateClocks = () => {
    if (moveIndex.value === -1) {
        whiteTime.value = moveTimes.value[0] || null;
        blackTime.value = moveTimes.value[1] || null;
    } else if (moveIndex.value === 0) {
        whiteTime.value = moveTimes.value[0] || null;
        blackTime.value = moveTimes.value[1] || null;
    } else {
        const currentMove = gameHistory.value[moveIndex.value];
        const isWhiteMove = currentMove.color === "w";

        if (isWhiteMove) {
            whiteTime.value =
                moveTimes.value[moveIndex.value] || whiteTime.value;
        } else {
            blackTime.value =
                moveTimes.value[moveIndex.value] || blackTime.value;
        }
    }
};
const nextMove = () => {
    if (moveIndex.value < gameHistory.value.length - 1) {
        moveIndex.value++;
        const move = gameHistory.value[moveIndex.value];
        updateClocks();
        emit("move-change", {
            moveIndex: moveIndex.value,
            move: move.san,
            fen: currentFen.value,
            orientation: orientation.value,
        });
        game.move(move.san);
        currentFen.value = game.fen();
        boardAPI.value?.move(move.san);
    }
};

const prevMove = () => {
    if (moveIndex.value > -1) {
        game.undo();
        moveIndex.value--;
        const move = gameHistory.value[moveIndex.value];
        currentFen.value = game.fen();
        let prevFen = game.fen();
        if (moveIndex.value > -1) {
            game.undo();
            prevFen = game.fen();
            game.move(move.san);
        }
        boardAPI.value?.undoLastMove();
        updateClocks();

        emit("move-change", {
            moveIndex: moveIndex.value,
            move: move?.san,
            fen: prevFen,
            orientation: orientation.value,
        });
    }
};

function flipBoard() {
    boardAPI.value?.toggleOrientation();
    orientation.value = orientation.value === "white" ? "black" : "white";
    game.undo();

    if (moveIndex.value > -1) {
        const curMove = gameHistory.value[moveIndex.value];
        const prevFen = game.fen();

        game.move(curMove.san);

        emit("move-change", {
            moveIndex: moveIndex.value,
            move: curMove.san,
            fen: prevFen,
            orientation: orientation.value,
        });
    }
}
</script>

<style scoped>
.player-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: #f0f0f0;
    border-radius: 4px;
    margin: 8px 0;
}

.player-name {
    font-weight: bold;
    font-size: 16px;
}

.player-clock {
    font-family: monospace;
    font-size: 18px;
    font-weight: bold;
    padding: 4px 12px;
    border-radius: 4px;
    border: 2px solid #ddd;
}

.clock-white {
    color: #000;
    background-color: #fff;
    border-color: #999;
}

.clock-black {
    color: #fff;
    background-color: #2c3e50;
    border-color: #1a252f;
}
.game-controls {
    margin-top: 20px;
    padding: 20px;
    background: linear-gradient(135deg, #ebecd0 0%, #739552 100%);
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.game-controls h2 {
    margin: 0 0 15px 0;
    font-size: 20px;
    color: #2c3e50;
    font-weight: 600;
}

.button-group {
    display: flex;
    gap: 0;
    flex-wrap: wrap;
}

.btn {
    font-size: 16px;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn i {
    margin: 0 4px;
}
</style>
