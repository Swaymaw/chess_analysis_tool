<template>
    <div class="container border p-5 rounded">
        <h1>Analyze Game</h1>
        <br />
        <form>
            <div class="form-group">
                <label for="pgn_string">Paste your PGN String Here:</label>
                <textarea
                    v-model="PGNString"
                    id="pgn_string"
                    rows="10"
                    class="form-control"
                ></textarea>
            </div>

            <div class="mt-5 d-flex align-items-center form-group">
                <small class="me-3 fw-bolder">Or Upload a .PGN file</small>
                <input type="file" class="border p-2" @change="loadPGNFile" />
            </div>

            <div class="d-flex justify-content-center mt-5">
                <button
                    @click="analyze"
                    type="submit"
                    class="btn btn-primary"
                    :disabled="PGNEmpty"
                >
                    <i class="fa-regular fa-chess-knight" /> Analyze Game
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
