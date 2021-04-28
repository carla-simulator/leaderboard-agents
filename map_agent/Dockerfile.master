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

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    vim \
    ca-certificates \
    castxml \
    doxygen \
    graphviz \
    gnupg2 \
    lsb-release \
    libproj-dev \
    libboost-all-dev \
    libpugixml-dev \
    libgtest-dev \
    libpython-dev \
    libosmium2-dev \
    liblapacke-dev \
    libjpeg-dev \
    libpng16-16 \
    libtiff5 \
    libpng-dev \
    python-dev \
    python-pip \
    python-setuptools \
    python-wheel \
    python3-dev \
    python3-pip \
    python3-wheel \
    python3-setuptools &&\
    python -m pip install --upgrade pip && \
    python3 -m pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --user setuptools py_trees==0.8.3 psutil shapely six dictor requests ephem tabulate networkx==2.2 simple-watchdog-timer
RUN pip3 install --user setuptools py_trees==0.8.3 psutil shapely six dictor requests ephem tabulate networkx==2.2 simple-watchdog-timer

RUN python2 -m pip install --user pygccxml pyplusplus xmlrunner pygame xmlschema==1.0.18 opencv-python==4.2.0.32
RUN python3 -m pip install --user pygccxml pyplusplus xmlrunner pygame xmlschema==1.0.18 opencv-python==4.2.0.32

# Copy the files into the docker
WORKDIR /workspace

ENV CARLA_ROOT "/workspace/CARLA"
ENV SCENARIO_RUNNER_ROOT "/workspace/scenario_runner"
ENV LEADERBOARD_ROOT "/workspace/leaderboard"
ENV TEAM_CODE_ROOT "/workspace/team_code"
ENV MAP_ROOT "/workspace/map"

COPY .tmp/PythonAPI ${CARLA_ROOT}/PythonAPI
COPY .tmp/scenario_runner ${SCENARIO_RUNNER_ROOT}
COPY .tmp/leaderboard ${LEADERBOARD_ROOT}
COPY .tmp/team_code ${TEAM_CODE_ROOT}
COPY .tmp/map ${MAP_ROOT}

RUN mkdir -p /workspace/results
RUN chmod +x $LEADERBOARD_ROOT/scripts/run_evaluation.sh

# install colcon and build the code
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-colcon-common-extensions \
        && rm -rf /var/lib/apt/lists/*
RUN cd $MAP_ROOT && colcon build --metas colcon_python.meta

# Set environment variables
ENV PYTHONPATH "/workspace/CARLA/PythonAPI/carla/dist/carla-leaderboard-py3x.egg":"${SCENARIO_RUNNER_ROOT}":"${CARLA_ROOT}/PythonAPI/carla":"${LEADERBOARD_ROOT}":"$MAP_ROOT/install/ad_map_access/lib/python3.6":$TEAM_CODE_ROOT:${PYTHONPATH}

ENV TEAM_AGENT ${TEAM_CODE_ROOT}/map_agent.py
ENV CHALLENGE_TRACK_CODENAME MAP
ENV SCENARIOS ${LEADERBOARD_ROOT}/data/all_towns_traffic_scenarios_public.json
ENV ROUTES ${LEADERBOARD_ROOT}/data/routes_training.xml
ENV REPETITIONS 1
ENV CHECKPOINT_ENDPOINT /workspace/results/results.json
ENV DEBUG_CHALLENGE 0

ENV HTTP_PROXY ""
ENV HTTPS_PROXY ""
ENV http_proxy ""
ENV https_proxy ""

CMD ["/bin/bash"]
