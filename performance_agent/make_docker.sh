#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

rm -fr ${SCRIPT_DIR}/.tmp

echo "Creating a temporary folder"
mkdir -p ${SCRIPT_DIR}/.tmp
mkdir -p ${SCRIPT_DIR}/.tmp/scenario_runner

echo "Copying the submodules into the folder"
cp -fr ${SCRIPT_DIR}/../submodules/scenario_runner/srunner ${SCRIPT_DIR}/.tmp/scenario_runner/srunner  # Only srunner is really needed
cp -fr ${SCRIPT_DIR}/../submodules/scenario_runner/requirements.txt ${SCRIPT_DIR}/.tmp/scenario_runner/requirements.txt  # And their requirements
cp -fr ${SCRIPT_DIR}/../submodules/leaderboard/ ${SCRIPT_DIR}/.tmp

cp ${SCRIPT_DIR}/entrypoint.sh ${SCRIPT_DIR}/.tmp/entrypoint.sh

echo "Building the docker"
docker build --force-rm -t profiler_agent -f ${SCRIPT_DIR}/Dockerfile ${SCRIPT_DIR}/.

echo "Removing the temporary folder"
rm -fr ${SCRIPT_DIR}/.tmp

