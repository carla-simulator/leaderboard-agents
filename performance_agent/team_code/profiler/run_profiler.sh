#!/bin/bash

DOC_STRING="Profile the leadeboard."

USAGE_STRING=$(cat <<- END
Usage: $0 [-h|--help]
END
)

usage() { echo "$DOC_STRING"; echo "$USAGE_STRING"; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h | --help )
      usage
      ;;
    * )
      shift ;;
  esac
done

[[ -d "/workspace/results/profiler" ]] || mkdir "/workspace/results/profiler"

python3 ${TEAM_CODE_ROOT}/profiler/leaderboard_evaluator.py \
--scenarios=${SCENARIOS}  \
--routes=${TEAM_CODE_ROOT}/profiler/data/route.xml \
--repetitions=${REPETITIONS} \
--track=${CHALLENGE_TRACK_CODENAME} \
--checkpoint=${CHECKPOINT_ENDPOINT} \
--agent=${TEAM_CODE_ROOT}/profiler/profiler_agent.py \
--agent-config=${TEAM_CONFIG} \
--debug=${DEBUG_CHALLENGE} \
--record=${RECORD_PATH} \
--resume=${RESUME}
