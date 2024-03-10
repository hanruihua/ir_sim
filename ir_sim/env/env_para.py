import yaml
from ir_sim.util.util import file_check

class EnvPara:
    '''
    The base class of environment parameters read from yaml file.
        basic categories: world, plot, robot, obstacle, robots, obstacles, plot


    '''


    def __init__(self, world_name) -> None:
        
        world_file_path = file_check(world_name)

        self.kwargs_parse = { 'world': dict(), 'plot': dict(), 'keyboard': dict(), 'robot': list(), 'robots': list(), 'obstacles': list(), 'landmarks': list()}

        if world_file_path != None:
           
            with open(world_file_path) as file:
                com_list = yaml.load(file, Loader=yaml.FullLoader)

                for key in self.kwargs_parse.keys():
                    self.kwargs_parse[key] = com_list.get(key, dict())

        else:
            print('File not found!')





        





        # for python 3.10
        # world_kwargs |= kwargs.get('world', dict())
        # plot_kwargs |= kwargs.get('plot', dict())
        # robots_kwargs |= kwargs.get('robots', dict())
        # obstacles_kwargs |= kwargs.get('obstacles', dict())
        # robot_kwargs |= kwargs.get('robot', dict())


    



