<template>
    <div>
        <div style="display: flex; gap: 20px; align-items: center">
            <TheChessboard
                :fen="currentFen"
                :board-config="boardConfig"
                @board-created="(api) => (boardAPI = api)"
                style="width: 400px; height: 400px"
            />

            <div>
                <h2>Game Controls</h2>
                <div style="margin-bottom: 10px">
                    <button
                        @click="prevMove"
                        :disabled="moveIndex <= -1"
                        style="margin-right: 5px"
                    >
                        Previous
                    </button>
                    <button
                        @click="nextMove"
                        :disabled="moveIndex >= gameHistory.length - 1"
                        style="margin-right: 5px"
                    >
                        Next
                    </button>
                    <button @click="flipBoard">Flip Board</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { TheChessboard } from "vue3-chessboard";
import "vue3-chessboard/style.css";
import { Chess } from "chess.js";
import { useGameStore } from "../store/game.js";

const store = useGameStore();
const pgn = store.pgn;

const game = new Chess();

const boardAPI = ref();
const currentFen = ref("");
const gameHistory = ref([]);
const moveIndex = ref(-1);

const boardConfig = {
    viewOnly: true,
    coordinates: true,
};

onMounted(() => {
    game.loadPgn(pgn, { strict: false });
    gameHistory.value = game.history({ verbose: true });
    game.reset();
    currentFen.value = game.fen();
    boardAPI.value?.setPosition(currentFen.value);
});

const nextMove = () => {
    if (moveIndex.value < gameHistory.value.length - 1) {
        moveIndex.value++;
        const move = gameHistory.value[moveIndex.value];
        game.move(move.san);
        currentFen.value = game.fen();
        boardAPI.value?.move(move.san);
    }
};

const prevMove = () => {
    if (moveIndex.value > -1) {
        game.undo();
        currentFen.value = game.fen();
        moveIndex.value--;
        boardAPI.value?.undoLastMove();
    }
};

function flipBoard() {
    boardAPI.value?.toggleOrientation();
}
</script>
