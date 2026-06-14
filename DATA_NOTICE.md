# 数据使用说明

本仓库不分发比赛原始数据、官方测试集、由原始数据转换出的 JSONL 文件或最终提交文件。

原因：

- CCL2025 细粒度中文仇恨言论识别数据集由任务组织方发布。
- 官方说明中声明数据集所有权归大连理工大学信息检索研究室所有。
- 数据集中包含有害违规内容示例，均不代表本项目作者立场。
- 所有资源仅供科学研究使用，严禁商用。

如需复现实验，请从官方渠道获取数据，并将文件放入：

```text
data/train.json
data/test2.json
```

随后运行：

```bash
python scripts/prepare_data.py --train-json data/train.json --test-json data/test2.json --output-dir output
```
