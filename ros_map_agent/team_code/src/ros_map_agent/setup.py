
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    scripts=["nodes/ros_map_agent"],
    packages=["ros_map_agent", "ros_map_agent.map_agent"],
    package_dir={"": "src"}
)

setup(**d)
