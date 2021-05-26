# leaderboard-agents

This repository serves as a guideline for users to see how to run different agents inside of a docker which is already prepared to be submitted into the Leaderboard. The `submodules` contains references to all the necessary modules that agents need to have in order to run the leaderboard. Remember to use `git submodule update --init --recursive` to download all submodules.

Except from scenario runner and the leaderboard, which all agents use, the rest of the packages might be unique to a specfic agent. Navigate to each of the agents to understand more about what they do and which of the submodules do they require. Some agents might be run differently but for most cases, do the following in order to create and run them:

1) Set the *CARLA_ROOT* environment variable to point to a CARLA package
2) Create the docker of the desired agent: `./agent-folder-path/make_docker.sh`.
3) Start the CARLA server
4) Run the docker: `./agent-folder-path/run_docker.sh`.
5) Run the *run_evaluation.sh* script to start the leaderboard: `bash leaderboard/scripts/run_evaluation.sh`.


