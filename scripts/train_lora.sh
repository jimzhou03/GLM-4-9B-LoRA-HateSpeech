#!/usr/bin/env bash
set -euo pipefail

MODEL_PATH="${MODEL_PATH:-ZhipuAI/GLM-4-9B-0414}"
TRAIN_DATA="${TRAIN_DATA:-output/sft_data.jsonl}"
OUTPUT_DIR="${OUTPUT_DIR:-output/glm_4_9b_lora}"
CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"

export CUDA_VISIBLE_DEVICES

swift sft \
  --model "${MODEL_PATH}" \
  --train_type lora \
  --dataset "${TRAIN_DATA}" \
  --dataloader_num_workers 8 \
  --split_dataset_ratio 0.0 \
  --seed 2025 \
  --num_train_epochs 3 \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 8 \
  --per_device_eval_batch_size 1 \
  --lr_scheduler_type cosine \
  --warmup_ratio 0.05 \
  --learning_rate 5e-5 \
  --max_length 1024 \
  --target_modules all-linear \
  --lora_rank 64 \
  --lora_alpha 128 \
  --lora_dropout 0.1 \
  --weight_decay 0.1 \
  --eval_steps 100 \
  --save_steps 100 \
  --save_total_limit 5 \
  --output_dir "${OUTPUT_DIR}" \
  --logging_steps 5
