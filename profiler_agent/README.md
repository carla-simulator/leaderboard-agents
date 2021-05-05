# profiler-agent

```sh
sh -c 'echo 1 >/proc/sys/kernel/perf_event_paranoid'
nsys profile --sampling-period 500000 --sample=cpu --output=/workspace/profiling/<NAME>.qdrep bash team_code/run_profiler.sh
```
