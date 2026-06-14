# -*- coding: utf-8 -*-
import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Export ms-swift JSONL predictions to Tianchi submission txt.")
    parser.add_argument("--predict-jsonl", type=Path, default=Path("output/predict_result.jsonl"))
    parser.add_argument("--output-txt", type=Path, default=Path("output/predict_result.txt"))
    parser.add_argument("--response-key", default="response")
    args = parser.parse_args()

    args.output_txt.parent.mkdir(parents=True, exist_ok=True)
    with args.predict_jsonl.open("r", encoding="utf-8") as source, args.output_txt.open("w", encoding="utf-8") as target:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            item = json.loads(line)
            if args.response_key not in item:
                raise KeyError(f"line {line_number} does not contain key {args.response_key!r}")
            target.write(str(item[args.response_key]).strip() + "\n")

    print(f"wrote submission file to {args.output_txt}")


if __name__ == "__main__":
    main()
