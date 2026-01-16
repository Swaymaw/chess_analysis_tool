<template>
    <div class="container-md py-4">
        <div class="row g-4">
            <div class="col-lg-7">
                <div class="ai-commentary-section">
                    <div v-if="isLoadingEvaluation" class="placeholder-glow">
                        <span class="placeholder col-12 rounded py-3"></span>
                    </div>
                    <div v-else-if="res?.ai_commentary" class="comment-bubble shadow-sm p-3 border-start border-4 border-primary bg-white rounded">
                        <div class="small fw-bold text-primary mb-1">
                            <i class="bi bi-robot"></i> AI INSIGHT
                        </div>
                        <p class="mb-0 fst-italic text-dark">{{ res.ai_commentary }}</p>
                    </div>
                </div>
                <div class="board-wrapper shadow-sm rounded p-2 bg-light text-center">
                    <ChessBoard :pgn="store.pgn" @move-change="onMoveChange" />
                </div>
            </div>
            <div class="col-lg-5">
                <div class="analysis-panel d-flex flex-column gap-3">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title fw-bold text-muted text-uppercase small mb-3">Game Evaluation</h5>
                            <div v-if="isLoadingScores" class="text-center py-4">
                                <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
                                <span class="ms-2 text-muted">Calculating scores...</span>
                            </div>
                            <ScoreChart v-else :scores="scores" :moveIndex="moveIdx" />
                        </div>
                    </div>
                    <div class="card border-0 shadow-sm">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <MoveQuality v-if="moveIdx >= 0" :move_quality="moveQualities[moveIdx]" />
                            </div>

                            <div v-if="scores && scores.length" class="table-responsive">
                                <table class="table table-hover align-middle mb-0">
                                    <thead class="table-light">
                                        <tr class="small">
                                            <th>Metric</th>
                                            <th class="text-center">White</th>
                                            <th class="text-center">Black</th>
                                        </tr>
                                    </thead>
                                    <tbody class="border-top-0">
                                        <tr>
                                            <td class="fw-semibold">Accuracy</td>
                                            <td class="text-center"><span class="badge bg-success bg-opacity-10 text-success p-2 w-75">{{ whiteAcc.toFixed(1) }}%</span></td>
                                            <td class="text-center"><span class="badge bg-success bg-opacity-10 text-success p-2 w-75">{{ blackAcc.toFixed(1) }}%</span></td>
                                        </tr>
                                        <tr v-for="l in labels" :key="l" class="small">
                                            <td class="text-muted">{{ l }}</td>
                                            <td class="text-center fw-bold">{{ counts.white[l.toLowerCase()] }}</td>
                                            <td class="text-center fw-bold">{{ counts.black[l.toLowerCase()] }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <EngineLine
                        :isLoading="isLoadingEvaluation"
                        :data="res"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.container-md {
    max-width: 1100px;
}
.comment-bubble {
    position: relative;
    font-size: 1.05rem;
    line-height: 1.5;
}
.comment-bubble::after {
    content: '';
    position: absolute;
    left: 20px;
    bottom: -10px;
    border-width: 10px 10px 0;
    border-style: solid;
    border-color: #fff transparent transparent;
}
.card {
    transition: transform 0.2s ease;
}
.engine-text {
    line-height: 1.6;
    letter-spacing: 0.5px;
    color: #00ff88; /* Matrix/Terminal green feel for engine */
}
</style>

<script setup>
import { ref, onMounted, computed } from "vue";
import { debounceAsync } from "../utils/helper.js";
import { useGameStore } from "../store/game.js";
import ChessBoard from "../components/ChessBoard.vue";
import ScoreChart from "../components/ScoreChart.vue";
import MoveQuality from "../components/MoveQuality.vue";
import EngineLine from '../components/EngineLine.vue'
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
