<template>
    <div class="card shadow-sm p-4 mx-auto" style="max-width: 600px">
        <div class="mb-3">
            <label class="form-label fw-semibold">Paste your PGN:</label>
            <textarea v-model="pgn" rows="6" class="form-control"></textarea>
        </div>

        <div class="mb-3">
            <label class="form-label fw-semibold">Select your side:</label>
            <select v-model="side" class="form-select">
                <option value="white">White</option>
                <option value="black">Black</option>
            </select>
        </div>

        <button class="btn btn-primary w-100 fw-semibold" @click="analyze">
            Analyze
        </button>
    </div>
</template>

<script>
export default {
    data() {
        return { pgn: "", side: "white" };
    },
    methods: {
        analyze() {
            if (!this.pgn.trim()) return alert("Please paste a PGN first!");
            this.$emit("analyze", { pgn: this.pgn, side: this.side });
        },
    },
};
</script>
