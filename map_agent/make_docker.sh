#!/bin/bash

if [ -z "$CARLA_ROOT" ]; then
  echo "Error $CARLA_ROOT is empty. Set \$CARLA_ROOT as an environment variable first."
  exit 1
fi

rm -fr .tmp

echo "Creating a temporary file"
mkdir -p .tmp
mkdir -p .tmp/scenario_runner

echo "Copying the submodules into the folder"
cp -fr ${CARLA_ROOT}/PythonAPI  .tmp
cp -fr ../submodules/scenario_runner/srunner .tmp/scenario_runner/srunner  # Only srunner is really needed
cp -fr ../submodules/leaderboard/ .tmp
cp -fr ../submodules/map/ .tmp/map

mv .tmp/PythonAPI/carla/dist/carla*-py2*.egg .tmp/PythonAPI/carla/dist/carla-leaderboard-py2x.egg
mv .tmp/PythonAPI/carla/dist/carla*-py3*.egg .tmp/PythonAPI/carla/dist/carla-leaderboard-py3x.egg

echo "Copying the team code into the folder"
cp -fr team_code/ .tmp/team_code

echo "Building the docker"
docker build --force-rm -t map_agent_2 -f Dockerfile.master .

echo "Removing the temporary file"
rm -fr .tmp
