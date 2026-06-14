#!/usr/bin/env bash
set -euo pipefail

: "${ADAPTER_PATH:?Set ADAPTER_PATH to a LoRA checkpoint directory, for example output/glm_4_9b_lora/v1-xxxx/checkpoint-xxxx}"

TEST_DATA="${TEST_DATA:-output/test_data.jsonl}"
RESULT_PATH="${RESULT_PATH:-output/predict_result.jsonl}"
CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"

export CUDA_VISIBLE_DEVICES

swift infer \
  --adapters "${ADAPTER_PATH}" \
  --max_batch_size 1 \
  --infer_backend pt \
  --max_length 1000 \
  --num_beams 3 \
  --dataset_shuffle false \
  --split_dataset_ratio 1.0 \
  --dataset "${TEST_DATA}" \
  --seed 2025 \
  --result_path "${RESULT_PATH}"
