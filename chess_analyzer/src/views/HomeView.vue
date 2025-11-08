<template>
    <div class="container py-5">
        <h1 class="text-center mb-4">Chess Game Analyzer</h1>
        <PGNUploader @analyze="goToAnalysis" />
    </div>
</template>

<script>
import PGNUploader from "../components/PGNUploader.vue";

export default {
    components: { PGNUploader },
    methods: {
        goToAnalysis({ pgn, side }) {
            this.$router.push({ name: "analysis", state: { pgn, side } });
        },
    },
};
</script>
