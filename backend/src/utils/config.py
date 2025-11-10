ENGINE_PATHS: dict[str, str] = {
    "stockfish": "Engines/stockfish/stockfish-macos-m1-apple-silicon",
    "lc0": "Engines/lc0/lc0-v0.32.0-macos_12.6.1",
}

WEIGHTS_FILE: dict[str, str] = {"maia-2200": "Engines/lc0/maia-2200.pb.gz"}

MATE_SCORE: int = 100000
