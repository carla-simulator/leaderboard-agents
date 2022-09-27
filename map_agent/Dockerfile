FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG http_proxy

RUN apt-get update && apt-get install --reinstall -y locales && locale-gen en_US.UTF-8 && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US
ENV LC_ALL en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    vim \
    ca-certificates \
    libjpeg-dev \
    libpng16-16 \
    libtiff5 \
    libpng-dev \
    python3-dev \
    python3-pip \
    python3-setuptools && \
    python3 -m pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# Copy the files into the docker
WORKDIR /workspace

ENV CARLA_ROOT "/workspace/CARLA"
ENV SCENARIO_RUNNER_ROOT "/workspace/scenario_runner"
ENV LEADERBOARD_ROOT "/workspace/leaderboard"
ENV TEAM_CODE_ROOT "/workspace/team_code"

COPY .tmp/PythonAPI ${CARLA_ROOT}/PythonAPI
COPY .tmp/scenario_runner ${SCENARIO_RUNNER_ROOT}
COPY .tmp/leaderboard ${LEADERBOARD_ROOT}
COPY .tmp/team_code ${TEAM_CODE_ROOT}

RUN pip3 install -r ${SCENARIO_RUNNER_ROOT}/requirements.txt
RUN pip3 install -r ${LEADERBOARD_ROOT}/requirements.txt

RUN mkdir -p /workspace/results
RUN chmod +x $LEADERBOARD_ROOT/scripts/run_evaluation.sh

ENV PYTHONPATH "${CARLA_ROOT}/PythonAPI/carla/dist/carla-leaderboard-py3x.egg":"${SCENARIO_RUNNER_ROOT}":"${CARLA_ROOT}/PythonAPI/carla":"${LEADERBOARD_ROOT}":"$MAP_ROOT/install/ad_map_access/lib/python3.6":$TEAM_CODE_ROOT:${PYTHONPATH}

############################################################################################
####                     BEGINNING OF AGENT SPECIFIC COMMANDS                           ####
############################################################################################
RUN python3 -m pip install --user ad-map-access

ENV TEAM_AGENT ${TEAM_CODE_ROOT}/ad_map_agent.py
ENV CHALLENGE_TRACK_CODENAME MAP
############################################################################################
####                        END OF AGENT SPECIFIC COMMANDS                              ####
############################################################################################

ENV ROUTES ${LEADERBOARD_ROOT}/data/routes_training.xml
ENV REPETITIONS 1
ENV CHECKPOINT_ENDPOINT /workspace/results/results.json
ENV DEBUG_CHALLENGE 0

ENV HTTP_PROXY ""
ENV HTTPS_PROXY ""
ENV http_proxy ""
ENV https_proxy ""

CMD ["/bin/bash"]
