#!/bin/bash

export TEAM_AGENT=$TEAM_CODE_ROOT/map_agent.py
export SCENARIOS=$LEADERBOARD_ROOT/data/all_towns_traffic_scenarios_public.json
export ROUTES=$LEADERBOARD_ROOT/data/routes_training.xml
export REPETITIONS=1
export CHALLENGE_TRACK_CODENAME=MAP
export DEBUG_CHALLENGE=0
export RECORD_PATH=
export RESUME=

bash $LEADERBOARD_ROOT/scripts/run_evaluation.sh
