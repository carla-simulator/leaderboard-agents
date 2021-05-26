#!/bin/bash

DOC_STRING="Benchmark your agent in CARLA scenarios."

USAGE_STRING=$(cat <<- END
Usage: $0 [-h|--help] [-o |--output FILENAME]
END
)

usage() { echo "$DOC_STRING"; echo "$USAGE_STRING"; exit 1; }

BENCHMARK_FILENAME="benchmark.md"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o |--output )
      BENCHMARK_FILENAME=$2
      shift 2 ;;
    -h | --help )
      usage
      ;;
    * )
      shift ;;
  esac
done

[[ -d "/workspace/results/benchmark" ]] || mkdir "/workspace/results/benchmark"

python3 ${TEAM_CODE_ROOT}/benchmark/leaderboard_evaluator.py \
--scenarios=${SCENARIOS}  \
--routes=${ROUTES} \
--repetitions=${REPETITIONS} \
--track=${CHALLENGE_TRACK_CODENAME} \
--checkpoint=${CHECKPOINT_ENDPOINT} \
--agent=${TEAM_CODE_ROOT}/benchmark/benchmark_agent.py \
--agent-config=${TEAM_CONFIG} \
--debug=${DEBUG_CHALLENGE} \
--record=${RECORD_PATH} \
--resume=${RESUME} \
--benchmark-filename=/workspace/results/benchmark/${BENCHMARK_FILENAME}
