from pydantic import BaseModel, Field


class MoveAnalyze(BaseModel):
    moveIndex: int = Field(description="Current move count")
    fen: str = Field(description="The FEN of the current board position to be analyzed")
    orientation: str = Field(
        description="Which player side to analyze from [white|black]"
    )
    move: str = Field(description="SAN Move played by the player in this position")


class PerMoveScores(BaseModel):
    pgn: str = Field(description="PGN file to be analyzed")


class GetPositionScore(BaseModel):
    fen: str = Field(description="FEN string for current position")
