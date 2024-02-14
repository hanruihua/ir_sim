import yaml
from ir_sim.util.util import file_check

class EnvPara:
    '''
    The base class of environment parameters read from yaml file.
        basic categories: world, plot, robot, obstacle, robots, obstacles, plot


    '''


    def __init__(self, world_name) -> None:
        
        world_file_path = file_check(world_name)

        world_kwargs, plot_kwargs, robot_kwargs_list, robots_kwargs_list, obstacle_kwargs_list, obstacles_kwargs_list  = dict(), dict(), [], [], [], []

        if world_file_path != None:
           
            with open(world_file_path) as file:
                com_list = yaml.load(file, Loader=yaml.FullLoader)
                world_kwargs = com_list.get('world', dict())
                plot_kwargs = com_list.get('plot', dict())
                keyboard_kwargs = com_list.get('keyboard', dict())
                robot_kwargs_list = com_list.get('robot', list())
                robots_kwargs_list = com_list.get('robots', list())
                obstacle_kwargs_list = com_list.get('obstacle', list())
                obstacles_kwargs_list = com_list.get('obstacles', list())

        # for python 3.10
        # world_kwargs |= kwargs.get('world', dict())
        # plot_kwargs |= kwargs.get('plot', dict())
        # robots_kwargs |= kwargs.get('robots', dict())
        # obstacles_kwargs |= kwargs.get('obstacles', dict())
        # robot_kwargs |= kwargs.get('robot', dict())


    



