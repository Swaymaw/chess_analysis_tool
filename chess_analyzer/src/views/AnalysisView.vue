<template>
    <div class="container-md">
        <div class="row">
            <div class="col">
                <ChessBoard :pgn="store.pgn" @move-change="onMoveChange" />
            </div>
            <div class="col">
                <div class="border p-4 rounded mt-4">
                    <h4>Game Score</h4>
                    <pre v-if="isLoadingScores">Getting Scores...</pre>
                    <ScoreChart :scores="scores" :moveIndex="moveIdx" />
                    <h4 class="mt-3">Game Summary</h4>
                    <div v-if="scores && scores.length">
                        <table
                            class="table table-sm table-striped table-bordered table-hover"
                        >
                            <thead class="thead-dark">
                                <tr>
                                    <th>Label</th>
                                    <th>White</th>
                                    <th>Black</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr>
                                    <td>Accuracy</td>
                                    <td>{{ whiteAcc.toFixed(2) }}</td>
                                    <td>{{ blackAcc.toFixed(2) }}</td>
                                </tr>
                                <tr v-for="l in labels" :key="l">
                                    <td>{{ l }}</td>
                                    <td>{{ counts.white[l.toLowerCase()] }}</td>
                                    <td>{{ counts.black[l.toLowerCase()] }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <MoveQuality
                        class="mt-3"
                        v-if="moveIdx >= 0"
                        :move_quality="moveQualities[moveIdx]"
                    />
                </div>
                <pre v-if="isLoadingEvaluation">Analyzing...</pre>
                <pre v-else>{{ res?.description || null }}</pre>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
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
const moveQualities = ref([]);
const moveIdx = ref(-1);
const whiteAcc = ref(0.0);
const blackAcc = ref(0.0);

const labels = [
    "BRILLIANT",
    "BEST",
    "EXCELLENT",
    "GOOD",
    "INACCURACY",
    "MISTAKE",
    "BLUNDER",
];

const counts = computed(() => {
    const white = {};
    const black = {};

    labels.forEach((l) => {
        const key = l.toLowerCase();
        white[key] = 0;
        black[key] = 0;
    });

    moveQualities.value.forEach((quality, idx) => {
        const key = quality.toLowerCase();
        if (idx % 2 === 0) white[key]++;
        else black[key]++;
    });

    return { white, black };
});

onMounted(() => {
    isLoadingScores.value = true;
    async function getPerMoveScore() {
        const api_res = await api.getPerMoveScores(store.pgn);
        scores.value = api_res?.scores;
        moveQualities.value = api_res?.move_qualities;
        whiteAcc.value = api_res?.white_acc ?? 0.0;
        blackAcc.value = api_res?.black_acc ?? 0.0;
        isLoadingScores.value = false;
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
