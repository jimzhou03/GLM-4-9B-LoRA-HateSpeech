# GLM-4-9B-LoRA-HateSpeech

**语言 / Language:** 中文 | [English](#english)

## 中文

### 项目简介

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

### 方法概览

- 基座模型：[GLM-4-9B-0414](https://www.modelscope.cn/models/ZhipuAI/GLM-4-9B-0414)
- 训练方式：LoRA SFT
- 训练框架：ms-swift
- 主要目标：生成符合比赛格式的仇恨言论四元组
- 实验记录最佳公开分数：`0.3566`，对应 `glm-4-9b-0414 v1`

### 复现范围

本仓库支持复现完整训练和推理流程，但不直接提交比赛原始数据、转换后的 JSONL、提交文件、checkpoint 或 LoRA 权重。因此它是一个合规的复现脚手架，而不是“克隆后直接跑出同分数”的完整包。

复现实验需要准备：

- `data/train.json`：官方训练集
- `data/test1.json`：官方测试输入，可用于初赛或格式检查
- `data/test2.json`：官方复赛/最终测试输入
- GLM-4-9B-0414 基座模型，或云服务中已挂载/部署好的本地模型路径
- CUDA/PyTorch/ms-swift 训练环境
- 足够显存的 GPU 资源
- 如果不重新训练、只想直接推理，还需要最终 LoRA adapter/checkpoint

比赛数据文件未纳入本仓库，以避免二次公开分发比赛数据。复现时请按比赛规则从官方渠道获取数据，并放入 `data/` 目录。

### 仓库结构

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
├── LICENSE                        # MIT License，仅覆盖本仓库代码
├── requirements.txt
└── 基于GLM_4_9B_LoRA的细粒度中文仇恨言论识别.pdf
```

### 数据准备

本仓库不公开分发比赛原始数据或由原始数据转换出的训练/测试 JSONL。请按比赛规则从官方渠道获取数据，并放置为：

```text
data/train.json
data/test1.json
data/test2.json
```

生成 ms-swift 训练与推理数据：

```bash
python scripts/prepare_data.py \
  --train-json data/train.json \
  --test-json data/test2.json \
  --output-dir output
```

详见 [data/README.md](data/README.md) 与 [DATA_NOTICE.md](DATA_NOTICE.md)。

### 环境安装

建议使用 Python 3.10+ 与 CUDA 环境。

```bash
pip install -r requirements.txt
```

论文和本仓库记录的硬件参考配置：

- GPU：2 x NVIDIA GPU，每卡 24GB 显存
- CPU：24 核
- 内存：64GB

如果 GLM-4-9B-0414 已经在云服务中部署或挂载，不需要额外下载模型到仓库，只需要在训练和推理时把 `MODEL_PATH` 或 `ADAPTER_PATH` 指向云环境中的对应路径。

### 复现流程

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
MODEL_PATH=/path/to/GLM-4-9B-0414 \
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

### 未纳入仓库的内容

- 官方原始数据与派生 JSONL
- 最终提交文件
- 大模型权重、LoRA checkpoint、`.safetensors`、`.bin`
- 本地课程资料、PPT、临时 Office 文件、服务器连接配置

### 隐私与数据说明

当前发布版本不包含密钥、Token、本地绝对路径、服务器连接配置、原始数据、派生 JSONL、预测提交文件或大权重。

需要注意：仓库中的论文 PDF 保留了论文署名信息，包括作者姓名、学校学院和联系邮箱。如需完全匿名发布，应替换为匿名版 PDF 或删除该 PDF。

另外，旧版 zip 虽已从当前发布版本删除，但仍可能存在于 Git 历史中。若需要从公开历史中彻底移除，需要单独执行历史清理并强推。

### License

本仓库代码使用 [MIT License](LICENSE)。比赛数据、基座模型、LoRA 权重和论文 PDF 不自动包含在 MIT License 授权范围内，需分别遵守其原始许可或发布规则。

### 比赛信息

- 竞赛名称：细粒度片段级中文仇恨言论识别
- 竞赛地址：[天池竞赛平台](https://tianchi.aliyun.com/competition/entrance/532298/information)
- 官方仓库：[DUTIR-Emotion-Group/CCL2025-Chinese-Hate-Speech-Detection](https://github.com/DUTIR-Emotion-Group/CCL2025-Chinese-Hate-Speech-Detection)

### 风险提示

本项目包含有害文本检测相关内容，仅用于科研与比赛复现。模型输出可能存在偏见、漏检、误检或格式错误，不应直接用于线上自动化执法、内容处罚或高风险决策。

---

## English

**Language / 语言:** [中文](#中文) | English

### Project Overview

This repository is the organized competition release for CCL25-Eval Task 10 / Tianchi Fine-Grained Chinese Hate Speech Detection. The method fine-tunes GLM-4-9B-0414 with LoRA supervised fine-tuning to generate structured hate-speech quadruples from Chinese social-media comments.

The output format is:

```text
Target | Argument | Targeted Group | Hateful [END]
```

If one sample contains multiple quadruples, they are separated by `[SEP]`.

Example:

```text
老黑 | 讨厌 | Racism | hate [SEP] 媚黑的 | 倒贴 | Racism | hate [END]
```

### Method Summary

- Base model: [GLM-4-9B-0414](https://www.modelscope.cn/models/ZhipuAI/GLM-4-9B-0414)
- Training method: LoRA SFT
- Training framework: ms-swift
- Main goal: generate hate-speech quadruples that follow the competition format
- Recorded best public score: `0.3566`, corresponding to `glm-4-9b-0414 v1`

### Reproduction Scope

This repository supports the full training and inference workflow, but it does not directly commit the original competition data, converted JSONL files, submission files, checkpoints, or LoRA weights. It is therefore a compliant reproduction scaffold, not a complete package that can reproduce the same score immediately after cloning.

Reproduction requires:

- `data/train.json`: official training set
- `data/test1.json`: official test input, useful for preliminary evaluation or format checks
- `data/test2.json`: official final-round or final test input
- GLM-4-9B-0414 base model, or a local model path already mounted/deployed in a cloud service
- CUDA/PyTorch/ms-swift training environment
- GPU resources with enough VRAM
- The final LoRA adapter/checkpoint if they want inference only without retraining

The competition data files are excluded from this repository to avoid redistributing the dataset. For reproduction, obtain the data from the official competition channel and place it under `data/`.

### Repository Structure

```text
.
├── assets/training_curves/        # training curve screenshots
├── configs/                       # training parameters and DeepSpeed config
├── data/README.md                 # official data acquisition and placement notes
├── docs/experiment_scores.md      # experiment score records
├── scripts/prepare_data.py        # convert official JSON to ms-swift JSONL
├── scripts/train_lora.sh          # LoRA training script
├── scripts/infer.sh               # inference script
├── scripts/export_submission.py   # convert JSONL predictions to submission txt
├── DATA_NOTICE.md                 # data copyright and usage notice
├── MODEL_CARD.md                  # model use, limitations, and risk notes
├── LICENSE                        # MIT License, code only
├── requirements.txt
└── 基于GLM_4_9B_LoRA的细粒度中文仇恨言论识别.pdf
```

### Data Preparation

This repository does not publicly distribute the original competition data or the converted train/test JSONL files. Please obtain the data from the official channel under the competition rules, and place the files as:

```text
data/train.json
data/test1.json
data/test2.json
```

Generate ms-swift training and inference data:

```bash
python scripts/prepare_data.py \
  --train-json data/train.json \
  --test-json data/test2.json \
  --output-dir output
```

See [data/README.md](data/README.md) and [DATA_NOTICE.md](DATA_NOTICE.md).

### Environment Setup

Python 3.10+ and a CUDA environment are recommended.

```bash
pip install -r requirements.txt
```

Hardware reference recorded in the paper and this repository:

- GPU: 2 x NVIDIA GPUs, 24GB VRAM per card
- CPU: 24 cores
- RAM: 64GB

If GLM-4-9B-0414 has already been deployed or mounted in a cloud service, the model does not need to be stored in this repository. During training or inference, set `MODEL_PATH` or `ADAPTER_PATH` to the corresponding path in the cloud environment.

### Reproduction Workflow

1. Generate ms-swift training data:

```bash
python scripts/prepare_data.py \
  --train-json data/train.json \
  --test-json data/test2.json \
  --output-dir output
```

2. Train LoRA:

```bash
bash scripts/train_lora.sh
```

Default parameters can be overridden with environment variables:

```bash
MODEL_PATH=/path/to/GLM-4-9B-0414 \
TRAIN_DATA=output/sft_data.jsonl \
OUTPUT_DIR=output/glm_4_9b_lora \
bash scripts/train_lora.sh
```

3. Run inference:

```bash
ADAPTER_PATH=output/glm_4_9b_lora/v1-xxxx/checkpoint-xxxx \
TEST_DATA=output/test_data.jsonl \
bash scripts/infer.sh
```

4. Export the submission file:

```bash
python scripts/export_submission.py \
  --predict-jsonl output/predict_result.jsonl \
  --output-txt output/predict_result.txt
```

### Excluded Content

- Official raw data and derived JSONL files
- Final submission files
- Base-model weights, LoRA checkpoints, `.safetensors`, `.bin`
- Local course materials, slides, Office temporary files, and server connection configs

### Privacy and Data Notes

The current release does not contain secrets, tokens, local absolute paths, server connection configs, original data, derived JSONL files, prediction submission files, or large weights.

Note: the paper PDF in this repository keeps the paper byline information, including author names, school/college, and contact email. If the project needs to be fully anonymous, replace it with an anonymized PDF or remove the PDF.

Also, the old zip file has been removed from the current release, but it may still exist in Git history. Removing it from public history requires a separate history rewrite and force push.

### License

The repository code is released under the [MIT License](LICENSE). Competition data, the base model, LoRA weights, and the paper PDF are not automatically covered by the MIT License and must follow their original licenses or release rules.

### Competition Information

- Competition name: Fine-Grained Chinese Hate Speech Detection
- Competition page: [Tianchi](https://tianchi.aliyun.com/competition/entrance/532298/information)
- Official repository: [DUTIR-Emotion-Group/CCL2025-Chinese-Hate-Speech-Detection](https://github.com/DUTIR-Emotion-Group/CCL2025-Chinese-Hate-Speech-Detection)

### Risk Notice

This project involves harmful-text detection and is intended only for research and competition reproduction. Model outputs may contain bias, false negatives, false positives, or formatting errors, and should not be directly used for automated enforcement, content punishment, or high-risk decisions.
