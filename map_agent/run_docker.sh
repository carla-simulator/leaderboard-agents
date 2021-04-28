#!/bin/bash

docker run \
    -it \
    --rm \
    --net=host \
    map_agent_2:latest /bin/bash
