# GLM-4-9B-LoRA-HateSpeech

中文为主的项目说明。英文版请点击下方折叠区展开。

<details>
<summary><strong>English version (click to expand)</strong></summary>

## Fine-Grained Chinese Hate Speech Detection Based on GLM-4-9B with LoRA

This repository contains the reproducible competition release for CCL25-Eval Task 10 / Tianchi Fine-Grained Chinese Hate Speech Detection. The method fine-tunes GLM-4-9B-0414 with LoRA to extract structured hate-speech quadruples from Chinese social-media text.

### Task

Input: a social-media comment.

Output:

```text
Target | Argument | Targeted Group | Hateful [END]
```

Multiple quadruples are separated by `[SEP]`.

### Method

- Base model: [GLM-4-9B-0414](https://www.modelscope.cn/models/ZhipuAI/GLM-4-9B-0414)
- Training method: LoRA SFT
- Framework: ms-swift
- Local best recorded score: `0.3566` with `glm-4-9b-0414 v1`

### Reproduction Status

The repository supports reproducing the training and inference pipeline, but it does not include the competition dataset or model checkpoints. To reproduce the result, obtain the official data from the competition organizers and place it under:

```text
data/train.json
data/test2.json
```

Then run:

```bash
python scripts/prepare_data.py --train-json data/train.json --test-json data/test2.json --output-dir output
bash scripts/train_lora.sh
ADAPTER_PATH=output/glm_4_9b_lora/v1-xxxx/checkpoint-xxxx bash scripts/infer.sh
python scripts/export_submission.py --predict-jsonl output/predict_result.jsonl --output-txt output/predict_result.txt
```

### Data and Privacy

This repository does not distribute the original competition data, converted JSONL files, prediction files, checkpoints, or LoRA weights. See [DATA_NOTICE.md](DATA_NOTICE.md) and [MODEL_CARD.md](MODEL_CARD.md).

</details>

## 项目简介

本项目是 CCL25-Eval Task 10 / 天池「细粒度中文仇恨识别评测」的参赛方案整理版。方案基于 GLM-4-9B-0414，通过 LoRA 监督微调，将中文社交媒体评论生成结构化仇恨言论四元组。

任务输出格式：

```text
Target | Argument | Targeted Group | Hateful [END]
```

如果一条样本包含多个四元组，使用 `[SEP]` 分隔。

示例：

```text
老黑 | 讨厌 | Racism | hate [SEP] 媚黑的 | 倒贴 | Racism | hate [END]
```

## 方法概览

- 基座模型：[GLM-4-9B-0414](https://www.modelscope.cn/models/ZhipuAI/GLM-4-9B-0414)
- 训练方式：LoRA SFT
- 训练框架：ms-swift
- 主要目标：生成符合比赛格式的仇恨言论四元组
- 本地记录最佳公开分数：`0.3566`，对应 `glm-4-9b-0414 v1`

## 当前仓库能复现到什么程度

当前仓库支持复现完整训练和推理流程，但不包含比赛原始数据、转换后的 JSONL、提交文件、checkpoint 或 LoRA 权重。因此它不是“下载后直接跑出同分数”的完整包，而是一个合规的复现脚手架。

复现者还需要自行准备：

- `data/train.json`：官方训练集
- `data/test2.json`：官方复赛/测试输入
- GLM-4-9B-0414 基座模型访问权限或本地模型路径
- CUDA/PyTorch/ms-swift 训练环境
- 足够显存的 GPU 资源

不建议上传到仓库的内容：

- 官方原始数据与派生 JSONL
- 最终提交文件
- 大模型权重、LoRA checkpoint、`.safetensors`、`.bin`
- 本地课程资料、PPT、临时 Office 文件、服务器连接配置

## 仓库结构

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

本仓库不公开分发比赛原始数据或由原始数据转换出的训练/测试 JSONL。请按比赛规则从官方渠道获取数据，并放置为：

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

## 隐私与数据说明

当前主干不包含密钥、Token、本地绝对路径、服务器连接配置、原始数据、派生 JSONL、预测提交文件或大权重。

需要注意：仓库中的论文 PDF 保留了论文署名信息，包括作者姓名、学校学院和联系邮箱。如果你希望项目完全匿名，应替换为匿名版 PDF 或删除该 PDF。

另外，旧版 zip 虽已从当前主干删除，但仍可能存在于 Git 历史中。若需要从公开历史中彻底移除，需要单独执行历史清理并强推。

## 比赛信息

- 竞赛名称：细粒度片段级中文仇恨言论识别
- 竞赛地址：[天池竞赛平台](https://tianchi.aliyun.com/competition/entrance/532298/information)
- 官方仓库：[DUTIR-Emotion-Group/CCL2025-Chinese-Hate-Speech-Detection](https://github.com/DUTIR-Emotion-Group/CCL2025-Chinese-Hate-Speech-Detection)

## 风险提示

本项目包含有害文本检测相关内容，仅用于科研与比赛复现。模型输出可能存在偏见、漏检、误检或格式错误，不应直接用于线上自动化执法、内容处罚或高风险决策。
