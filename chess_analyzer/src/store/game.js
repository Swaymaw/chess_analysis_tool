import { defineStore } from "pinia";

export const useGameStore = defineStore("game", {
  state: () => ({
    pgn: "",
  }),
  actions: {
    setPGN(value) {
      this.pgn = value;
    },
    clearPGN() {
      this.pgn = "";
    },
  },
});
