ARG DISTRIBUTION=18.04
FROM ubuntu:${DISTRIBUTION} AS ubuntu

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG http_proxy

RUN apt-get update && apt-get install --reinstall -y locales && locale-gen en_US.UTF-8 && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US
ENV LC_ALL en_US.UTF-8

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpng-dev \
    libjpeg-dev \
    libtiff5 \
    python3-pip \
    python3-setuptools &&\
    python3 -m pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the files into the docker
WORKDIR /workspace

ENV CARLA_ROOT "/workspace/CARLA"
ENV SCENARIO_RUNNER_ROOT "/workspace/scenario_runner"
ENV LEADERBOARD_ROOT "/workspace/leaderboard"
ENV TEAM_CODE_ROOT "/workspace/team_code"

COPY .tmp/scenario_runner ${SCENARIO_RUNNER_ROOT}
COPY .tmp/leaderboard ${LEADERBOARD_ROOT}

RUN pip3 install --user -r ${SCENARIO_RUNNER_ROOT}/requirements.txt
RUN pip3 install --user -r ${LEADERBOARD_ROOT}/requirements.txt

RUN mkdir -p /workspace/results
RUN chmod +x $LEADERBOARD_ROOT/scripts/run_evaluation.sh

ENV PYTHONPATH ${SCENARIO_RUNNER_ROOT}:${LEADERBOARD_ROOT}:${TEAM_CODE_ROOT}:${PYTHONPATH}

########################################################################################################################
########################################################################################################################
############                                BEGINNING OF AGENT COMMANDS                                      ###########
########################################################################################################################
########################################################################################################################

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    gnupg \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://developer.download.nvidia.com/devtools/repos/ubuntu2004/amd64/nvidia.pub | apt-key add - \
    && echo "deb https://developer.download.nvidia.com/devtools/repos/ubuntu2004/amd64/ /" >> /etc/apt/sources.list.d/nsight.list \
    && apt-get update && apt-get install -y --no-install-recommends nsight-systems-cli-2021.2.1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --user nvtx

ENV TEAM_AGENT ${TEAM_CODE_ROOT}/profiler_agent.py
ENV CHALLENGE_TRACK_CODENAME SENSORS
ENV SCENARIOS ${LEADERBOARD_ROOT}/data/all_towns_traffic_scenarios_public.json
ENV ROUTES ${TEAM_CODE_ROOT}/data/routes_training.xml
ENV REPETITIONS 1
ENV CHECKPOINT_ENDPOINT /workspace/results/results.json
ENV DEBUG_CHALLENGE 0

COPY .tmp/entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

########################################################################################################################
########################################################################################################################
############                                   END OF AGENT COMMANDS                                         ###########
########################################################################################################################
########################################################################################################################

ENV HTTP_PROXY ""
ENV HTTPS_PROXY ""
ENV http_proxy ""
ENV https_proxy ""

CMD ["/bin/bash"]
