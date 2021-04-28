# map-agent

The main feature of this agent is the use of the AD map library, which is an example of a library tcan be used during the Leaderboard capable of parsing the OpenDrive without the need to access the carla.Map. Using the library and some sensors, the agent is capable of following the lane and by adding a LIDAR, obstacles ahead of the ego are detected.

To create the docker:

1) Set the *CARLA_ROOT* environment variable to point to a CARLA package
2) Run the *make_docker.sh* file `./make_docker.sh`.

And to run it:

1) Start the CARLA package
2) Run the *run_docker.sh* file `./run_docker.sh`.
3) Navigate to the taem code folder `cd team_code`.
4) Run the *map_script.sh* file `./map_script.sh`.
