"""
Lab 6 CineSense – Prompt Evaluation Skeleton

This is a scaffold, not a complete starter kit.
Students should complete the TODO sections based on the LLM/API they choose.

The script supports three prompt versions:
- v1: baseline prompt
- v2: improved prompt
- v3_cot: CoT-inspired prompt
"""

import csv
import json
from pathlib import Path

DATA_PATH = Path("data/imdb_sample_50.csv")

PROMPT_PATHS = {
    "v1": Path("prompts/prompt_template_v1.txt"),
    "v2": Path("prompts/prompt_template_v2.txt"),
    "v3_cot": Path("prompts/prompt_template_v3_cot.txt"),
}

OUTPUT_DIR = Path("outputs")


def call_llm(prompt: str) -> str:
    """
    TODO:
    Replace this function with your LLM call.

    Options:
    - Gemini API
    - Groq API
    - OpenRouter
    - Ollama local API
    - Manual web UI copy/paste, then skip this script

    Return:
        Raw text output from the LLM.
    """
    raise NotImplementedError("Students should implement the LLM call.")


def parse_json_safely(raw_text: str):
    """
    Try to parse LLM output as JSON.

    Returns:
        parsed_object: dict
        valid_json: 1 if parsing succeeds, else 0
    """
    try:
        return json.loads(raw_text), 1
    except json.JSONDecodeError:
        return {}, 0


def extract_pred_sentiment(parsed_output: dict) -> str:
    """
    Extract predicted sentiment from parsed JSON output.
    """
    sentiment = parsed_output.get("sentiment", "")
    if isinstance(sentiment, str):
        sentiment = sentiment.strip().lower()
    return sentiment if sentiment in {"positive", "negative"} else ""


def run_one_prompt(prompt_version: str, prompt_path: Path, rows: list[dict]):
    """
    Run one prompt template on all rows.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"result_{prompt_version}.csv"

    prompt_template = prompt_path.read_text(encoding="utf-8")
    outputs = []

    for row in rows:
        prompt = prompt_template.replace("{review_text}", row["review_text"])

        # TODO: call your LLM here.
        # llm_output = call_llm(prompt)

        # Temporary placeholder for students who use manual web UI.
        llm_output = "TODO: paste or generate LLM output here"

        parsed_output, valid_json = parse_json_safely(llm_output)
        pred_sentiment = extract_pred_sentiment(parsed_output)

        outputs.append({
            "review_id": row["review_id"],
            "review_text": row["review_text"],
            "gold_sentiment": row["gold_sentiment"],
            "prompt_version": prompt_version,
            "llm_output": llm_output,
            "valid_json": valid_json,
            "pred_sentiment": pred_sentiment,
        })

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "review_id",
                "review_text",
                "gold_sentiment",
                "prompt_version",
                "llm_output",
                "valid_json",
                "pred_sentiment",
            ],
        )
        writer.writeheader()
        writer.writerows(outputs)

    print(f"Saved outputs to {output_path}")


def main():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for prompt_version, prompt_path in PROMPT_PATHS.items():
        if not prompt_path.exists():
            print(f"Skip {prompt_version}: {prompt_path} not found")
            continue
        run_one_prompt(prompt_version, prompt_path, rows)


if __name__ == "__main__":
    main()
