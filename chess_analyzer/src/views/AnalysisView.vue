<template>
    <div class="container-fluid p-4">
        <div class="row">
            <div
                class="col-md-6 d-flex justify-content-center align-items-start"
            >
                <ChessBoard :pgn="pgn" :side="side" />
            </div>
            <div class="col-md-6">
                <h3 class="mb-3">Analysis for {{ side }}</h3>
                <p class="text-muted">Here’s your PGN:</p>
                <pre class="bg-light p-3 rounded border">{{ pgn }}</pre>
            </div>
        </div>
    </div>
</template>

<script>
import ChessBoard from "../components/ChessBoard.vue";
export default {
    props: ["pgn", "side"],
    components: { ChessBoard },
};
</script>
