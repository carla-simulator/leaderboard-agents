#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

${SCRIPT_DIR}/docker-gui \
    -it \
    --rm \
    --net=host \
    --volume=${SCRIPT_DIR}/results:/workspace/results:rw \
    ros_human_agent:latest /bin/bash
