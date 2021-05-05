# performance-agent

This agent is intended to benchmark and profile the leaderboard.

**This agent should not be taken as a reference to build other leadeboard agents.**

## Setup

Firstly clone the `leadeboard-agents` repository:

```
git clone --recurse-submodules https://github.com/carla-simulator/leaderboard-agents
```

Then, build the `performance.agent` image:

```sh
cd performance_agent && ./make_docker.sh
```

## Usage

1. Run a CARLA server.

```sh
./CarlaUE4.sh
```

2. Run the `performance-agent` image:
```
./run_docker.sh
```

**Important**: It is necessary to set a `CARLA_ROOT` environment variable pointing to a CARLA package.

### Benchmarking

To start a benchmark run the following command:

```
bash team_code/scripts/run_benchmark.sh
```

### Profiling

To start the profiler run the following commands:

```sh
sh -c 'echo 1 >/proc/sys/kernel/perf_event_paranoid'
nsys profile --sampling-period 500000 --sample=cpu --output=/workspace/profiling/<NAME>.qdrep bash team_code/scripts/run_profiler.sh
```
