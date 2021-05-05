# leaderboard-agents

This repository serves as a guideline for users to see how to run different agents inside of a docker, which is already prepared to be submitted into the Leaderboard. The `submodules` contains references to all the necessary modules that agents need to have in order to run the leaderboard. Except from scenario runner and the leaderboard, which all agents use, the rest of the packages might be unique to a specfic agent.

To create the docker:

1) Set the *CARLA_ROOT* environment variable to point to a CARLA package
2) Navigate to the desired agent and create its docker: `./make_docker.sh`.

And to run it:

1) Start the CARLA package
2) Navigate to the desired agent and run the docker: `./run_docker.sh`.
4) Run the *run_evaluation.sh* script: `bash leaderboard/scripts/run_evaluation.sh`.
