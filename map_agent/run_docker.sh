#!/bin/bash

docker run \
    -it \
    --rm \
    --net=host \
    map_agent:latest /bin/bash
