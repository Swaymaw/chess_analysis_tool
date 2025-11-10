import { defineStore } from "pinia";

export const useGameStore = defineStore("game", {
  state: () => {
    return {
      pgn: "",
    };
  },
  actions: {
    setPGN(value) {
      this.pgn = value;
    },
    clearPGN() {
      this.pgn = "";
    },
  },
});
