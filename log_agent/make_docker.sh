#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$CARLA_ROOT" ]; then
  echo "Error $CARLA_ROOT is empty. Set \$CARLA_ROOT as an environment variable first."
  exit 1
fi

rm -fr ${SCRIPT_DIR}/.tmp

echo "Creating a temporary folder"
mkdir -p ${SCRIPT_DIR}/.tmp
mkdir -p ${SCRIPT_DIR}/.tmp/scenario_runner

echo "Copying the submodules into the folder"
cp -fr ${CARLA_ROOT}/PythonAPI  ${SCRIPT_DIR}/.tmp
cp -fr ${SCRIPT_DIR}/../_submodules/scenario_runner/srunner ${SCRIPT_DIR}/.tmp/scenario_runner/srunner  # Only srunner is really needed
cp -fr ${SCRIPT_DIR}/../_submodules/scenario_runner/requirements.txt ${SCRIPT_DIR}/.tmp/scenario_runner/requirements.txt  # And their requirements
cp -fr ${SCRIPT_DIR}/../_submodules/leaderboard/ ${SCRIPT_DIR}/.tmp

mv ${SCRIPT_DIR}/.tmp/PythonAPI/carla/dist/carla*-py2*.egg ${SCRIPT_DIR}/.tmp/PythonAPI/carla/dist/carla-leaderboard-py2x.egg
mv ${SCRIPT_DIR}/.tmp/PythonAPI/carla/dist/carla*-py3*.egg ${SCRIPT_DIR}/.tmp/PythonAPI/carla/dist/carla-leaderboard-py3x.egg

echo "Copying the team code into the folder"
cp -fr ${SCRIPT_DIR}/team_code/ ${SCRIPT_DIR}/.tmp/team_code

echo "Building the docker"
docker build --force-rm -t log_agent -f ${SCRIPT_DIR}/Dockerfile ${SCRIPT_DIR}/.

echo "Removing the temporary folder"
rm -fr ${SCRIPT_DIR}/.tmp
