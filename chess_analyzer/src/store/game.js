import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";

export const useGameStore = defineStore("game", {
  state: () => {
    return {
      pgn: useLocalStorage("pgn", ""),
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
