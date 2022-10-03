# Leaderboard agents

This repository serves as a guideline for users to see how to run different agents inside the leaderboard. Each of these agents can be directly run on a local version of the Leaderboard, and they also come with their own docker files, to easily understand the steps needed to submit them into the Leaderboard itself. Additionally, all agents have there own specific purposes, so it is recommended to check them out and see if they suit your needs.

## Requirements


## Setup

Firstly, clone the leaderboard agents repository:

```
git clone --recurse-submodules https://github.com/carla-simulator/leaderboard-agents.git
```

The Leadeboard 2.0 **requires a specific version of CARLA**. You can dowload it from [here](https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/Leaderboard/CARLA_Leaderboard_20.tar.gz).
While some agents might have slight variations of this process, it is only needed to **set the `CARLA_ROOT` environment variable** to point to your CARLA root folder:

```sh
export CARLA_ROOT=<path-to-carla>
```

We recommend adding this command to your `.bashrc` file to set it permanently.

## Building the agent docker image

To ease the creation of the docker files, each agent is already prepared with its own files, and they only have to be run in order to automatically create them. For instance, to build the `human-agent` stack:

```sh
bash human_agent/make_docker.sh
```

This will generate a `human_agent:latest` docker image

## Running the agent

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

## Subdmodules

