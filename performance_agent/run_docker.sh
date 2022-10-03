#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$CARLA_ROOT" ]; then
  echo "Error $CARLA_ROOT is empty. Set \$CARLA_ROOT as an environment variable first."
  exit 1
fi

docker run \
    -it \
    --rm \
    --privileged \
    --net=host \
    --volume=${SCRIPT_DIR}/../_submodules/leaderboard:/workspace/leaderboard:rw \
    --volume=${SCRIPT_DIR}/../_submodules/scenario_runner:/workspace/scenario_runner:rw \
    --volume=${SCRIPT_DIR}/team_code:/workspace/team_code:rw \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    --volume="${CARLA_ROOT}/PythonAPI":"/workspace/CARLA/PythonAPI":ro \
    profiler_agent:latest /bin/bash
