# -*- coding: utf-8 -*-
import argparse
import json
from pathlib import Path


SYSTEM_PROMPT = """本次任务为细粒度片段级中文仇恨言论识别。基于给定的社交媒体文本，输出仇恨四元组，顺序依次为评论对象（Target）、论点（Argument）、目标群体（Targeted Group）、是否仇恨（Hateful）。

评论对象（Target）：帖子的评述对象，如一个人或一个群体。当实例无具体目标时设为 NULL。
论点（Argument）：包含对评论目标关键论点的信息片段。
目标群体（Targeted Group）：包括 Region、Racism、Sexism、LGBTQ、others；非仇恨或不包含特定群体的一般攻击性言论设为 non-hate。
是否仇恨（Hateful）：hate 或 non-hate。

每个四元组中各元素之间用 " | " 分割，并用 [END] 结尾；如果一条样本包含多个四元组，不同四元组之间用 [SEP] 分割。请严格按照顺序和格式输出，不要省略空格。"""


def load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list")
    return data


def write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_train_rows(items: list[dict]) -> list[dict]:
    rows = []
    for item in items:
        rows.append(
            {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": item["content"]},
                    {"role": "assistant", "content": item["output"]},
                ]
            }
        )
    return rows


def build_test_rows(items: list[dict]) -> list[dict]:
    rows = []
    for item in items:
        rows.append(
            {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": item["content"]},
                    {"role": "assistant", "content": "无"},
                ]
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert official CCL2025 JSON files to ms-swift JSONL.")
    parser.add_argument("--train-json", type=Path, default=Path("data/train.json"))
    parser.add_argument("--test-json", type=Path, default=Path("data/test2.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()

    train_data = load_json(args.train_json)
    test_data = load_json(args.test_json)

    write_jsonl(build_train_rows(train_data), args.output_dir / "sft_data.jsonl")
    write_jsonl(build_test_rows(test_data), args.output_dir / "test_data.jsonl")

    print(f"wrote {len(train_data)} train rows to {args.output_dir / 'sft_data.jsonl'}")
    print(f"wrote {len(test_data)} test rows to {args.output_dir / 'test_data.jsonl'}")


if __name__ == "__main__":
    main()
