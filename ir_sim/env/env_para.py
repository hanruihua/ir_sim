import yaml
from ir_sim.util.util import file_check

class EnvPara:
    '''
    The base class of environment parameters read from yaml file.
        basic categories: world, plot, robot, obstacle, robots, obstacles, plot


    '''


    def __init__(self, world_name) -> None:
        
        world_file_path = file_check(world_name)

        self.kwargs_parse = { 'world': dict(), 'plot': dict(), 'keyboard': dict(), 'robot': dict(), 'robots': dict(), 'obstacles': dict(), 'landmarks': dict()}

        if world_file_path != None:
           
            with open(world_file_path) as file:
                com_list = yaml.load(file, Loader=yaml.FullLoader)
                self.kwargs_parse['world'] = com_list.get('world', dict())
                self.kwargs_parse['plot'] = com_list.get('plot', dict())
                self.kwargs_parse['keyboard'] = com_list.get('keyboard', dict())
                self.kwargs_parse['robot'] = com_list.get('robot', dict())
                self.kwargs_parse['robots'] = com_list.get('robots', dict())
                self.kwargs_parse['obstacles'] = com_list.get('obstacles', dict())
                self.kwargs_parse['landmarks'] = com_list.get('landmarks', dict())

        else:
            print('File not found!')



        # for python 3.10
        # world_kwargs |= kwargs.get('world', dict())
        # plot_kwargs |= kwargs.get('plot', dict())
        # robots_kwargs |= kwargs.get('robots', dict())
        # obstacles_kwargs |= kwargs.get('obstacles', dict())
        # robot_kwargs |= kwargs.get('robot', dict())


    



