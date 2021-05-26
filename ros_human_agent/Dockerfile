ARG ROS_DISTRO="melodic"

FROM ros:$ROS_DISTRO-ros-base

WORKDIR /workspace

ENV DEBIAN_FRONTEND "noninteractive"

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG http_proxy

RUN apt-get update && apt-get install --reinstall -y locales && locale-gen en_US.UTF-8 && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US
ENV LC_ALL en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update; \
  if [ "$ROS_DISTRO" = "melodic" ]; then \
    apt-get install -y --no-install-recommends \
      ros-${ROS_DISTRO}-rosbridge-suite \
      python-setuptools \
      python3-setuptools \
      python-wheel \
      python3-wheel \
      python-pip \
      python3-pip \
      && python2 -m pip install --upgrade pip \
      && python3 -m pip install --upgrade pip; \
  elif [ "$ROS_DISTRO" = "noetic" ]; then \
    apt-get install -y --no-install-recommends \
      ros-${ROS_DISTRO}-rosbridge-suite \
      python-is-python3 \
      python3-setuptools \
      python3-wheel \
      python3-pip \
      && python3 -m pip install --upgrade pip; \
  elif [ "$ROS_DISTRO" = "foxy" ]; then \
    apt-get install -y --no-install-recommends \
      # TODO: This should be installed by rosdep
      python3-opencv \
      python3-setuptools \
      python3-wheel \
      python3-pip \
      && python3 -m pip install --upgrade pip; \
  fi; \
  rm -rf /var/lib/apt/lists/*

ENV CARLA_ROOT "/workspace/CARLA"
ENV SCENARIO_RUNNER_ROOT "/workspace/scenario_runner"
ENV LEADERBOARD_ROOT "/workspace/leaderboard"
ENV CARLA_ROS_BRIDGE_ROOT "/workspace/carla_ros_bridge"
ENV TEAM_CODE_ROOT "/workspace/team_code"

COPY .tmp/PythonAPI ${CARLA_ROOT}/PythonAPI
COPY .tmp/scenario_runner ${SCENARIO_RUNNER_ROOT}
COPY .tmp/leaderboard ${LEADERBOARD_ROOT}

COPY .tmp/ros-bridge/carla_ros_bridge ${CARLA_ROS_BRIDGE_ROOT}/src/carla_ros_bridge
COPY .tmp/ros-bridge/carla_common ${CARLA_ROS_BRIDGE_ROOT}/src/carla_common
COPY .tmp/ros-bridge/carla_msgs ${CARLA_ROS_BRIDGE_ROOT}/src/carla_msgs
COPY .tmp/ros-bridge/ros_compatibility ${CARLA_ROS_BRIDGE_ROOT}/src/ros_compatibility

COPY .tmp/team_code ${TEAM_CODE_ROOT}

RUN pip3 install --user -r ${SCENARIO_RUNNER_ROOT}/requirements.txt
RUN pip3 install --user -r ${LEADERBOARD_ROOT}/requirements.txt

# Install carla ros bridge
RUN /bin/bash -c 'source /opt/ros/$ROS_DISTRO/setup.bash; \
  apt-get update && rosdep update; \
  cd /workspace/carla_ros_bridge; \
  rm -rf build devel install log; \
  rosdep install --from-paths src --ignore-src -r -y; \
  if [ "$ROS_VERSION" = "1" ]; then \
    catkin_make install -DCMAKE_INSTALL_PREFIX=/opt/ros/$ROS_DISTRO; \
  else \
    colcon build; \
  fi; \
  rm -rf build devel log; \
  rm -rf /var/lib/apt/lists/*'

# Install agent
RUN /bin/bash -c 'source /opt/ros/$ROS_DISTRO/setup.bash; \
  apt-get update && rosdep update; \
  cd /workspace/team_code; \
  rm -rf build devel install log; \
  rosdep install --from-paths src --ignore-src -r -y; \
  if [ "$ROS_VERSION" = "1" ]; then \
    catkin_make install; \
  else \
    colcon build; \
  fi; \
  rm -rf build devel log; \
  rm -rf /var/lib/apt/lists/*'

RUN mkdir -p /workspace/results
RUN chmod +x /workspace/leaderboard/scripts/run_evaluation.sh

ENV PYTHONPATH "${CARLA_ROOT}/PythonAPI/carla":"${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":${PYTHONPATH}

RUN if [ "$ROS_DISTRO" = "melodic" ]; then \
    echo "${CARLA_ROOT}/PythonAPI/carla/dist/carla-leaderboard-py2x.egg" > /usr/local/lib/python2.7/dist-packages/carla.pth; \
    echo "${CARLA_ROOT}/PythonAPI/carla/dist/carla-leaderboard-py3x.egg" > /usr/local/lib/python3.6/dist-packages/carla.pth; \
  else \
    echo "${CARLA_ROOT}/PythonAPI/carla/dist/carla-leaderboard-py3x.egg" > /usr/local/lib/python3.8/dist-packages/carla.pth; \
  fi

RUN pip3 install roslibpy

############################################################################################
####                     BEGINNING OF AGENT SPECIFIC COMMANDS                           ####
############################################################################################

RUN pip2 install --user -r ${SCENARIO_RUNNER_ROOT}/requirements.txt
RUN pip2 install pygame==1.9.6

ENV TEAM_AGENT ${TEAM_CODE_ROOT}/ros_human_agent.py
ENV CHALLENGE_TRACK_CODENAME SENSORS

############################################################################################
####                        END OF AGENT SPECIFIC COMMANDS                              ####
############################################################################################

ENV SCENARIOS ${LEADERBOARD_ROOT}/data/all_towns_traffic_scenarios_public.json
ENV ROUTES ${LEADERBOARD_ROOT}/data/routes_training.xml
ENV REPETITIONS 1
ENV CHECKPOINT_ENDPOINT /workspace/results/results.json
ENV DEBUG_CHALLENGE 0

ENV HTTP_PROXY ""
ENV HTTPS_PROXY ""
ENV http_proxy ""
ENV https_proxy ""

# Agent sources
RUN /bin/echo \
  'source /opt/ros/$ROS_DISTRO/setup.bash; \
  if [ "$ROS_VERSION" = "2" ]; then \
    source $CARLA_ROS_BRIDGE_ROOT/install/setup.bash; \
  fi; \
  source $TEAM_CODE_ROOT/install/setup.bash;' >> ${HOME}/agent_sources.sh

COPY .tmp/entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

CMD ["/bin/bash"]
