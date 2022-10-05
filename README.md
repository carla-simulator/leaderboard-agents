# Leaderboard agents

This repository serves as a guideline for users to see how to run different agents inside the leaderboard. Each of these agents can be directly run on a local version of the Leaderboard, and they also come with their own docker files, to easily understand the steps needed to submit them into the Leaderboard itself. Additionally, all agents have there own specific purposes, so it is recommended to check them out and see if they suit your needs. Full documentation of the Leaderboard can be found [here](https://leaderboard.carla.org/).

## Get started

### Requirements

* Docker (19.03+)
* Nvidia docker (https://github.com/NVIDIA/nvidia-docker)

### Setup

Firstly, clone the leaderboard agents repository:

```
git clone --recurse-submodules https://github.com/carla-simulator/leaderboard-agents.git
```

The Leadeboard 2.0 **requires a specific version of CARLA**. You can download it from [here](https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/Leaderboard/CARLA_Leaderboard_20.tar.gz).
While some agents might have slight variations of this process, it is only needed to **set the `CARLA_ROOT` environment variable** to point to your CARLA root folder:

```sh
export CARLA_ROOT=<path-to-carla>
```

We recommend adding this command to your `.bashrc` file to set it permanently.

### Building the agent docker image

To ease the creation of the docker files, each agent is already prepared with its own files, and they only have to be run in order to automatically create them. For instance, to build the `human-agent` stack:

```sh
bash human_agent/make_docker.sh
```

This will generate a `human_agent:latest` docker image

### Running the agent

1. Run the CARLA server

```sh
${CARLA_ROOT}/CarlaUE4.sh
```

2. Run the agent image:

```sh
bash human_agent/run_docker.sh
```

This will start an interactive sheel inside the container. To start the agent run the following command:

```sh
bash leaderboard/scripts/run_evaluation.sh
```

By default, all dockers have a shared volume corresponding to the `results` folder.

## Repository structure

In order to run the Leaderboard, you need to also have [CARLA](https://github.com/carla-simulator/carla) as well as [ScenarioRunner](https://github.com/carla-simulator/scenario_runner) installed. Both ScenarioRunner and the Leaderboard are available in this repository, inside the `_submodules` folder, and they will be automatically fetched when creating the docker.

The `_submodules` folder also contains references to other packages needed by specific agents. The following table shows the exact submodules used for each agent:

| Agent | ScenarioRunner | Leaderboard | ROS Bridge |
| ---- | ----- | ----- | ------------- | -------- |
| Human Agent |  &#9989; | &#9989;|  |
| ROS human agent | &#9989; | &#9989;| &#9989;|
| ROS2 human agent | &#9989; | &#9989;| &#9989;|
| Performance agent | &#9989; | &#9989; |  |
| Log agent | &#9989; | &#9989; |  |

**Note:** Remember you can download all the submodules using

```
git submodule update --init --recursive
```

or if you only want a specific one:

```
git submodule update --init --recursive <path to specific submodule>
```
