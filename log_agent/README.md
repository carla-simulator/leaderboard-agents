# Log agent

The main feature of this agent is its capability to record the simualted routes, in order to replay them later on. With this agent, several baselines can be created which can be used to understand the optimal behavior of the AV stack. This agent is meant to be manually controlled.

### Usage of the agent

To use the agent, create and run the docker the same way as any of the other agents. Note that when running the docker, a `HOST_RESULTS_PATH` variable is being set up. This variable is used **by the server** to know where to place the recorder logs.

Once inside the docker, run the `run_evaluation.sh` script as normal, but this agent has several additional arguments:

```
bash leaderboard/scripts/run_evaluation.sh -m <mode> -id <id>
```

The first argument, `-m`, is the mode, which has two values, `log`, and `playback`.

By using the `log` mode, the CARLA recorder will be activated, and, for all frames, both the state and control actions of the ego vehicle will be saved into a *json* file. With this mode, `-id` is the folder name where all these files will be saved. The chosen folder will be saved inside the `results` one.

The `playback` mode allows replaying a previously saved log of the ego vehicle in a new simulation. In this case, the `-id` should be the path to such log.

Lastly, this agent also offers a `recorder_replayer.py`, which can replay the CARLA logs. Remember to use the `HOST_RESULTS_PATH` variable when running the script from inside the docker, as the server will be the one searching for the CARLA log file.

