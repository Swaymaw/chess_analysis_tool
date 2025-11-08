<template>
    <div>
        <div id="board" class="border shadow rounded"></div>
    </div>
</template>

<script>
import { Chess } from "chess.js";
import Chessboard from "chessboardjsx";

export default {
    props: ["pgn", "side"],
    data: () => ({ pgn: "", side: "white" }),
    created() {
        const s = this.$route.state ?? window.history.state ?? {};
        this.pgn = s.pgn ?? "";
        this.side = s.side ?? "white";
    },
    mounted() {
        let game = new Chess();
        console.log(this.pgn, this.side);
        try {
            // The fix is to pass an options object with `sloppy: true`
            game.loadPgn(this.pgn, { sloppy: true });
        } catch {
            alert("Invalid PGN!");
        }

        Chessboard("board", {
            position: game.fen(),
            orientation: this.side,
            draggable: false,
        });
    },
};
</script>

<style scoped>
#board {
    width: 480px;
}
</style>
