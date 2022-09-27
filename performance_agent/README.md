# Performance agent

This agent is intended to be used as a helping tool in benchmarking and profiling the different aspects of the Leaderboard. As the focus of this agent is the Leaderboard itself, and not the agent, it will function very differently from the rest. As such **this agent should not be taken as a reference** to build other Leaderboard agents.

### Usage of the agent

To ease the testing of the Leaderboard and CARLA, this agent has several modifications.

When running the docker, **the Leaderboard and Scenario Runner volumes are shared** with its local counterparts. Therefore, any changes made will directly affect the ones inside the docker.

For CARLA, the `CARLA_ROOT` environment variable isn't used when building the docker, but instead, taken into account when running it, so that different CARLA versions can be easily used. To change the version of CARLA, change the `CARLA_ROOT`, close and reopen the docker.

### Benchmarking

The agent comes with a benchmark script, which runs a [version of the Leaderboard](https://github.com/carla-simulator/leaderboard-agents/blob/main/performance_agent/team_code/benchmark/leaderboard_evaluator.py) that acts as a wrapper, recording several parameters of each route, and creating a table so that they can be compared. To start a benchmark, just run the benchmark script:

```
bash team_code/benchmark/run_benchmark.sh -o <benchmark file name>
```

By default, the docker shares the `workspace/results` folder, so it is recommended to place the file there.

### Profiling

Lastly, the agent is also capable of performing profiling. This uses a [version of the Leaderboard](https://github.com/carla-simulator/leaderboard-agents/blob/main/performance_agent/team_code/profiler/leaderboard_evaluator.py) that has annotations during the Leaderboard runtime. This creates a file that can then be opened using NVIDIA Nsight Systems. **To avoid the files being excessively big**, a [specific route](https://github.com/carla-simulator/leaderboard-agents/tree/main/performance_agent/team_code/profiler/data) is used, and **it should be stopped mid simulation**. To create the profiler file, run the following commands:

```sh
sh -c 'echo 1 >/proc/sys/kernel/perf_event_paranoid'
nsys profile --sampling-period 500000 --sample=cpu --output=/workspace/results/profiler/<profiler file name>.qdrep bash team_code/profiler/run_profiler.sh
```

By default, the docker shares the `workspace/results` folder, so it is recommended to place the file there. If so, then it is only needed to run NVIDIA Nsight Systems at your local machine, and open the file previously created.
