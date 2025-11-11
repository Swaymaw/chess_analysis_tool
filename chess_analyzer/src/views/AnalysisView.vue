<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <ChessBoard
                    :pgn="store.pgn"
                    @move-change="debouncedOnMoveChange"
                />
            </div>
            <div class="col">
                <pre v-if="isLoading">Analyzing...</pre>
                <pre v-else>{{ res?.description || null }}</pre>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { debounce } from "../utils/helper.js";
import { useGameStore } from "../store/game.js";
import ChessBoard from "../components/ChessBoard.vue";
import api from "../api/api.js";

const isLoading = ref(false);
const res = ref(null);

const store = useGameStore();
async function onMoveChange({ moveIndex, move, fen, orientation }) {
    console.log("Move changed:", moveIndex, move, fen, orientation);
    if (moveIndex < 0) {
        res.value = "";
        return;
    }
    isLoading.value = true;
    try {
        res.value = await api.analyzePosition({
            fen,
            orientation,
            move,
            moveIndex,
        });
    } finally {
        isLoading.value = false;
    }
}

const debouncedOnMoveChange = debounce(onMoveChange, 20);
</script>
