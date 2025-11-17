import axios from "axios";

class Api {
  constructor(baseURL) {
    this.client = axios.create({
      baseURL,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  async analyzePosition({ fen, orientation, move, moveIndex }) {
    if (!fen) throw new Error("FEN is required");

    const { data } = await this.client.get("/api/v1/analysis/move_analyze", {
      params: {
        fen: fen,
        orientation: orientation,
        move: move,
        moveIndex: moveIndex,
      },
    });

    return data;
  }

  async getPerMoveScores(pgn) {
    if (!pgn) throw new Error("PGN is required");

    const { data } = await this.client.get("/api/v1/analysis/per_move_score", {
      params: {
        pgn: pgn,
      },
    });

    return data;
  }
}

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const api = new Api(baseURL);

export default api;
