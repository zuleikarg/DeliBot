# DeliBot

## Requirements

To make your computer capable of ejecute all the scripts and make them work together, some installatins are needed.

| Plugin | Description |
| ------ | ------ |
| CUDA Toolkit 11.0 | [From the official page without drivers.][CUDA] |
| cuDNN | [Last version of cuDNN for CUDA 11.x][cuDNN] for CUDA configuration. |
| Anaconda | To get the requirements needed. |
| requirements.txt | Create enviroment with reuirements:  conda create --name <environment_name> --file requirements.txt . |


## Steps for execution:

Once you get all the requirements, you must follow some steps to archieve the results.

First, you must compile the DeliBot folder as a ROS workspace. From a terminal:
```sh
conda activate <environment_name>
cd <route_to_DeliBot_root>
catkin_make
```

Also, it's compulsory to export the path of the folder as a parameter and it's recomended to include it in the _.bash_ archive:
```sh
export DELIBOT_PATH=<path_of_folder>
```

It is recommended that you specify the type of turtlebot model used, in this case, the **burger** one, in the _.bash_ archive:
```sh
export TURTLEBOT3_MODEL=burger
```
If you don't follow the previous step, you must specify the turtlebot model used at each terminal.

In addition, it is important that you follow the steps below in each terminal before executing the rest of the scripts:
```sh
conda activate <environment_name>
cd <route_to_DeliBot_root>
source devel/setup.bash
```

The next step is executing the scripts in the terminals:

First Tab:
```sh
roslaunch turtlebot3_gazebo Office_world.launch
```
When gazebo have been loaded, you must remove the _waffle_ turtlebot.

Second Tab:

```sh
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=<path_to_DeliBot_folder>/Delibot/src/siam-mot/Office.yaml
```
When rviz have been loaded, you must adjust the _burger_ turtlebot to the correct position with ''2D Pose Estimate''.

Third Tab:

```sh
roslaunch turtlebot3_navigation move_base.launch
```

Fourth Tab:
```sh
rosrun my_code speech.py
```

Fifth Tab:

```sh
rosrun my_code navigation.py
```

Sixth Tab:


```sh
cd src/siam-mot/demos
python demo.py
```

Seventh Tab: Select the goal person

```sh
rosrun my_code interface.py
```
Eighth Tab: When necessary in simulation, send signal to represent that the person took the package

```sh
rostopic pub /collected my_code/collect "collected: true"
```


Otherwise, if you just want to take a new photo for a employee:

First Tab:
```sh
roscore
```

Second Tab:
```sh
rosrun my_code setup.py
```

## References

Some references that have been crucial to achieve the main objective are:

- [Turtlebot3] - Repository needed to use turtlebot3.
- [Turtlebot3_simulations] - To get the results in simulation.
- [SiamMOT] - To get the bounding box of the people detected.
- [Maskrcnn-benchmark] - Ass the main tool of SiamMot.
- [Face Recognition] - To compare the person in search to the person in the bbox.

   [CUDA]: <https://developer.nvidia.com/cuda-11.0-download-archive?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=2004&target_type=runfilelocal>
   [cuDNN]: <https://developer.nvidia.com/rdp/cudnn-archive>
   [Turtlebot3]: <https://github.com/ROBOTIS-GIT/turtlebot3/tree/noetic-devel>
   [Turtlebot3_simulations]: <https://github.com/ROBOTIS-GIT/turtlebot3_simulations/tree/noetic-devel>
   [SiamMOT]: <https://github.com/amazon-science/siam-mot>
   [Maskrcnn-benchmark]: <https://github.com/facebookresearch/maskrcnn-benchmark>
   [Face Recognition]: <https://github.com/ageitgey/face_recognition>
