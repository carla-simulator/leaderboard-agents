#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

${SCRIPT_DIR}/docker-gui \
    -it \
    --rm \
    --privileged \
    --net=host \
    --volume=${SCRIPT_DIR}/../submodules/leaderboard:/workspace/leaderboard:rw \
    --volume=${SCRIPT_DIR}/../submodules/scenario_runner:/workspace/scenario_runner:rw \
    --volume=${SCRIPT_DIR}/../submodules/ros-bridge:/workspace/carla_ros_bridge/src:rw \
    --volume=${SCRIPT_DIR}/team_code/src:/workspace/team_code/src:rw \
    --volume=${SCRIPT_DIR}/team_code/ros2_human_agent.py:/workspace/team_code/ros2_human_agent.py:rw \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    --volume=${SCRIPT_DIR}/log:/workspace/log:rw \
    --env ROUTES_SUBSET=0-2 \
    --env ROUTES=/workspace/leaderboard/data/new_routes_training.xml \
    --env DEBUG_CHALLENGE=2 \
    --env DEBUG_CHECKPOINT_ENDPOINT=/workspace/results/live_results.txt \
    ros2_human_agent:latest /bin/bash

#--volume=${SCRIPT_DIR}/../data:/workspace/data\
