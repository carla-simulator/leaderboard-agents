# Map agent

The main feature of this agent is the use of the AD map library, which is an example of a library that parses the OpenDRIVE. As a result, the agent doesn't use the `carla.Map` class, which is considered as privileged information, and can be submitted to the Leaderboard. Using this library, the route can be interpolated, and adding a GNSS, IMU and speedometer, the agent is capable of lane following. Lastly, with the addition of a LIDAR, obstacles ahead of the ego are detected.

Additionally, all docker files can be divided in two parts, the basic requirements needed by the Leaderboard, and the agent specific ones. While other agents might have them mixed up, the docker file of this agent has been created in such a way that this is clearly differentiated.
