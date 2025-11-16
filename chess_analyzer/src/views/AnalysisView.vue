<template>
    <div class="container-md">
        <div class="row">
            <div class="col">
                <ChessBoard :pgn="store.pgn" @move-change="onMoveChange" />
            </div>
            <div class="col">
                <div class="border p-4 rounded mt-4">
                    <h3>Game Score</h3>
                    <pre v-if="isLoadingScores">Getting Scores...</pre>
                    <ScoreChart
                        v-if="scores != []"
                        :scores="scores"
                        :moveIndex="moveIdx"
                    />
                    <MoveQuality
                        class="mt-5"
                        v-if="res?.move_quality && !isLoadingEvaluation"
                        :move_quality="res.move_quality"
                    />
                </div>
                <pre v-if="isLoadingEvaluation">Analyzing...</pre>
                <pre v-else>{{ res?.description || null }}</pre>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { debounceAsync } from "../utils/helper.js";
import { useGameStore } from "../store/game.js";
import ChessBoard from "../components/ChessBoard.vue";
import ScoreChart from "../components/ScoreChart.vue";
import MoveQuality from "../components/MoveQuality.vue";
import api from "../api/api.js";

const isLoadingEvaluation = ref(false);
const isLoadingScores = ref(false);
const res = ref(null);
const scores = ref([]);
const moveIdx = ref(0);

onMounted(() => {
    isLoadingScores.value = true;
    async function getPerMoveScore() {
        const api_res = await api.getPerMoveScores(store.pgn);
        scores.value = api_res?.scores;
        isLoadingScores.value = false;
        console.log(scores.value);
    }
    getPerMoveScore();
});

const store = useGameStore();

const debouncedAnalyze = debounceAsync(async (params) => {
    return await api.analyzePosition(params);
}, 300);

async function onMoveChange({ moveIndex, move, fen, orientation }) {
    console.log("Move Changed:", moveIndex, move, fen, orientation);
    moveIdx.value = moveIndex;
    if (moveIndex < 0) {
        res.value = "";
        return;
    }

    isLoadingEvaluation.value = true;

    try {
        res.value = await debouncedAnalyze({
            fen,
            orientation,
            move,
            moveIndex,
        });
    } finally {
        console.log(res.value);
        isLoadingEvaluation.value = false;
    }
}
</script>
