# performance-agent

This agent is intended to be used as a helping tool in benchmarking and profiling the different aspects of the Leaderboard. As the focus of this agent is the Leaderboard itself, and not the agent, it will function very differently from the rest. As such **this agent should not be taken as a reference** to build other Leaderboard agents.

Due to its unique objective, its usage is also different:

1) Build the docker of the agent `./make_docker.sh`
2) Run the CARLA server `./CarlaUE4.sh`
3) Set a `CARLA_ROOT` environment variable pointing to the CARLA package.
4) Run the docker `./run_docker.sh`

As its focus is the Leaderboard itself, when running the docker, the Leaderboard and Scenario Runner submodule volumes will be shared with its local counterparts and any changes made will directly affect the docker. For CARLA, the `CARLA_ROOT` environment variable is used, so in order to use different versions of CARLA, such set that variable, close and reopen the docker.

### Benchmarking

To start a benchmark run the benchmark script.

```
bash team_code/benchmark/run_benchmark.sh
```

This script runs a [version of the Leaderboard](https://github.com/carla-simulator/leaderboard-agents/tree/profiler_agent/performance_agent/team_code/leaderboard/benchmark) that records and benchmarks all the simulated routes.

### Profiling

To start the profiler run the profiler script:

```sh
sh -c 'echo 1 >/proc/sys/kernel/perf_event_paranoid'
nsys profile --sampling-period 500000 --sample=cpu --output=/workspace/results/profiler/<NAME>.qdrep bash team_code/profiler/run_profiler.sh
```

**Note that `<NAME>` will be name of the profilling file.**

This script runs a [version of the Leaderboard](https://github.com/carla-simulator/leaderboard-agents/tree/profiler_agent/performance_agent/team_code/leaderboard/profiler) with anotations at the functions of the Leaderboard called during runtime. This Leaderboard creates a file that can then be opened using NVIDIA Nsight Systems. **TODO:** Add that the route is fixed and not $ROUTES and that should be stopped mid simulation