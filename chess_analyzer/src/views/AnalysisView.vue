<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <ChessBoard :pgn="store.pgn" @move-change="onMoveChange" />
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
import { debounceAsync } from "../utils/helper.js";
import { useGameStore } from "../store/game.js";
import ChessBoard from "../components/ChessBoard.vue";
import api from "../api/api.js";

const isLoading = ref(false);
const res = ref(null);

const store = useGameStore();

const debouncedAnalyze = debounceAsync(async (params) => {
    return await api.analyzePosition(params);
}, 300);

async function onMoveChange({ moveIndex, move, fen, orientation }) {
    console.log("Move Changed:", moveIndex, move, fen, orientation);
    if (moveIndex < 0) {
        res.value = "";
        return;
    }
    isLoading.value = true;

    try {
        res.value = await debouncedAnalyze({
            fen,
            orientation,
            move,
            moveIndex,
        });
    } finally {
        isLoading.value = false;
    }
}
</script>
