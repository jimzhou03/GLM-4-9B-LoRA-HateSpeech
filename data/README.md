# 数据目录

请从 CCL2025 / 天池官方渠道获取数据，并放入本目录：

```text
data/train.json
data/test1.json
data/test2.json
```

本仓库不提交上述文件，以避免二次公开分发比赛数据。获取数据后运行：

```bash
python scripts/prepare_data.py --train-json data/train.json --test-json data/test2.json --output-dir output
```

生成文件：

```text
output/sft_data.jsonl
output/test_data.jsonl
```
