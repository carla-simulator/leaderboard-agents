# leaderboard-agents

This repository serves as a guideline for users to see how to run different agents inside of a docker, which is already prepared to be submitted into the Leaderboard. The `submodules` contains references to all the necessary modules that agents need to have in order to run the leaderboard. Except from scenario runner and the leaderboard, which all agents use, the rest of the packages might be unique to a specfic agent.

To create the agent docker, navigate to their specific folder and run the `make_docker.sh` file. Use the `run_docker.sh` to run them.
