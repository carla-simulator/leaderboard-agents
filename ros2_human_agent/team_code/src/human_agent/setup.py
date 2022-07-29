from setuptools import setup

package_name = 'human_agent'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['launch/human_agent.launch.py']),
        ('share/' + package_name, ['config/config.rviz']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jmoriana',
    maintainer_email='joel.moriana@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'human_agent = human_agent.human_agent:main'
        ],
    },
)
