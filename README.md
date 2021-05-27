# leaderboard-agents

This repository serves as a guideline for users to see how to run different agents inside the leaderboard. Each of these agent can be directly run on a local version of the Leaderboard, and they also come with their own docker files, to easily understand the steps needed to submit them into the Leaderboard itself. Additionally, all agents have there own specific purposes, so it is recommended to check them out and see if anyone suits your needs.

## Submodules

In order to run the Leaderboard, you need to also have [CARLA](https://github.com/carla-simulator/carla) as well as [ScenarioRunner](https://github.com/carla-simulator/scenario_runner) installed. Both ScenarioRunner and the Leaderboard are available in this repository, inside the `submodules` folder, and they will be automatically fetched when creating the docker. As it is expected for you to do some tests locally, a specific version of CARLA isn't been given, instead, use the `CARLA_ROOT` environment variable to point to your CARLA folder.

The `submodules` folder also contains references to other packages needed by specific agents. The following table shows the exact submodules used for each agent:

| Agent | ScenarioRunner | Leaderboard | AD Map | ROS Bridge |
| ---- | ----- | ----- | ------------- | -------- |
| AD Map agent |  &#9989; | &#9989;| &#9989;|  |
| ROS human agent | &#9989; | &#9989;| | &#9989;|
| Performance agent | &#9989; | &#9989; |  |  |

**Note:** Remember to download all the submodules using

```git submodule update --init --recursive```,

or if you only want a specific one:

```git submodule update --init --recursive <path to specific submodule>```.

## Creation of the agent docker

To ease the creation of the docker files, each agent is already prepared with its own files, and they only have to be run in order to automatically create them. While some agents might have slight variations of this process, the only steps needed are to **set the `CARLA_ROOT` environment variable** to point to the desired version of CARLA, and then run the docker creation file:

```bash <path to specific agent>/make_docker.sh```.

## Running the agent docker

The process of running the agent has also been prepared, having only to **start the CARLA server**, run the docker file

```bash <path to specific agent>/run_docker.sh```,

and run the Leaderboard

```bash leaderboard/scripts/run_evaluation.sh```.

**Note:** By default, all dockers have a shared volume correponding to the `results` folder.