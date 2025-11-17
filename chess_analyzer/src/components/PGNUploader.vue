<template>
    <div class="container-fluid container-md border p-4 p-md-5 rounded">
        <h1 class="h3 h-md-1 text-center">Analyze Game</h1>

        <form class="mt-4">
            <div class="form-group mb-4">
                <label for="pgn_string" class="fw-bold"
                    >Paste your PGN String Here:</label
                >
                <textarea
                    v-model="PGNString"
                    id="pgn_string"
                    rows="8"
                    class="form-control mt-2"
                ></textarea>
            </div>

            <div
                class="form-group d-flex flex-column flex-md-row align-items-start align-items-md-center gap-3 mb-4"
            >
                <small class="fw-bold">Or Upload a .PGN</small>
                <input
                    type="file"
                    class="form-control w-100 w-md-auto"
                    @change="loadPGNFile"
                />
            </div>

            <div class="d-flex justify-content-center mt-4">
                <button
                    @click="analyze"
                    type="submit"
                    class="btn btn-primary w-100 w-md-auto"
                    :disabled="PGNEmpty"
                >
                    <i class="fa-regular fa-chess-knight"></i> Analyze Game
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useGameStore } from "../store/game.js";

const PGNString = ref("");
const PGNEmpty = computed(() => PGNString.value.trim() === "");

const router = useRouter();
const store = useGameStore();

function loadPGNFile(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (evt) => {
        PGNString.value = evt.target.result || "";
    };
    reader.readAsText(file);
}

function analyze(e) {
    e.preventDefault();
    if (!PGNString.value.trim()) {
        return alert("Please paste a PGN string!");
    }
    store.setPGN(PGNString.value);
    router.push({ name: "analysis" });
}
</script>
