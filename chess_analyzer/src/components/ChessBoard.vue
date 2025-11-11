<template>
    <div>
        <TheChessboard
            :fen="currentFen"
            :board-config="boardConfig"
            class="my-chessboard-container"
            @board-created="(api) => (boardAPI = api)"
        />

        <div>
            <h2>Game Controls</h2>
            <div>
                <button @click="prevMove" :disabled="moveIndex <= -1">
                    Previous
                </button>
                <button
                    @click="nextMove"
                    :disabled="moveIndex >= gameHistory.length - 1"
                >
                    Next
                </button>
                <button @click="flipBoard">Flip Board</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from "vue";
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

const boardConfig = {
    viewOnly: true,
    coordinates: true,
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
        gameHistory.value = game.history({ verbose: true });
        game.reset();
        moveIndex.value = -1;
        currentFen.value = game.fen();
        orientation.value = "white";
        boardAPI.value?.setPosition(currentFen.value);
    },
    { immediate: true },
);

const nextMove = () => {
    if (moveIndex.value < gameHistory.value.length - 1) {
        moveIndex.value++;
        const move = gameHistory.value[moveIndex.value];
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
.my-chessboard-container {
    /* Override the default CSS variables for the chessboard */
    --vc-light-color: #000000; /* Example: Cream color for light squares */
    --vc-dark-color: #b58863; /* Example: Brown color for dark squares */
}
</style>
