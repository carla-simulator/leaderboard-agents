#!/usr/bin/env python
# Copyright (c) 2021 Intel Corporation.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

from __future__ import print_function

import argparse
import os
import sys
import traceback
from argparse import RawTextHelpFormatter

import carla
import nvtx
import py_trees

from srunner.scenariomanager.carla_data_provider import CarlaDataProvider
from srunner.scenariomanager.timer import GameTime

from leaderboard.leaderboard_evaluator import LeaderboardEvaluator
from leaderboard.scenarios.scenario_manager import ScenarioManager
from leaderboard.utils.statistics_manager import StatisticsManager
from leaderboard.autoagents.agent_wrapper import AgentError
from leaderboard.envs.sensor_interface import SensorReceivedNoData


class ScenarioManagerWithAnnotations(ScenarioManager):

    @nvtx.annotate("ScenarioManager._tick", color="blue")
    def _tick_scenario(self):
        """
        Run next tick of scenario and the agent and tick the world.
        """

        if self._running and self.get_running_status():
            with nvtx.annotate("ScenarioManager._tick_carla", color="red"):
                CarlaDataProvider.get_world().tick(self._timeout)

        timestamp = CarlaDataProvider.get_world().get_snapshot().timestamp

        if self._timestamp_last_run < timestamp.elapsed_seconds and self._running:
            self._timestamp_last_run = timestamp.elapsed_seconds

            self._watchdog.update()
            # Update game time and actor information
            GameTime.on_carla_tick(timestamp)
            with nvtx.annotate("CarlaDataProvider.on_carla_tick", color="green"):
                CarlaDataProvider.on_carla_tick()

            with nvtx.annotate("ScenarioManager._tick_agent", color="green"):
                self._watchdog.pause()

                try:
                    self._agent_watchdog.resume()
                    self._agent_watchdog.update()
                    ego_action = self._agent_wrapper()
                    self._agent_watchdog.pause()

                # Special exception inside the agent that isn't caused by the agent
                except SensorReceivedNoData as e:
                    raise RuntimeError(e)

                except Exception as e:
                    raise AgentError(e)

                self._watchdog.resume()
                self.ego_vehicles[0].apply_control(ego_action)

            # Tick scenario. Add the ego control to the blackb
            with nvtx.annotate("ScenarioManager._tick_scenario", color="green"):
                py_trees.blackboard.Blackboard().set("AV_control", ego_action, overwrite=True)
                self.scenario_tree.tick_once()

            if self._debug_mode > 1:
                self.compute_duration_time()

                # Update live statistics
                self._statistics_manager.compute_route_statistics(
                    self.config,
                    self.scenario_duration_system,
                    self.scenario_duration_game,
                    failure_message=""
                )
                self._statistics_manager.write_live_results(
                    self.config.index,
                    self.ego_vehicles[0].get_velocity().length(),
                    ego_action,
                    self.ego_vehicles[0].get_location()
                )

            if self._debug_mode > 2:
                print("\n")
                py_trees.display.print_ascii_tree(self.scenario_tree, show_status=True)
                sys.stdout.flush()

            if self.scenario_tree.status != py_trees.common.Status.RUNNING:
                self._running = False

            with nvtx.annotate("ScenarioManager.move_spectator", color="green"):
                ego_trans = self.ego_vehicles[0].get_transform()
                self._spectator.set_transform(carla.Transform(ego_trans.location + carla.Location(z=80),
                                                              carla.Rotation(pitch=-90)))


class LeaderboardWithAnnotations(LeaderboardEvaluator):

    def __init__(self, args, statistics_manager):
        super(LeaderboardWithAnnotations, self).__init__(args, statistics_manager)

        self.manager = ScenarioManagerWithAnnotations(args.timeout, args.debug > 1)


def main():
    description = "CARLA AD Leaderboard Benchmark Evaluation: benchmark your Agent in CARLA scenarios\n"

    # general parameters
    parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--host', default='localhost',
                        help='IP of the host server (default: localhost)')
    parser.add_argument('--port', default=2000, type=int,
                        help='TCP port to listen to (default: 2000)')
    parser.add_argument('--traffic-manager-port', default=8000, type=int,
                        help='Port to use for the TrafficManager (default: 8000)')
    parser.add_argument('--traffic-manager-seed', default=0, type=int,
                        help='Seed used by the TrafficManager (default: 0)')
    parser.add_argument('--debug', type=int,
                        help='Run with debug output', default=0)
    parser.add_argument('--record', type=str, default='',
                        help='Use CARLA recording feature to create a recording of the scenario')
    parser.add_argument('--timeout', default=300.0, type=float,
                        help='Set the CARLA client timeout value in seconds')

    # simulation setup
    parser.add_argument('--routes', required=True,
                        help='Name of the routes file to be executed.')
    parser.add_argument('--routes-subset', default='', type=str,
                        help='Execute a specific set of routes')
    parser.add_argument('--repetitions', type=int, default=1,
                        help='Number of repetitions per route.')

    # agent-related options
    parser.add_argument("-a", "--agent", type=str,
                        help="Path to Agent's py file to evaluate", required=True)
    parser.add_argument("--agent-config", type=str,
                        help="Path to Agent's configuration file", default="")

    parser.add_argument("--track", type=str, default='SENSORS',
                        help="Participation track: SENSORS, MAP")
    parser.add_argument('--resume', type=bool, default=False,
                        help='Resume execution from last checkpoint?')
    parser.add_argument("--checkpoint", type=str, default='./simulation_results.json',
                        help="Path to checkpoint used for saving statistics and resuming")
    parser.add_argument("--debug-checkpoint", type=str, default='./live_results.txt',
                        help="Path to checkpoint used for saving live results")

    arguments = parser.parse_args()

    statistics_manager = StatisticsManager(arguments.checkpoint, arguments.debug_checkpoint)

    try:
        leaderboard_evaluator = LeaderboardWithAnnotations(arguments, statistics_manager)
        leaderboard_evaluator.run(arguments)

    except Exception as e:
        traceback.print_exc()
    finally:
        del leaderboard_evaluator


if __name__ == '__main__':
    main()