# GLM-4-9B-LoRA-HateSpeech

基于 GLM-4-9B-0414 与 LoRA 微调的细粒度中文仇恨言论四元组抽取方案。本项目用于 CCL25-Eval Task 10 / 天池「细粒度中文仇恨识别评测」参赛方案复现与技术说明。

## 任务简介

输入为社交媒体评论文本，输出为一个或多个仇恨言论四元组：

```text
Target | Argument | Targeted Group | Hateful [END]
```

多四元组样本使用 `[SEP]` 分隔。示例：

```text
老黑 | 讨厌 | Racism | hate [SEP] 媚黑的 | 倒贴 | Racism | hate [END]
```

## 方法概览

- 基座模型：[GLM-4-9B-0414](https://www.modelscope.cn/models/ZhipuAI/GLM-4-9B-0414)
- 训练方式：LoRA SFT
- 训练框架：ms-swift
- 主要目标：将评论文本生成规范化四元组，兼顾硬匹配与软匹配 F1
- 本地记录最佳公开分数：`0.3566`，对应 `glm-4-9b-0414 v1`

## 仓库内容

```text
.
├── assets/training_curves/        # 训练曲线截图
├── configs/                       # 训练参数与 DeepSpeed 配置
├── data/README.md                 # 官方数据获取与放置说明
├── docs/experiment_scores.md      # 实验分数记录
├── scripts/prepare_data.py        # 官方 JSON 转 ms-swift JSONL
├── scripts/train_lora.sh          # LoRA 训练脚本
├── scripts/infer.sh               # 推理脚本
├── scripts/export_submission.py   # JSONL 预测结果转提交 txt
├── DATA_NOTICE.md                 # 数据版权与使用说明
├── MODEL_CARD.md                  # 模型用途、限制与风险说明
├── requirements.txt
└── 基于GLM_4_9B_LoRA的细粒度中文仇恨言论识别.pdf
```

## 数据准备

本仓库不再分发比赛原始数据或由原始数据转换出的训练/测试 JSONL。请按比赛规则从官方渠道获取数据，并放置为：

```text
data/train.json
data/test2.json
```

详见 [data/README.md](data/README.md) 与 [DATA_NOTICE.md](DATA_NOTICE.md)。

## 环境安装

建议使用 Python 3.10+ 与 CUDA 环境。

```bash
pip install -r requirements.txt
```

硬件参考配置：

- GPU：2 x NVIDIA GPU，每卡 24GB 显存
- CPU：24 核
- 内存：64GB

## 复现流程

1. 生成 ms-swift 训练数据：

```bash
python scripts/prepare_data.py \
  --train-json data/train.json \
  --test-json data/test2.json \
  --output-dir output
```

2. 训练 LoRA：

```bash
bash scripts/train_lora.sh
```

可通过环境变量覆盖默认参数：

```bash
MODEL_PATH=ZhipuAI/GLM-4-9B-0414 \
TRAIN_DATA=output/sft_data.jsonl \
OUTPUT_DIR=output/glm_4_9b_lora \
bash scripts/train_lora.sh
```

3. 推理：

```bash
ADAPTER_PATH=output/glm_4_9b_lora/v1-xxxx/checkpoint-xxxx \
TEST_DATA=output/test_data.jsonl \
bash scripts/infer.sh
```

4. 导出提交文件：

```bash
python scripts/export_submission.py \
  --predict-jsonl output/predict_result.jsonl \
  --output-txt output/predict_result.txt
```

## 比赛信息

- 竞赛名称：细粒度片段级中文仇恨言论识别
- 竞赛地址：[天池竞赛平台](https://tianchi.aliyun.com/competition/entrance/532298/information)
- 官方仓库：[DUTIR-Emotion-Group/CCL2025-Chinese-Hate-Speech-Detection](https://github.com/DUTIR-Emotion-Group/CCL2025-Chinese-Hate-Speech-Detection)

## 说明

本项目包含有害文本检测相关内容，仅用于科研与比赛复现。模型输出可能存在偏见、漏检、误检或格式错误，不应直接用于线上自动化执法、内容处罚或高风险决策。




