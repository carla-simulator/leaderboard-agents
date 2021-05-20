#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

${SCRIPT_DIR}/docker-gui \
    -it \
    --rm \
    --net=host \
    --volume=${SCRIPT_DIR}/../submodules/leaderboard:/workspace/leaderboard:rw \
    --volume=${SCRIPT_DIR}/../submodules/scenario_runner:/workspace/scenario_runner:rw \
    --volume=${SCRIPT_DIR}/../submodules/ros-bridge:/workspace/carla_ros_bridge/src:rw \
    --volume=${SCRIPT_DIR}/team_code/src:/workspace/team_code/src:rw \
    --volume=${SCRIPT_DIR}/team_code/ros_human_agent.py:/workspace/team_code/ros_human_agent.py:rw \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    ros_human_agent:latest /bin/bash
