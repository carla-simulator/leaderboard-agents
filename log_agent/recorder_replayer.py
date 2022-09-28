#!/usr/bin/env python

# Copyright (c) 2020 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
import argparse
import threading
import sys

import carla

FPS = 20
FIRST_FRAME = 0
LAST_FRAME = None
REPLAY_SPEED = 1
TIME = 0

def tick(world):
    global TIME, REPLAY_SPEED
    world.tick()
    TIME += world.get_snapshot().delta_seconds * REPLAY_SPEED

def recorder_utilities(world, client):
    global LAST_FRAME, REPLAY_SPEED, FIRST_FRAME
    stop = False

    while not stop and not LAST_FRAME:
        data = input("\nInput the next action: ")
        try:
            int_data = float(data)
            print("  Setting the replayer factor to {}".format(int_data))
            client.set_replayer_time_factor(int_data)
            REPLAY_SPEED = int_data
        except ValueError:
            if data not in ("S", "R"):
                print("\033[93mIgnoring unknown command '{}'\033[0m".format(data))
                continue

            print("  Frame: {}\n  Time: {}".format(
                world.get_snapshot().frame - FIRST_FRAME, round(TIME, 3))
            )
            if data == 'S':
                stop = True
    LAST_FRAME = world.get_snapshot().frame

def main():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument('--host', metavar='H', default='localhost',
                           help='IP of the host CARLA Simulator (default: localhost)')
    argparser.add_argument('--port', metavar='P', default=2000, type=int,
                           help='TCP port of CARLA Simulator (default: 2000)')

    # Recorder arguments
    argparser.add_argument('-f', '--file', default='', required=True,
                           help='File to be executed')
    argparser.add_argument('--start-time', default=0, type=float,
                           help='Start time of the recorder')
    argparser.add_argument('--end-time', default=0, type=float,
                           help='End time of the recorder. If different from 0, the simulation will automatically stop at that time')
    argparser.add_argument('--follow-id', default=0, type=int, help='ID to follow')
    argparser.add_argument('--follow-ego', action="store_true", help='follow the ego vehicle')
    argparser.add_argument('--factor', default=1, type=float, help='Initial recorder factor')

    # Simulation arguments
    argparser.add_argument('--reload-world', action='store_true',
                           help='Reloads the world. Needed when recording differents logs')

    args = argparser.parse_args()

    if args.follow_id and args.follow_ego:
        print("Choose to either follow an id, or the ego vehicle, but not both")
        sys.exit(0)

    global TIME, LAST_FRAME, FIRST_FRAME

    TIME = args.start_time

    client = None
    world = None

    # Get the client
    print("\n\033[1m> Setting the simulation\033[0m")
    client = carla.Client(args.host, args.port)
    client.set_timeout(120.0)

    # Get the recorded data
    file_info = client.show_recorder_file_info(args.file, True)

    # Load / reload / Get the world
    map_name = file_info.split("\n")[1].replace("Map: ", "")
    sim_map_name = client.get_world().get_map().name.split('/')[-1]

    if sim_map_name != map_name:
        print("Detected a different map that the recorded one. Loading map '{}'".format(map_name))
        world = client.load_world(map_name)
    elif args.reload_world:
        world = client.reload_world()
    else:
        world = client.get_world()

    # Synchronous mode provides a smoother motion of the camera that follows the ego
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 1/FPS
    world.apply_settings(settings)

    # Get the world frame before the recorded starts. TODO: Understand why this is one more (hence the -1)
    FIRST_FRAME = world.get_snapshot().frame - 1

    # Get the ego vehicle id so that the spectator focuses on it
    follow_id = args.follow_id
    if args.follow_ego:
        file_split = file_info.split("Create ")
        for data in file_split:
            if not "role_name = hero\n" in data:
                continue
            follow_id = int(data.split(": ")[0])
            print("Detected an ego vehicle with id '{}'".format(follow_id))
            break

    # Get the duration of the recorder (only if the end time is 0, aka until the recorder end)
    duration = args.end_time
    if not duration:
        duration = float(file_info.split("Duration: ")[-1].split(" ")[0])

    print("\033[1m> Starting the replayer\033[0m")
    client.replay_file(args.file, args.start_time, args.end_time, follow_id)
    client.set_replayer_time_factor(args.factor)

    tick(world)

    try:
        print("\033[1m> Running the recorder. Use\033[0m")
        print("\033[1m  - R: to record the replayer timestamp data\033[0m")
        print("\033[1m  - S: to stop the script\033[0m")
        print("\033[1m  - A number: to change the speed's factor of the replayer\033[0m")

        t1 = threading.Thread(target=recorder_utilities, args=(world, client, ))
        t1.start()

        while not LAST_FRAME:
            tick(world)
            if TIME >= duration:
                LAST_FRAME = world.get_snapshot().frame

    except KeyboardInterrupt:
        pass
    finally:

        if world is not None:
            settings = world.get_settings()
            settings.synchronous_mode = False
            settings.fixed_delta_seconds = None
            world.apply_settings(settings)

        if client is not None:
            client.set_replayer_time_factor(1)

if __name__ == '__main__':
    main()
