import os
from ..utils.helper import get_ai_client
from google.genai import types
from async_lru import alru_cache


@alru_cache(maxsize=1024)
async def get_move_commentary(
    move: str, best_move: str, score: float, best_score: float, fen: str
):
    eval_diff = abs(best_score - score)

    # STRUCTURE: Put the static "instruction" first to maximize Implicit Cache hits.
    # Note: Gemini 2.0 Flash requires a minimum of 1024 tokens for implicit caching.
    # For smaller requests, the 'alru_cache' is your primary speed booster.
    prompt = (
        "Expert Chess Commentator Instruction: Provide a single-line, punchy commentary. "
        "Be witty for blunders, instructive for mistakes. Exactly one sentence.\n\n"
        f"Position: {fen}\n"
        f"Move Played: {move} (Eval: {score})\n"
        f"Engine Best: {best_move} (Eval: {best_score})\n"
        f"Loss: {eval_diff}"
    )

    client = get_ai_client()

    try:
        # Use client.aio for async calls in FastAPI
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=100,
            ),
        )
        return response.text.strip()
    except Exception as e:
        print(f"GenAI Error: {e}")
        return "Analysis currently unavailable."
