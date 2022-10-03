#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

${SCRIPT_DIR}/../_utils/docker-gui \
    -it \
    --rm \
    --net=host \
    --privileged \
    --volume=${SCRIPT_DIR}/../_submodules/leaderboard:/workspace/leaderboard:rw \
    --volume=${SCRIPT_DIR}/../_submodules/scenario_runner:/workspace/scenario_runner:rw \
    --volume=${SCRIPT_DIR}/../_submodules/ros-bridge/carla_ros_bridge:/workspace/carla_ros_bridge/src/carla_ros_bridge:rw \
    --volume=${SCRIPT_DIR}/../_submodules/ros-bridge/carla_common:/workspace/carla_ros_bridge/src/carla_common:rw \
    --volume=${SCRIPT_DIR}/../_submodules/ros-bridge/carla_msgs:/workspace/carla_ros_bridge/src/carla_msgs:rw \
    --volume=${SCRIPT_DIR}/../_submodules/ros-bridge/ros_compatibility:/workspace/carla_ros_bridge/src/ros_compatibility:rw \
    --volume=${SCRIPT_DIR}/team_code/src:/workspace/team_code/src:rw \
    --volume=${SCRIPT_DIR}/team_code/ros_map_agent.py:/workspace/team_code/ros_map_agent.py:rw \
    --volume=${SCRIPT_DIR}/team_code/src/ros_map_agent/src/ros_map_agent/map_agent:/workspace/team_code/src/ros_map_agent/src/ros_map_agent/map_agent:rw \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    --volume=${SCRIPT_DIR}/log:/workspace/log:rw \
    --volume=${SCRIPT_DIR}/../data:/workspace/data\
    --env ROUTES=/workspace/data/old_routes_training.xml \
    --env ROUTES=/workspace/leaderboard/data/new_routes_training.xml \
    --env ROUTES=/workspace/data/old_routes_training.xml \
    --env DEBUG_CHALLENGE=2 \
    --env DEBUG_CHECKPOINT_ENDPOINT=/workspace/results/live_results.txt \
    ros_map_agent:latest /bin/bash

#--volume=${SCRIPT_DIR}/../data:/workspace/data\
#--env ROUTES=/workspace/data/old_routes_training.xml \

#--env ROUTES_SUBSET=0-2 \
#--env ROUTES=/workspace/leaderboard/data/new_routes_training.xml \
